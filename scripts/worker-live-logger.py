#!/usr/bin/env python3
"""Run the isolated OpenCode Worker with live, content-free progress and heartbeat logs.

The full stdout/stderr remains runner-local; neither GitHub Actions logs nor the
uploaded progress artifact contain prompts, file content, tool arguments or outputs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
TOOL = re.compile(r"(?:^|\s)[→←]\s*(Read|Edit|Write|Glob|Grep|Skill|Shell|Bash|Task|WebFetch|WebSearch)\b")
DIAGNOSTICS = (
    ("Model unavailable", "model_unavailable"),
    ("Permission denied", "permission_denied"),
    ("Command exceeded timeout", "command_timeout"),
    ("websocket open timeout", "browser_websocket_timeout"),
)
HEARTBEAT_SECONDS = 45
IDLE_WARNING_SECONDS = 180
PROGRESS_THROTTLE_SECONDS = 8


def classify(line: str) -> str | None:
    """Return an allowlisted category; never return original model text or a path."""
    clean = ANSI.sub("", line).strip()
    matched = TOOL.search(clean)
    if matched:
        return "tool_" + matched.group(1).lower()
    if clean.startswith("$ "):
        return "tool_shell"
    if clean.startswith("> build"):
        return "model_turn"
    for phrase, code in DIAGNOSTICS:
        if phrase.lower() in clean.lower():
            return "diagnostic_" + code
    return None


def run(model: str, title: str, prompt_file: Path, root: Path,
        heartbeat_seconds: int = HEARTBEAT_SECONDS) -> int:
    if heartbeat_seconds < 1:
        raise ValueError("heartbeat interval must be positive")
    root.mkdir(parents=True, exist_ok=True)
    raw_path = root / "worker-output.raw"
    progress_path = root / "worker-progress.jsonl"
    start = time.monotonic()
    last_output = start
    last_report = start
    bytes_written = 0
    action_count = 0
    last_action = "none"
    queue_: queue.Queue[bytes | None] = queue.Queue()
    prompt = prompt_file.read_text(encoding="utf-8")

    def emit(kind: str, **fields: object) -> None:
        record = {
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": int(time.monotonic() - start),
            "kind": kind,
            **fields,
        }
        with progress_path.open("a", encoding="utf-8") as dest:
            dest.write(json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n")
        # No raw model text, arguments, paths, GitHub token, or environment in Actions logs.
        printable = " ".join(f"{key}={value}" for key, value in record.items() if key != "time")
        print("[worker-live] " + printable, flush=True)

    command = ["opencode", "run", "--model", model, "--agent", "build", "--title", title, prompt]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)

    def reader() -> None:
        assert proc.stdout is not None
        try:
            while True:
                chunk = os.read(proc.stdout.fileno(), 4096)
                if not chunk:
                    break
                queue_.put(chunk)
        finally:
            queue_.put(None)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    def terminate(_signum: int, _frame: object) -> None:
        emit("termination_requested", output_bytes=bytes_written)
        if proc.poll() is None:
            proc.terminate()

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)

    pending = b""
    eof = False
    next_heartbeat = start + heartbeat_seconds
    emit("started", heartbeat_interval_seconds=heartbeat_seconds)
    with raw_path.open("wb") as raw:
        while not eof:
            now = time.monotonic()
            try:
                chunk = queue_.get(timeout=max(0.05, min(1.0, next_heartbeat - now)))
            except queue.Empty:
                chunk = b""
            if chunk is None:
                eof = True
            elif chunk:
                raw.write(chunk)
                raw.flush()
                bytes_written += len(chunk)
                last_output = time.monotonic()
                pending += chunk
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    category = classify(line.decode("utf-8", errors="replace"))
                    if category:
                        action_count += 1
                        last_action = category
                        # Always report allowlisted errors; throttle ordinary tool activity.
                        if category.startswith("diagnostic_") or time.monotonic() - last_report >= PROGRESS_THROTTLE_SECONDS:
                            emit("activity", category=category, observed_events=action_count,
                                 output_bytes=bytes_written)
                            last_report = time.monotonic()
                # Don't let a non-newline stdout fragment consume unbounded memory.
                if len(pending) > 16384:
                    pending = pending[-4096:]
            now = time.monotonic()
            if now >= next_heartbeat:
                idle = int(now - last_output)
                emit("heartbeat", running=(proc.poll() is None),
                     output_bytes=bytes_written, idle_seconds=idle,
                     observed_events=action_count, last_reported_category=last_action)
                if idle >= IDLE_WARNING_SECONDS:
                    emit("idle_warning", idle_seconds=idle)
                next_heartbeat = now + heartbeat_seconds

    thread.join(timeout=2)
    result = proc.wait()
    emit("finished", exit_code=result, output_bytes=bytes_written,
         observed_events=action_count)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--heartbeat-seconds", type=int, default=HEARTBEAT_SECONDS)
    opts = parser.parse_args()
    return run(opts.model, opts.title, opts.prompt_file, opts.root, opts.heartbeat_seconds)


if __name__ == "__main__":
    sys.exit(main())

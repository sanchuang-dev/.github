"""Local tests for the trusted Worker live-log supervisor (no model or GitHub required)."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "worker-live-logger.py"
SPEC = importlib.util.spec_from_file_location("worker_live_logger", SCRIPT)
LOGGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOGGER)


class ProgressLogTests(unittest.TestCase):
    def test_only_known_event_labels_are_exposed(self):
        self.assertEqual(LOGGER.classify("← Edit file-with-secret.txt"), "tool_edit")
        self.assertEqual(LOGGER.classify("→ Read private/secret.env"), "tool_read")
        self.assertEqual(LOGGER.classify("$ echo secret-value"), "tool_shell")
        self.assertEqual(LOGGER.classify("Error: Model unavailable: foo/bar"), "diagnostic_model_unavailable")
        self.assertIsNone(LOGGER.classify("API_KEY=private-token"))

    def test_heartbeat_redaction_and_exact_exit_code(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            binary = root / "opencode"
            binary.write_text(
                "#!/usr/bin/env python3\n"
                "import sys, time\n"
                "print('> build · FREE_MODEL_TEST', flush=True)\n"
                "print('← Edit sensitive-file-with-SUPERSECRET.txt', flush=True)\n"
                "print('API_KEY=SUPERSECRET', flush=True)\n"
                "time.sleep(1.3)\n"
                "print('Error: Model unavailable: SUPERSECRET', flush=True)\n"
                "sys.exit(7 if 'fail' in sys.argv else 0)\n",
                encoding="utf-8",
            )
            binary.chmod(0o755)
            prompt = root / "prompt.txt"
            prompt.write_text("PRIVATEPROMPT", encoding="utf-8")
            outputs = io.StringIO()
            with patch.dict(os.environ, {"PATH": str(root) + os.pathsep + os.environ["PATH"]}):
                with contextlib.redirect_stdout(outputs):
                    rc = LOGGER.run("test/model", "fail", prompt, root / "logs", heartbeat_seconds=1)
            self.assertEqual(rc, 7)
            public = outputs.getvalue() + (root / "logs" / "worker-progress.jsonl").read_text()
            self.assertNotIn("SUPERSECRET", public)
            self.assertNotIn("PRIVATEPROMPT", public)
            self.assertNotIn("sensitive-file", public)
            self.assertIn("heartbeat", public)
            self.assertIn("diagnostic_model_unavailable", public)
            self.assertIn("exit_code=7", outputs.getvalue())
            private = (root / "logs" / "worker-output.raw").read_text()
            self.assertIn("SUPERSECRET", private)
            events = [
                json.loads(row) for row in (root / "logs" / "worker-progress.jsonl").read_text().splitlines()
            ]
            self.assertEqual(events[-1]["exit_code"], 7)


if __name__ == "__main__":
    unittest.main()

# 三创免费 Worker · 标准接入与验收

状态：组织标准候选（本文件合并后生效） · Owner：`sanchuang-dev/.github`

## 1. 责任与边界

- **组织执行器**：[`sanchuang-free-worker-v2.yml`](../../.github/workflows/sanchuang-free-worker-v2.yml)，本模板采用安全加固并经过 Codex 审查的固定版本（[PR #8](https://github.com/sanchuang-dev/.github/pull/8) Merge SHA）：`985ff50c297b844af65a920bd38f9c0b1ae31098`。此前完成三创端到端烟测的是 `0118f124b7bb95d75273f377b69dbab9ca050750`；新版增加不可变执行器对默认分支与当前提交的强制验证，**尚未单独进行恶意分支派工与新版本端到端测试**。任何升级必须经 PR 审查，各业务仓库分别更新固定 SHA，不使用 `@main` 等可移动引用。
- **组织模板**：[`workflow-templates/sanchuang-free-worker.yml`](../../workflow-templates/sanchuang-free-worker.yml)（GitHub Actions 的组织模板入口）；配套的 `.properties.json` 供 GitHub 展示。
- **仓库调用器**：每个仓库**单独选择接入**，将上述模板复制为该仓库默认分支上的 `.github/workflows/sanchuang-free-worker.yml`，通过独立 PR 审查。模板初始 `ENROLLED=false`、无有效工程分支、验证命令固定失败：**直接复制并不会自动拥有执行能力**。
- **人工授权**：只有维护者针对**已存在且仍 Open 的 Issue**明确授权施工，才可通过人工 `workflow_dispatch`，或经过仓库单独审查启用的受控 Issue 评论入口派工。创建 Issue、普通评论、机器人评论、PR 事件、CI 通过都不是授权。
- **交付权限**：只允许自由模型在隔离 Runner 中施工 → 全新只读 Runner 验证同一补丁 → 全新写权限 Runner 交付 **Draft PR**。Worker 不得自行合并、关卡验收、关闭 Issue、推进环境、部署或发布；分支晋级遵循 [environment-model](./environment-model.md)。

## 2. 接入前逐仓库检查

1. 核对仓库的默认分支、实际工程基线（通常 `dev`）、`AGENTS.md` 和仓库现有 CI。**默认分支仅用于向 GitHub 注册手动派工入口，不等于实现基线。** 标准模板拒绝向 `main`、`master`、`test`、`prod` 投递。如果仓库尚无合规工程基线，先完成独立工程分支建设，或为明确批准的例外单独设计受限调用器。
2. 在仓库 GitHub Settings → Actions → General → Workflow permissions 核查 **Allow GitHub Actions to create and approve pull requests** 已获组织和仓库允许；`GITHUB_TOKEN` 默认权限保持 **Read**，通过单个调用作业显式申请 `contents: write`、`pull-requests: write`、`issues: read`。如果设置被组织阻止，停止并上报，不用广域 PAT、私有密钥或偷偷修改组织策略绕行。
3. 选择仓库专属的**可信验证命令**。它们必须检查暂存的完整补丁，例如 `git diff --cached --check` 加仓库既有的 lint / typecheck / test / 构建及必要的文件范围断言。只有文档任务的明确例外才允许仅使用文档范围验证；普通代码工作不能以单纯 `echo PASS`、`true`、`|| true` 或跳过测试充数。仓库无可执行的可信验证方案时，不接入。
4. 将模板通过 PR 加入仓库**默认分支**，审查时完成：
   - 设置 `ENROLLED: "true"`；
   - 将 `ENGINEERING_BASE` 改为已核实且可写入 PR 的工程基线，如 `dev`；
   - 用该仓库的真实命令替换 `verification_command` 中的两个失败哨兵行；
   - 保留 `workflow_dispatch` 手动触发、校验后 Issue 号的 `fromJSON` 数字转换、两款 free 模型白名单、最小权限、固定组织 SHA 和单独守卫 Job。若启用 `issue_comment: created`，须保持评论身份 / 当前仓库权限 / Issue 状态 / 全文指令的 fail-closed 门禁，并经独立评审。
5. 维护者审查并明确合并该**接入 PR**，让工作流进入默认分支。接入完成 ≠ 已触发任务 ≠ 已验证该仓库的真实端到端流程。不得因为存在组织模板就对外声称所有仓库已接入。

> **见趣例外**：`sanchuang-dev/ai-mirror` 现有 `jianqu-free-worker-f01.yml` 是仅限 Issue #4、仅限文档、`main` bootstrap 的历史特许，**不能**直接复用为普适调用器；它所在的 Issue 已验收关闭。见趣已在 `main` 启用面向 `dev` 的一般 V2 调用器；新评论入口仍需单独审查 PR，并不因为组织模板升级自动生效。已有 V1 的业务仓库必须保留 V1，迁移需独立评审 PR，不得覆盖或并发派同一 Issue。

## 3. 模型、授权与运行

| 选项 | 真实模型路由 | 状态 |
| --- | --- | --- |
| 默认 MiMo | `opencode/mimo-v2.6-flash-free` | 免费目录白名单支持；三创尚未以此模型完成相同 E2E |
| 可选 DeepSeek | `opencode/deepseek-v4.1-flash-free` | 三创真实 Issue → Draft PR E2E 已验证 |

不使用 Provider API Key，不做收费模型自动降级/升级，免费路由随服务商状态可能变化。模型可见于 GitHub Actions 手工运行输入；用户不得在输入或 Issue 中发送 Token。

**派工前提**：核对目标仓库、Open Issue 编号、执行指令中的明确授权、默认分支上已生效的仓库调用器、实际工程基线和本仓库需触发的真实工作流名称。没有明确授权或运行入口不满足条件时停止。

**GitHub UI 人工派工**：目标仓库 → Actions → `Sanchuang Free Worker (opt-in)` → Run workflow → 选择默认分支 → 填写 Issue 编号与 MiMo/DeepSeek → Run。如果目标仓库的默认分支已经**独立合并并启用评论派工守卫**，则可按照 [GitHub Issue 原生派工入口](./free-worker-issue-comment-dispatch.md) 通过连接器发送精确维护者指令，再独立核对 Actions Run。尚未接入该守卫时，仍用 GitHub UI 派工；**不得未告知就使用用户远程电脑或本地 `gh` 作为替代**。如果用户明确逐次授权其他派工渠道，按授权限定操作并核对返回的 Actions run ID。

## 4. 交付和正式验收

对每次执行保留以下可复核材料：

- **Run 身份**：仓库、Issue、模型、手工触发来源、默认分支、工作流文件与组织固定 SHA、实际 Run URL。
- **作业结果**：`worker` 施工、`verify` 独立补丁验收、`delivery` Draft PR 创建必须全部成功；运行中、失败或跳过不得报告成功。日志与 14 天证据 Artifact 以实际 Actions 结果为准。
- **交付物**：核对 Draft PR 的实际 base 为仓库工程基线、范围/文件 diff 符合 Issue、不是直接提交环境分支、没有自行合并/发布。继续执行 AI Review、人类验收和分支晋级的组织流程。
- **失败分流**：模型 Free 路由失效、缺少实际 diff、验证失败、PR 权限不足分别报告具体阶段和日志；不自动重跑、不暗换模型，不为了绿灯削弱验收。
- **状态边界**：Draft PR 是交付，AI Review 是建议，合并是代码事实，Issue Completed/关闭仍需维护者验收授权。Project Status 只能在有真实访问权限时确认，不可由 Issue 状态推断其已同步。

## 5. 已知真实证据与升级

三创组织首个闭环由见趣 Issue #4 提供：[Actions #38875822060](https://github.com/sanchuang-dev/ai-mirror/actions/runs/38875822060) 与 [Draft PR #23（后经审查合并）](https://github.com/sanchuang-dev/ai-mirror/pull/23)。DeepSeek 免费版调用了原生 `execute-work-item` Skill，施工、独立验证、交付全部成功。前两次失败分别暴露了 `workflow_dispatch` 数值输入需要 `fromJSON`，以及已 `git add` 的真实改动需用 `git diff HEAD` 检测；均已修复在上述固定组织版本/见趣专用入口中。

标准模板的首次接入不是这次见趣 F01 的复刻：**必须选一张新的低风险真实 Issue，在该仓库审核过的工程分支上完成一次 E2E**。这一步的执行授权独立于模板合并授权。

版本升级必须修改组织执行器、得到 review 和可重现验证，再发布新的不可变 SHA；目标仓库逐个通过 PR 改 pin。对既有历史工作流不做静默替换。

## 6. V2 运行观测与浏览器验收（升级候选）

- 组织执行器候选改为 **Worker Job 60 分钟**（其中包括环境与工具阶段）；独立验证和 Draft 交付的作业时限不变。不能把 60 分钟理解成模型响应保证或端到端总预算。
- 受信监督程序在运行中提供 45 秒心跳、工具活动类别、无输出警告与退出码，实时打印到 Actions；不直接公开模型原始输出。退出后的 Artifact 包含脱敏进度记录、受限摘要与阶段证据，不包含原始提示词/工具内容。
- 新增 `skills/browser-verification/SKILL.md`，和主执行 Skill 由同一个 Organization 主分支提交加载，且遵守项目同名 Skill 禁止覆盖与 Skill allowlist。发生截图或 CDP 故障时限时止损，保留验收缺口。
- 这套能力只有在**组织 PR 审核合并**、明确冻结新的 40 位执行器 SHA、并且**目标仓库调用器经独立 PR 升级 pin**之后，才对该仓库后续派工生效。旧 pin（如 `985ff50c297b844af65a920bd38f9c0b1ae31098`）不会自动获得 60 分钟或新日志能力。
- 升级验收至少跑受信日志监督程序单元测试、检查 YAML 与 Skill 加载白名单，并在可控真实 Issue 上完成 Worker → verify → delivery 的独立 E2E；上线前不得宣称已验证该新执行器端到端。


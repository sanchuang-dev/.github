# 三创付费 Worker 接入（OpenCode Go）

> 状态：候选实现，合并并在一个调用仓库完成真实 E2E 前不得称为已上线。

## 定位

- 组织执行器：`.github/workflows/sanchuang-paid-worker.yml`。与免费 `sanchuang-free-worker-v2.yml` 并行，不更改、不回退到免费 Worker。
- 首期唯一允许的付费路由：`opencode-go/deepseek-v4.1-flash`；以 OpenCode Go 订阅和当前模型目录实际可用性为前提。
- 基于三创当前免费 V2 的防护结构：已打开且获授权的 Issue、受信默认分支派工校验、不可变组织 Skill、只读模型 Runner、独立只读补丁验收、独立写权限 Runner 仅创建 Draft PR。
- 公共仓库也可通过固定组织 commit SHA 调用公共 `.github` reusable workflow。

## 费用与密钥

1. 在 OpenCode Go 的工作区开通订阅，取得 Go API Key。**不要**放到 Issue、评论、仓库文件或 workflow_dispatch 输入。
2. 给试点调用仓库配置 repository secret `SANCHUANG_OPENCODE_GO_API_KEY`，或使用仅授权明确仓库集合的组织级 secret。不同组织的凭证不可默认为通用。GitHub Connector 不提供读取密钥值或创建密钥的能力。
3. 付费凭证仅注入模型 Runner 的 `OPENCODE_AUTH_CONTENT`；不传递给独立 verify/delivery jobs、工件或 PR 描述。模型和同 Runner shell 可以间接接触该执行环境：只用于可信、严格限权的付费额度，不应使用高权限通用密钥。
4. 无密钥或未开通 Go 时 fail closed；**绝不**自动从免费切换成付费，或在付费失败时调用别的计费服务。

## 每仓库受控 opt-in

先确认仓库默认分支、实际施工基线和 `AGENTS.md`，确定可信验证命令和 Actions PR 权限。新 caller 工作流进入仓库默认分支，base 应是文档明确的工程分支（通常 `dev`），引用的组织 workflow 必须是已审核并合并到 main 的 **40 位 commit SHA**，不能写 `@main`。每仓库单独 PR 审查。调用样例：

```yaml
name: Sanchuang Paid Worker
on:
  workflow_dispatch:
    inputs:
      issue_number:
        description: Existing authorized open Issue
        type: number
        required: true
jobs:
  worker:
    permissions:
      contents: write
      issues: read
      pull-requests: write
    uses: sanchuang-dev/.github/.github/workflows/sanchuang-paid-worker.yml@<REVIEWED_40_CHAR_MAIN_SHA>
    with:
      issue_number: ${{ fromJSON(inputs.issue_number) }}
      base_branch: dev # 必须按仓库实际工程基线调整
      verification_command: |
        git diff --cached --check
        npm ci --no-audit --no-fund
        npm run lint
        npm run build
      provider: opencode-go
      model: deepseek-v4.1-flash
    secrets:
      opencode_go_api_key: ${{ secrets.SANCHUANG_OPENCODE_GO_API_KEY }}
```

**样例不可直接原样接入**：调用器安装在 *仓库默认分支*；真实 verification 必须适配该仓库，证明补丁的代码行为，而不只是命令执行成功。若仓库已配置免费 Worker，付费 caller 使用不同 workflow 文件名和不同人工触发入口。

## 投递、验收与边界

- 仅在维护者明确授权已存在的 Open Issue 后，由 Actions 手工 `workflow_dispatch` 执行；本版不自动新增评论派工入口。不能因为某个仓库已有免费 `/worker run` 就认为付费版可以复用该触发器。
- 观察三段 job `worker → verify → delivery`，再检查 Draft PR 的 `base`、完整补丁和验证证据；都通过才算该次 Worker 交付。PR 合并、Issue 关闭、环境晋级和发布由维护者另行授权。
- 首个试点需完成一次真实付费模型推理 → 代码变动 → 独立 verify → Draft PR 的端到端验证。只有组织 workflow PR 合并、调用仓库 opt-in PR 合并、key 与 GitHub Actions 权限配置、E2E 实际成功后，才报告可用。
- 无自动跨仓库启用、无收费意外升级、无生产密钥或发布权限。

## 回滚

删除或禁用调用仓库的付费 caller / 收紧其 secret 授权即可阻止新付费运行，不影响既有免费 V2；无需破坏组织旧 workflow。

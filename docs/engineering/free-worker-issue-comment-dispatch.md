# GitHub Issue 原生派工入口（Free Worker V2）

状态：组织仓库调用器模板候选；**逐仓库 opt-in，不自动开放所有仓库**。

## 使用方式

仓库必须已经经过独立 PR 审查，将 `workflow-templates/sanchuang-free-worker.yml` 安装至 **默认分支**下的 `.github/workflows/sanchuang-free-worker.yml`，并正确设定 `ENROLLED=true`、工程基线及真实验证命令。现存调用器不会随组织模板改变而自动更新。

维护者在**开放的普通 Issue** 下发布一条新的、完整的 GitHub Issue 评论：

```text
/free-worker run
```

或明确指定免费模型：

```text
/free-worker run model=deepseek-v4.1-flash-free
```

`/free-worker run model=mimo-v2.6-flash-free` 等价于默认指令。指令必须占据评论全文；不允许附加任务文本、多行指令、额外参数或 API Key。任务范围只取现有 Issue 正文及经过权限核验的维护者修订评论。

使用 GitHub 连接器时，发送的是**普通 Issue 评论**，不需要也不应该从聊天转入远程电脑运行 `gh`。仅当仓库默认分支的调用器已启用 `issue_comment: created`，GitHub 才会自动接收该事件。评论成功不表示 Worker 成功；应核对 Actions Run、独立 verify、delivery 及 Draft PR。

## 信任边界与拒绝条件

- 普通 Issue 对话不触发守卫；以 `/free-worker` 开头的评论进入验证。
- 仅 `created` 事件；编辑历史评论不会触发。
- 事件 Actor、sender、comment.author 必须一致，作者必须为 GitHub `User` 而非机器人；不能依赖不可信的 `author_association`。
- 使用 GitHub Collaborator Permission API 验证该作者**当前**对目标仓库具有 `write`、`maintain` 或 `admin` 权限；API 失败即拒绝。
- 事件及实时 API 中均必须是仍 Open 的普通 Issue（不是 PR），且 Issue 正文非空；解析后的 Issue 号必须是正整数。
- 只允许三种精确的指令文本与两款官方免费模型；其余格式全部拒绝，不做 shell eval、提示词拼接或外部 URL/分支参数透传。
- `ENROLLED` 守卫、默认分支校验、工程基线守卫仍必须全部通过；额外运行 V2 不可变组织引擎自身的分支/当前提交/Issue 检查。
- `enrollment` 只有读权限；调用已固定 SHA 的 Worker V2 后继续保持模型只读、独立只读验证、交付 Runner 单独写权限的旧契约。只交 Draft PR，绝不自动合并、关 Issue、部署或发布。
- 相同 Issue 的 Worker job 使用 GitHub Actions concurrency 串行（**串行不等于永久去重**；手动 rerun 或重复发新评论仍可能产生新 Run，维护者需核对已有 PR）。
- 保留 `workflow_dispatch` 兼容入口，不删除任何既有工作流。

## 独立验收标准

1. 无关评论不产生 Worker 施工；非白名单指令、Bot、无写权限账号、PR 评论、关闭 Issue、无正文 Issue 均不能启动 Worker。
2. 已授权维护者对开放 Issue 发送精确指令后，Actions 必须有 `issue_comment` 事件 Run；守卫输出真实 Issue 号和模型，不允许未认证的评论覆盖工作流输入。
3. 真实 Run 的 `worker`、`verify`、`delivery` 独立成功，输出 Draft PR 指向可信工程基线；不出现模型环境写 Token、自动合并或环境晋级。
4. 对每个新接入业务仓库，必须检查其自身 `AGENTS.md`、现有工作流、真实验证命令并通过接入 PR；组织模板 PR 合并**不算完成业务仓库 E2E**。

参考：`docs/engineering/free-worker-onboarding.md`、`skills/dispatch-worker/SKILL.md`、`docs/engineering/external-worker.md`。

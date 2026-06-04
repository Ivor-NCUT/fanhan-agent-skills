---
name: skill-github-publisher
description: Publish newly created Agent skills to the user's GitHub skill repository. Use this skill whenever a new skill has been created with skill-creator and the user wants it uploaded, published, pushed, synced, or added to https://github.com/Ivor-NCUT/fanhan-agent-skills. It verifies local skill files, prepares README/evals when useful, commits or uploads the skill directory, and falls back to GitHub REST API if GitHub CLI or git push fails in this environment.
metadata:
  requires:
    bins: ["git", "gh", "curl"]
---

# Skill GitHub Publisher

## 目标

把新创建的 Agent skill 同步到用户的 GitHub 仓库：

```text
https://github.com/Ivor-NCUT/fanhan-agent-skills
```

这个 skill 只处理发布和同步，不负责设计 skill 内容。内容创建和修改完成后再使用。

## 输入

需要知道新 skill 的本地目录。默认位置：

```text
/Users/fanhan/.agents/skills/<skill-directory>
```

如果用户没有给路径，从最近创建或修改的 skill 目录推断。推断不稳时只问一个问题：

> 要发布的是哪个 skill 目录？

## 发布前检查

检查这些文件：

- `SKILL.md` 必须存在。
- frontmatter 至少有 `name` 和 `description`。
- 如果 skill 用法不直观，补一个简短 `README.md`。
- 如果已经有 `evals/evals.json`，确认 JSON 可解析。
- 不上传 `.DS_Store`、临时输出、大型中间文件、token、密钥或私人素材。

如果 `SKILL.md` 缺少必要字段，先修好再发布。

## 首选发布路径：本地仓库或 GitHub CLI

优先判断本地是否已有目标仓库：

```bash
find /Users/fanhan -type d -name fanhan-agent-skills -maxdepth 6 2>/dev/null
```

如果找到本地仓库：

1. 把 skill 目录复制或同步到仓库中的同名目录。
2. 查看 `git status`，确认只包含本次相关文件。
3. 提交信息使用 `add <skill-name> skill` 或 `update <skill-name> skill`。
4. 推送到远端。

如果没有本地仓库，使用 GitHub CLI 克隆或直接创建文件：

```bash
gh repo clone Ivor-NCUT/fanhan-agent-skills
```

如果 `gh` 认证正常，用常规 git 提交和 push。

## 兜底发布路径：GitHub REST API

本机曾出现过 GitHub CLI keyring token 失效、默认 DNS 路径连接 GitHub 失败的情况。遇到这些问题时，不要反复重试同一条失败命令：

- `gh auth status` 显示 token/keyring 异常。
- `gh repo clone` 或 `gh repo create` 对 `api.github.com` 返回 EOF。
- `git push` 对 `github.com:443` TLS 失败。

可行兜底是 GitHub REST API，必要时显式指定 API 主机解析：

```bash
curl --http1.1 --tlsv1.2 --resolve api.github.com:443:140.82.112.5 ...
```

使用 REST API 时：

1. 先确认可用 token 来源，不要在输出里展示完整 token。
2. 对每个要上传的文件读取当前远端 SHA；有 SHA 则更新，无 SHA 则创建。
3. 路径保持为 `<skill-directory>/<relative-file-path>`。
4. commit message 写清新增或更新的 skill。

## README 最小模板

如果需要补 README，用这个结构：

```markdown
# <skill name>

<一句话说明这个 skill 解决什么问题。>

## Files

- `SKILL.md`：skill 主说明。
- `evals/evals.json`：基础测试提示词。

## Usage

安装到 Agent skills 目录后，在相关任务中按 description 自动触发。
```

## 完成后交付

告诉用户：

- 已发布的 skill 名称。
- 本地路径。
- GitHub 仓库链接或具体目录链接。
- 使用的是常规 git/gh 还是 REST API 兜底。

## 自检清单

- 只发布本次相关 skill 文件。
- 没有上传密钥、token、私人素材或临时文件。
- 远端路径和本地目录名一致。
- README 和 evals 如存在，可正常打开。
- GitHub 链接返回给用户。


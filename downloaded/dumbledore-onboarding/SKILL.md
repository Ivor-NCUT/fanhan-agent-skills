---
name: dumbledore-onboarding
description: |
  Guide a user through installing Dumbledore into their own local folder and GitHub repository. Use this skill whenever the user says they want to install Dumbledore, onboard Dumbledore, fork or copy the framework, create their own knowledge repo, set up Dumbledore for Codex, Claude Code, OpenClaw, Manus, or another Agent, or avoid uploading their knowledge to the upstream repository.
---

# dumbledore-onboarding：安装与私有仓库初始化

你是 Dumbledore 的 onboarding 引导 Agent。你的目标是让用户拥有自己的 Dumbledore 知识库仓库，而不是把个人知识材料写入上游仓库 `Ivor-NCUT/dumbledore`。

## 核心原则

- 用户的数据应该进入用户自己的 GitHub 仓库。
- 上游仓库只作为框架模板和更新来源。
- 用户自己的 GitHub 仓库绑定为当前知识库的 `origin` remote。
- 完成绑定后，Dumbledore 在用户确认写入时会自动提交并推送最终产物。
- 优先使用一行命令完成安装；如果用户的 Agent 能操作终端，你可以直接帮用户运行。
- 如果用户没有 GitHub CLI 或未登录，给出最短的手动补救路径。
- 不要在上游仓库中录入用户的知识材料。

## 推荐一行命令

```bash
curl -fsSL https://raw.githubusercontent.com/Ivor-NCUT/dumbledore/main/install.sh | bash
```

这条命令会：

1. 下载 Dumbledore 模板。
2. 在本地创建用户自己的知识库目录。
3. 初始化 Git 仓库。
4. 如果 `gh` 已登录，引导用户创建并推送到自己的 GitHub 仓库，并把它绑定为 `origin`。

## Agent 一句话安装

当用户在 Codex、Claude Code、OpenClaw、Manus 或其他 Agent 里说：

> 帮我安装 Dumbledore，并创建我自己的 GitHub 知识库仓库。

你应该先确认当前环境是否能运行终端命令，然后执行 onboarding 流程。

## 工作流程

### Step 1：确认目标

先用一句话确认：

> 我会把 Dumbledore 复制成你自己的本地仓库，并推送到你自己的 GitHub；你的知识材料不会写入上游仓库。

如果用户只是想了解，不要运行命令。

### Step 2：检查环境

检查：

- `git`
- `curl`
- `tar`
- `gh`
- `gh auth status`

如果缺少 `gh` 或未登录，仍可创建本地仓库，并告诉用户之后如何推送。

### Step 3：运行安装

优先运行：

```bash
curl -fsSL https://raw.githubusercontent.com/Ivor-NCUT/dumbledore/main/install.sh | bash
```

如果用户希望非交互安装，可以使用：

```bash
curl -fsSL https://raw.githubusercontent.com/Ivor-NCUT/dumbledore/main/install.sh | DUMBLEDORE_DIR=~/dumbledore-knowledge DUMBLEDORE_REPO_NAME=dumbledore-knowledge DUMBLEDORE_VISIBILITY=private bash
```

### Step 4：打开新仓库

安装完成后，引导用户进入自己的仓库：

```bash
cd ~/dumbledore-knowledge
```

然后告诉用户，以后处理材料时说：

> 用 dumbledore 处理这份材料。

### Step 5：验证边界

完成后检查：

- 当前仓库 remote 是否指向用户自己的 GitHub 仓库。
- `origin` 不应指向 `https://github.com/Ivor-NCUT/dumbledore.git`，除非用户明确是在维护上游框架。
- `skills/dumbledore/SKILL.md` 存在。
- `AGENTS.md` 存在。
- `scripts/publish.sh` 存在且可执行。

### Step 6：说明自动发布

告诉用户：

> 以后你确认写入后，Dumbledore 会把分析出的知识、SOP、脚本建议和 skill 建议写入本地文件，然后自动提交并推送到这个绑定的 GitHub 仓库。

如果用户不想自动推送，必须在任务开始前明确说“只写本地，不推送”。

## 常见情况

### 用户没有 GitHub CLI

告诉用户先安装并登录：

```bash
brew install gh
gh auth login
```

然后在本地仓库里运行：

```bash
gh repo create dumbledore-knowledge --private --source=. --remote=origin --push
```

### 用户已经有自己的仓库

不要覆盖。引导用户选择一个空目录，或把 Dumbledore 作为新仓库初始化后再手动迁移旧内容。

### 用户想 fork 上游仓库

说明 fork 可以用于贡献框架，但不推荐用 fork 保存私人知识。私人知识库应该是一个新的 private repo。

## 完成汇报

完成后用简短中文说明：

- 本地路径。
- GitHub 仓库地址。
- 是否为 private。
- 是否已绑定为 `origin`。
- 以后如何触发 Dumbledore。

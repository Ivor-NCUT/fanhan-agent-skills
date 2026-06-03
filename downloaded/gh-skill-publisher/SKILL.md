---
name: gh-skill-publisher
description: Use this skill whenever the user asks Codex to create a GitHub repository, publish a local skill or folder to GitHub, push current work to a new repo, or avoid manually creating a repo in the GitHub web UI. It handles GitHub CLI auth checks, repo creation, local git setup, commit, remote wiring, push, and return of the final repo URL.
---

# GitHub Skill Publisher

Use this skill when the user wants a conversational workflow for creating a GitHub repository and pushing local files, especially Codex skills, without opening GitHub manually.

## Guardrails

- Never ask the user to paste a GitHub token into chat.
- Never write a PAT, API key, or OAuth token into a skill, repository, shell history, README, or committed file.
- Prefer `GH_TOKEN` from the environment or an already-valid `gh` login.
- If authentication is missing or invalid, stop after explaining the exact missing prerequisite and give the minimal command the user can run locally.
- Creating PATs, OAuth apps, deploy keys, or other persistent credentials in a browser is high risk. Ask the user to do that step themselves.
- Before pushing, inspect the working tree. Do not overwrite, reset, delete, or discard user changes.
- Before creating a public repo, confirm visibility if the user did not explicitly request public.

## Required Inputs

If missing, ask one question at a time:

- Target GitHub repo, in `owner/repo` format or a repo name for the authenticated user.
- Local source path to publish. Default to current directory if the user says "current folder" or does not name another path.
- Visibility. Default to private unless the user explicitly says public.
- Commit message. Default to `chore: publish initial files` for generic folders, or `feat: publish <skill-name> skill` for skill folders.

## Workflow

### 1. Check tools and auth

Run:

```bash
gh --version
gh auth status
```

If `gh auth status` fails, check whether `GH_TOKEN` exists without printing it:

```bash
test -n "$GH_TOKEN" && echo "GH_TOKEN is set" || echo "GH_TOKEN is missing"
```

If `GH_TOKEN` is set, authenticate non-interactively:

```bash
printf '%s' "$GH_TOKEN" | gh auth login --with-token
```

If neither login nor `GH_TOKEN` works, tell the user:

```bash
export GH_TOKEN="your_github_pat_here"
printf '%s' "$GH_TOKEN" | gh auth login --with-token
```

Do not proceed until authentication is valid.

### 2. Inspect local source

Run from the source directory:

```bash
pwd
git status --short
git remote -v
```

If the folder is not a git repo:

```bash
git init
```

If the user wants to publish a skill folder, verify the skill has a `SKILL.md` file before pushing.

### 3. Create or reuse the GitHub repo

Use private by default:

```bash
gh repo view OWNER/REPO >/dev/null 2>&1 || gh repo create OWNER/REPO --private --source=. --push=false
```

For public repos, only use `--public` when the user explicitly requested public or confirmed it.

If the repository already exists, continue by wiring the remote.

### 4. Wire the remote

Prefer HTTPS remotes for `gh`/token compatibility:

```bash
git remote get-url origin
```

If `origin` is missing:

```bash
git remote add origin https://github.com/OWNER/REPO.git
```

If `origin` exists but points somewhere else, do not overwrite it silently. Explain the current remote and ask whether to replace it or add a new remote name.

### 5. Commit and push

Only commit the intended files. For a whole-folder initial publish:

```bash
git add .
git commit -m "chore: publish initial files"
git branch -M main
git push -u origin main
```

If there is nothing to commit, push the existing branch:

```bash
git branch --show-current
git push -u origin HEAD
```

### 6. Return the result

Return:

- GitHub repo URL.
- What was created or reused.
- What branch was pushed.
- Any system maintenance recommendation, such as whether this workflow should be added to a team SOP.

## Common Prompts

User: "把这个 skill 推到 GitHub，仓库叫 Ivor-NCUT/codex-skills。"

Action: Check auth, verify `SKILL.md`, create/reuse `Ivor-NCUT/codex-skills`, commit and push.

User: "帮我创建一个私有仓库，把当前目录推上去。"

Action: Ask for the repo name, because it is the only missing required input.

User: "以后别让我手动去 GitHub 新建仓库了。"

Action: Explain that `gh repo create` can do this through Codex after `GH_TOKEN` or `gh auth login` is valid, then offer to run the current repo publish flow.

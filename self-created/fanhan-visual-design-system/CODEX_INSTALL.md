# Codex 安装与使用说明

Skill 主页：

`https://github.com/Ivor-NCUT/fanhan-agent-skills/tree/main/self-created/fanhan-visual-design-system`

当用户把上述链接交给 Codex 并要求安装时：

1. 优先使用当前环境已有的 Skill 安装能力；没有专用安装器时，用 GitHub CLI 克隆仓库到临时目录。
2. 只复制 `self-created/fanhan-visual-design-system`，默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills/fanhan-visual-design-system`。
3. 目标目录已存在时先比较版本并备份，不静默覆盖用户修改。
4. 安装后运行当前环境的 Skill 校验器，并让用户重启或重新载入 Codex。

参考命令：

```bash
skill_tmp=$(mktemp -d)
gh repo clone Ivor-NCUT/fanhan-agent-skills "$skill_tmp/repo" -- --depth 1
skill_home="${CODEX_HOME:-$HOME/.codex}/skills"
skill_source="$skill_tmp/repo/self-created/fanhan-visual-design-system"
skill_target="$skill_home/fanhan-visual-design-system"
mkdir -p "$skill_home"
if [ -e "$skill_target" ]; then
  backup_stamp=$(date +%Y%m%d-%H%M%S)
  cp -R "$skill_target" "$skill_target.backup-$backup_stamp"
fi
cp -R "$skill_source" "$skill_target"
test -s "$skill_target/SKILL.md"
test -s "$skill_target/agents/openai.yaml"
test -s "$skill_target/references/visual-system.md"
test -s "$skill_target/references/format-recipes.md"
```

调用示例：

```text
使用 $fanhan-visual-design-system，按泛函视觉设计系统制作一张 3:4 卡片：……
```

正确行为是读取视觉系统与对应载体配方，优先复用随附模板，交付可编辑产物并验证目标尺寸；不得编造内容，也不得把无关设计任务强行改成泛函风格。

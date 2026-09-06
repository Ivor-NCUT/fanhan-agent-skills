# Codex 安装与使用说明

Skill 主页：

`https://github.com/Ivor-NCUT/fanhan-agent-skills/tree/main/self-created/fanhan-personal-site-updater`

当用户把上述链接交给 Codex 并要求安装时，按以下方式处理。

## 安装

1. 优先使用当前环境已有的 Skill 安装能力；没有专用安装器时再使用下面的 GitHub CLI 方案。
2. 将仓库克隆到临时目录，只复制目标 Skill。不要把整个合集安装进自动发现目录。
3. 默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills/fanhan-personal-site-updater`。
4. 若目标目录已存在，先比较版本并创建带时间戳的备份；不得静默覆盖用户修改。
5. 安装后检查 `SKILL.md`、`agents/openai.yaml` 与 `references/intake-templates.md` 都存在，再运行当前环境的 Skill 校验器。

参考命令：

```bash
skill_tmp=$(mktemp -d)
gh repo clone Ivor-NCUT/fanhan-agent-skills "$skill_tmp/repo" -- --depth 1
skill_home="${CODEX_HOME:-$HOME/.codex}/skills"
skill_source="$skill_tmp/repo/self-created/fanhan-personal-site-updater"
skill_target="$skill_home/fanhan-personal-site-updater"
mkdir -p "$skill_home"
if [ -e "$skill_target" ]; then
  backup_stamp=$(date +%Y%m%d-%H%M%S)
  cp -R "$skill_target" "$skill_target.backup-$backup_stamp"
fi
cp -R "$skill_source" "$skill_target"
test -s "$skill_target/SKILL.md"
test -s "$skill_target/agents/openai.yaml"
test -s "$skill_target/references/intake-templates.md"
```

安装完成后让用户重启或重新载入 Codex，使新 Skill 出现在可用列表中。

## 使用

调用示例：

```text
使用 $fanhan-personal-site-updater 更新泛函个人网站。
```

未指定栏目时，先显示七个栏目菜单并等待选择；已指定栏目时，直接读取该栏目的资料模板。用户可以发自然语言、链接和图片，不要求重抄字段。

## 不可越过的边界

- 只修改七个编辑型栏目；公司、岗位、岗位数据与同步逻辑由百纯维护。
- “预览、草稿、先看看”不得推送或部署。
- “更新、上线、发布”可按目标仓库既有流程提交、同步和部署，但删除或替换已有条目仍需明确意图。
- 不编造事实，不公开未经用户明确授权的联系方式或私密素材。

## 安装后自检

让 Skill 响应下面的请求：

```text
使用 $fanhan-personal-site-updater，我想更新个人网站，但还没决定栏目。
```

正确行为是只列出七个栏目供选择，不修改网站，也不询问公司或岗位信息。

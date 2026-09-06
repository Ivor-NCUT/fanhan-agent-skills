---
name: skill-github-publisher
description: 将已完成的新建或更新 Skill 发布到用户指定的 GitHub 仓库。用于明确发布请求或已有匹配的长期发布授权；先验证范围、许可和私有材料，再通过 gh 或 gh api 发布并回读。
metadata:
  requires:
    bins: ["git", "gh"]
---

# Skill GitHub Publisher

默认目标为 `Ivor-NCUT/fanhan-agent-skills`；用户指定目标优先。此入口只处理发布，不承担重新设计或全套教程交付。

1. 从当前任务确定 Skill 目录、目标路径和授权范围。只有无法确认是哪份成果时才询问；已明确授权不再次询问是否发布。
2. 验证 `SKILL.md`、相关脚本／引用和已有 evals。检查许可证与公开范围；排除密钥、私有材料、临时产物和依赖目录。缺少可公开依据只暂停发布，继续完成本地成果。
3. 查现有工作区和仓库状态，保留用户未提交改动。只发布本任务文件；README 与示例仅在使用需要时补充。
4. GitHub 远端全部通过 `gh`／`gh api`；克隆用 `gh repo clone`，查询用 `gh repo view`、`gh api`。本地提交和差异检查可用 `git`，不直接执行 git 网络命令。
5. 发布文件时，优先复用仓库已有合规发布工具；否则用 `gh api` 的 Git Database blobs → tree → commit → ref 更新，基于读取的目标分支 head 构建一次完整变更，保留所有非目标文件。使用结构化参数／JSON 文件，不拼接 shell 字符串，不强制更新 ref。
6. 并发导致 head 改变时重新读取、保留双方意图再构建；超时先核对远端 commit/tree 和文件内容，已成功则不重复提交。需要 PR 时通过 `gh pr create`，是否合并服从已有授权与仓库规则。
7. 回读目标路径、提交及文件内容，确认与本次成果一致后交付链接。认证或权限阻塞时说明具体缺项，不能用 curl、固定 IP、SDK 或其他身份绕过。

最终说明已发布内容、目标链接与验证；未完成发布则明确本地已完成和远端阻塞，不把提交成功等同于目标交付。

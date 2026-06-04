---
name: skill-迭代工作流
description: Agent skill 迭代工作流。Use this skill whenever the user says a skill output is satisfactory, approved, finalized, “这一版满意了”, “按这个版本沉淀”, “更新到 skill”, “把刚才反馈写进能力包”, or asks to improve the original skill based on the current conversation. It identifies the skill used at the start of the work, extracts feedback, invokes 达尔文 skill when available, updates the original SKILL.md, and preserves a testable change record.
metadata:
  requires:
    skills: ["达尔文skill", "skill-creator"]
---

# Skill 迭代工作流

## 目标

当用户已经通过多轮反馈确认某个 skill 的产出可用，把这轮对话里的有效经验沉淀回原 skill。

这个 skill 处理“从满意版本回写能力包”的动作。它不用于新建 skill；新建仍使用 `skill-creator`。它也不用于普通内容修改，只有用户明确要把经验沉淀进能力包时才接管。

## 触发判断

使用本 skill 需要同时满足两点：

- 本轮或最近一轮工作中使用过某个 Agent skill。
- 用户表达了满意、确认或要求沉淀，例如“这版可以了”“我满意了”“就按这个写进 skill”“把这些反馈更新进去”。

如果用户只是说“继续改”“还不行”“这版不满意”，不要更新 skill。继续按当前任务迭代产出。

## 工作流程

### 1. 定位原始 skill

从当前对话中找出最初用于工作的 skill：

- 用户显式点名的 skill 优先级最高。
- 如果多个 skill 参与，选择负责主要产出的那个。
- 如果只是辅助工具 skill，例如文件读取、飞书上传，不要把它当作要迭代的对象。

找不到原始 skill 时，只问一个问题：

> 这次要把反馈沉淀到哪个 skill？

### 2. 提取可沉淀反馈

只提取能复用的内容：

- 用户明确指出的问题。
- 用户认可的版本相对前一版的变化。
- 反复出现的偏好。
- 任务中的关键边界，例如不要做什么、必须保留什么、输出格式如何。
- 可转成检查清单、流程分支、反例或触发描述的经验。

不要沉淀这些内容：

- 一次性素材、临时标题、具体客户隐私。
- 未验证的猜测。
- 和该 skill 无关的闲聊。
- 用户没有确认满意的中间版本。

### 3. 调用达尔文 skill

如果 `达尔文skill` 可用，读取它并按其流程优化原 skill。把本轮反馈作为输入，重点让达尔文处理：

- frontmatter 描述是否需要增加触发词。
- 工作流是否缺少失败分支。
- 自检清单是否覆盖这次踩到的问题。
- 反模式清单是否需要新增。
- 是否需要增加 eval prompt。

如果达尔文 skill 不可用，使用 `skill-creator` 的改进原则手动更新，但要在最终说明里写明没有调用达尔文。

### 4. 编辑原 skill

编辑前先读取原 `SKILL.md`，保留原有 name、目录名和核心定位。

优先做小范围改动：

- 更新 description 的触发场景。
- 增加“不要做什么”的反模式。
- 增加一个步骤或检查点。
- 补充 1-3 个测试 prompt。

不要把整段聊天记录塞进 `SKILL.md`。把反馈抽象成可复用规则。

### 5. 验证

至少做这些检查：

- `SKILL.md` frontmatter 仍可解析。
- name 没有被误改。
- 新增规则能解释这次满意版本为什么更好。
- 没有加入敏感信息、临时素材或过窄例子。

如果已有 evals，增加或调整最相关的 1-3 条。用户没有要求完整评测时，不强制跑大规模 benchmark。

## 交付格式

完成后告诉用户：

- 更新了哪个 skill。
- 改了哪几类规则。
- 是否调用了达尔文 skill。
- 是否新增测试用例。
- 本地路径。

示例：

```markdown
已把这轮反馈沉淀到 `/Users/fanhan/.agents/skills/xxx/SKILL.md`。
这次调用了「达尔文 skill」，主要更新了触发描述、反模式和交付前自检，并新增 2 条 eval。
```

## 自检清单

- 是否定位到本轮最初的主要 skill。
- 是否只沉淀用户已经认可的经验。
- 是否调用达尔文 skill，或明确说明不可用。
- 是否保留原 skill 名称和定位。
- 是否避免写入隐私、token、临时素材。
- 是否留下后续可测试的 eval 或检查点。


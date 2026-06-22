---
name: 候选人入库@泛函
description: 将候选人投递邮件、简历解析结果和作品集解析结果写入指定飞书多维表格的「候选人」数据表。Use this skill whenever the workflow has classified an email as candidate_submission, needs to ingest a candidate into Lark/Feishu Base, write parsed resume/portfolio information to the candidate database, upload resume or portfolio attachments to Base attachment fields, deduplicate by email/source mail ID, or update an existing candidate record.
---

# 候选人入库@泛函

## 目标

当「邮件智能分类入库@泛函」判断邮件为 `candidate_submission` 后，先调用「简历 + 作品集文本解析@泛函」解析简历和作品集，再把解析后的候选人信息写入飞书多维表格「候选人」数据表。

本 skill 不负责读取邮箱，不负责解析简历正文；它负责把已经读取/解析出的信息可靠写入 Base。

## 先读参考

执行前读取：

- `references/base-config.md`：真实 Base、表、字段、字段类型和字段映射。
- `references/write-protocol.md`：去重、创建/更新、附件上传和失败处理。

## 固定目标

- Base 名称：`泛函｜公司&职位&候选人`
- Base URL: `https://twoj0037lkv.feishu.cn/base/A80Xb9jOnaexcKswFkacPBoEnAf?table=tbldGJk6awx45Chc&view=vewjTTaw3N`
- Base token: `A80Xb9jOnaexcKswFkacPBoEnAf`
- 表名：`候选人`
- Table ID: `tbldGJk6awx45Chc`

## 输入

期望输入来自上游 workflow：

```text
classification:
  primary_category: candidate_submission
mail:
  subject:
  from:
  body:
  source_mail_id:
attachments:
  resume_files:
    - local path or filename
  portfolio_files:
    - local path or filename
candidate_parse:
  candidate_parse.json
  candidate_parse.md
```

如果 `classification.primary_category` 不是 `candidate_submission`，不要写候选人表，返回“分类不匹配”并建议调用对应入库 skill。

## 前置检查

1. 检查飞书授权：

```bash
lark-cli auth status --verify
```

2. 读取真实字段结构，不要凭记忆写：

```bash
lark-cli base +field-list \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --as user
```

3. 只写存储字段。不要写 `今日时间` 这类公式字段；附件字段必须用 `+record-upload-attachment`。

## 入库流程

### 1. 调用解析 skill

如果还没有结构化候选人解析结果，先调用「简历 + 作品集文本解析@泛函」，拿到：

- 候选人姓名、邮箱、微信号、求职类型。
- 邮件正文摘要。
- 简历文本提取。
- 简历及作品集解析 Markdown。
- 简历文件名、补充材料文件名。
- 本地附件路径。

### 2. 去重

按顺序查重：

1. `来源邮件ID`
2. `邮箱`
3. `姓名 & 昵称`

命中唯一记录时更新该记录；没有命中时创建新记录；命中多条时停止写入并返回人工复核。

### 3. 写普通字段

用 `lark-cli base +record-upsert` 写普通字段。不要把附件字段放进普通 JSON。

示例：

```bash
lark-cli base +record-upsert \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --json '{"姓名 & 昵称":"张三","邮箱":"zhangsan@example.com","实习 & 正职":"实习","来源邮件ID":"mail_xxx","邮件正文摘要":"...","简历文件名":"zhangsan.pdf","补充材料文件名":"portfolio.pdf","简历文本提取":"...","简历及作品集解析":"...","数据清洗":"候选人入库@泛函 已入库"}' \
  --as user
```

更新已有记录时增加 `--record-id <record_id>`。

### 4. 上传附件

记录创建或更新成功后，再上传附件：

```bash
lark-cli base +record-upload-attachment \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --record-id <record_id> \
  --field-id fldEJ0bz4j \
  --file /path/to/resume.pdf \
  --as user
```

作品集/补充材料上传到 `fldZxaqQl9`。

如果只有文件名没有本地路径，只写文件名字段，不上传附件。

## 输出

完成后输出：

```markdown
已完成候选人入库

Base：
- 泛函｜公司&职位&候选人 / 候选人

记录：
- record_id:
- 操作：created|updated|skipped|needs_review

写入字段：
- [字段清单]

附件：
- 简历：[uploaded/skipped + 原因]
- 作品集/补充材料：[uploaded/skipped + 原因]

后续：
- [是否需要人工补字段、去重确认或调用其他流程]
```

## 禁止行为

- 不读取邮箱。
- 不把候选人原始附件、解析缓存、token、cookie 提交进仓库。
- 不写公式字段、只读字段或附件字段的普通 CellValue。
- 不在多条疑似重复记录中自行合并。
- 不把未知的 `实习 & 正职` 选项写成新选项；无法判断时写 `不确定`。


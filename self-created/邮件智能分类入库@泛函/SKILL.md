---
name: 邮件智能分类入库@泛函
description: 对上游已经读取出的邮件标题、正文和附件信息进行智能分类，并产出可入库的 JSON + Markdown。Use this skill whenever the user asks to classify recruiting-related emails, triage candidate submissions, identify hiring company demand, recognize headhunter partners, recognize ecosystem partner referrals, or prepare email-derived records for later candidate/company/partner database ingestion. It does not read mailboxes; it classifies already-provided email content and records evidence, confidence, recommended routing, and follow-up actions.
---

# 邮件智能分类入库@泛函

## 目标

把上游已经读取出的邮件材料分类成可入库记录。输入是邮件标题、正文、附件名称/摘要/文件路径，以及上游已经抽取出的附件文本；本 skill 不负责读取邮箱，也不负责配置发信能力。

第一版输出两份：

- `email_classification.json`：给后续入库、自动化路由、Manus 发信或任务流使用。
- `email_classification.md`：给人复核分类依据、置信度和建议动作。

## 先读参考

- `references/taxonomy.md`：分类定义、判断证据和冲突处理。
- `references/output-schema.md`：JSON 和 Markdown 输出结构。

## 输入边界

期望输入：

```text
mail_subject: 邮件标题
mail_body: 邮件正文
from: 发件人，可选
to: 收件人，可选
cc: 抄送人，可选
attachments:
  - 文件名、文件类型、摘要、解析文本或本地路径
extracted_context:
  - 上游已经抽取出的简历、JD、公司介绍、推荐说明等文本
```

不要调用邮箱读取命令。若用户只给邮箱 message_id，说明需要上游先读取标题、正文和附件内容。

## 分类

主分类：

1. `candidate_submission`：候选人投递。候选人把简历或作品发来，希望匹配合适岗位。
2. `hiring_company`：需要招聘的公司。公司或招聘负责人发来岗位要求，希望匹配候选人。
3. `headhunter_partner`：猎头伙伴。其他猎头、招聘合作方、RPO 或招聘服务方希望交换职位/候选人/合作。
4. `ecosystem_referral`：生态伙伴推荐。朋友、合作伙伴、投资人、社群伙伴等转介绍候选人或招聘需求。

兜底分类：

- `other`：不属于以上主类，或只是普通抄送、通知、闲聊、系统邮件。
- `needs_review`：信息不足、多类证据冲突，或分类会影响重要动作时需要人工判断。

如果邮件只是抄送给 `fanhan@aimanziyi.vip`，且没有明确候选人、岗位、猎头合作或转介绍意图，归为 `other`。

## 判断流程

### 1. 建立证据

先从标题、正文、附件名、附件摘要里提取证据：

- 是否出现简历、求职、投递、候选人自荐、作品集、个人介绍。
- 是否出现 JD、岗位、招聘需求、公司介绍、预算、HC、到岗时间。
- 是否出现猎头、人才推荐、职位合作、候选人交换、佣金、合作协议。
- 是否出现朋友推荐、生态伙伴、转介绍、帮忙看看、推荐给你、资源对接。
- 是否只有抄送、通知、会议、账单、系统提醒、无招聘上下文。

### 2. 分类并打置信度

输出一个主分类和可选候选分类：

- `confidence`: 0-1。
- `evidence`: 支撑分类的原文片段或附件线索。
- `negative_evidence`: 为什么不是其他类。
- `needs_human_review`: 是否需要人工复核。

不要只靠关键词。比如“推荐一个人”可能是候选人投递，也可能是生态伙伴推荐；要看发件人身份、语气和请求对象。

### 3. 生成入库动作

只给建议，不直接发信：

- `create_candidate_record`
- `create_company_demand_record`
- `create_partner_record`
- `create_referral_record`
- `ignore_or_archive`
- `manual_review`

如果需要后续发邮件，把建议写成 `recommended_email_action`，具体发信由 Manus 或上游邮件能力处理。

## 入库字段提取

按分类提取最小字段：

- 候选人：姓名、邮箱、电话、目标岗位、所在地、简历/作品附件、候选人摘要。
- 招聘公司：公司名、岗位名、JD 摘要、地点、薪资/预算、招聘负责人、候选人要求。
- 猎头伙伴：伙伴姓名/机构、合作诉求、提供的职位/候选人、合作方式、联系方式。
- 生态伙伴推荐：推荐人、被推荐对象、推荐关系、推荐理由、后续建议。

缺失字段保留为空，不要编造。

## 冲突处理

- 同时有简历和 JD：如果发件人是在自荐并附简历，优先 `candidate_submission`；如果发件人代表公司招人并附候选人样例，优先 `hiring_company` 或 `headhunter_partner`。
- 公司 HR 发候选人：如果语义是“帮忙看看这个候选人”，优先 `ecosystem_referral`；如果语义是“我们要招这个岗位”，优先 `hiring_company`。
- 猎头发 JD：如果重点是“合作/帮我推人/互换资源”，优先 `headhunter_partner`；如果明确代表甲方公司招聘，可候选分类包含 `hiring_company`。
- 只是抄送 `fanhan@aimanziyi.vip` 且无明确诉求：`other`。

## 完成回复

```markdown
已完成：[邮件标题] 分类

分类：
- 主分类：[category]
- 置信度：[confidence]
- 是否需复核：[yes/no]

输出：
- JSON: [路径]
- Markdown: [路径]

建议动作：
- [recommended_action]
```


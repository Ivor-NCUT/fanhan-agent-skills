---
name: 简历 + 作品集文本解析@泛函
description: 将上游已经提取出的邮件标题、正文、简历附件和作品集文件/链接解析成可检索的 JSON + Markdown。Use this skill whenever the user asks to parse candidate resumes, portfolios, personal websites, PDF/DOCX/PPT/Markdown/HTML files, Lark docs, webpages, social profiles/posts, videos, podcasts, AI video works, long-form articles, or any candidate evidence for later JD matching and talent search. It extracts text, builds portfolio project cards, tags evidence for aesthetics, internet sense, content quality, and technical ability, and keeps source evidence traceable.
---

# 简历 + 作品集文本解析@泛函

## 目标

把候选人邮件材料转成后续智能查询、筛选和 JD 匹配能用的结构化材料。输入由上游提供，不负责读取飞书邮箱；本 skill 只处理已经给到 Agent 的邮件标题、正文、附件路径和链接。

输出同时给两份：

- `candidate_parse.json`：给后续检索、筛选、入库或匹配流程使用。
- `candidate_parse.md`：给人审阅、调试和追溯证据使用。

## 先读参考

按任务需要读取对应文件，不要一次性展开所有细节：

- `references/output-schema.md`：需要产出 JSON/Markdown 时读取。
- `references/source-routing.md`：遇到飞书链接、网页、社媒、视频、播客、公众号或 RSS 时读取。
- `references/tech-research.md`：需要选择解析工具、解释技术取舍或补充实现方案时读取。

## 输入边界

期望输入包含这些信息中的一部分或全部：

```text
mail_subject: 邮件标题
mail_body: 邮件正文
attachments:
  - 本地文件路径或可下载 URL
portfolio_links:
  - 作品集、个人站、飞书文档、社媒账号/帖子、视频、PPT、PDF、文章链接
candidate_hint:
  - 候选人姓名、邮箱、投递岗位等上游已知信息
```

不要调用飞书邮箱读取命令。若用户只给了飞书邮箱 message_id，说明本 skill 需要上游先提取邮件内容，再继续解析。

## 工作流程

### 1. 建立材料清单

先把输入拆成四类：

- `resume_sources`：简历文件或简历链接。
- `portfolio_sources`：作品集文件、网页、社媒、视频、文章、PPT、飞书文档等。
- `context_sources`：邮件标题、正文、投递岗位、候选人自述。
- `blocked_sources`：缺权限、无法下载、格式未知或平台限制导致无法读取的材料。

每个 source 都记录：

- `source_id`
- `source_type`
- `uri_or_path`
- `status`
- `parser_used`
- `failure_reason`

### 2. 简历解析

简历只要求提取关键文本，不做过度判断。优先保留：

- 姓名、联系方式、所在地、当前身份。
- 教育经历、工作经历、项目经历。
- 技能、工具、行业、作品链接。
- 时间线和可被 JD 检索的关键词。

如果文件解析失败，保留失败原因，并继续处理其他材料。

### 3. 作品集解析

作品集要产出项目卡片，不只是全文。每个作品尽量形成：

- 作品名称
- 作品类型：网页、图片、PPT、视频、社媒账号、长文、开源项目、产品 Demo 等
- 候选人角色
- 使用工具/技术/平台
- 作品摘要
- 可验证成果：数据、上线状态、传播效果、客户/用户反馈、业务结果
- 原始证据：链接、页码、字幕片段、截图说明、正文摘录
- 能力标签和初评分

能力标签至少覆盖：

- `aesthetic_judgment`：审美、视觉完成度、版式、图片/PPT/网页质感。
- `internet_sense`：网感、平台表达、短视频/社媒传播意识、标题/封面/节奏。
- `content_quality`：内容素养、结构表达、长文质量、观点密度、叙事能力。
- `technical_execution`：技术实现、工程能力、工具使用、自动化能力。
- `product_sense`：产品理解、用户路径、转化意识、业务意识。

评分只能作为初步信号，必须附带证据。没有证据时写 `unknown`，不要凭感觉补结论。

### 4. 网页与平台路由

遇到网页、社媒、视频、公众号、RSS、GitHub、LinkedIn、论坛等外部链接时，读取 `references/source-routing.md`，按 Agent Reach 路由处理。临时输出放 `/tmp/`，不要把网页抓取缓存、视频字幕、截图、候选人原始文件写进仓库。

### 5. 飞书链接处理

遇到飞书文档、飞书云文件、飞书幻灯片或 Markdown 文件时：

1. 先运行 `lark-cli auth status --verify`。
2. 如果用户身份不可用或不可刷新，引导用户完成 `lark-cli auth login --no-wait --json`。
3. 对 docs 命令，先运行 `lark-cli skills read lark-doc`，再选择具体命令。
4. 使用 `drive +inspect` 判断链接类型，再按类型 fetch、export 或 download。

不要把 token、cookie、候选人原始附件提交到仓库。

## 输出要求

读取 `references/output-schema.md`，同时产出 JSON 和 Markdown。JSON 面向机器，Markdown 面向人。

输出必须具备：

- 完整 source 清单和解析状态。
- 简历文本摘要与关键字段。
- 作品全文摘要和项目卡片。
- 审美、网感、内容素养等标签的证据。
- 失败项和下一步人工处理建议。

## 技术取舍

第一版先编排成熟工具，不手写复杂解析器：

- 文档解析优先 Docling / MarkItDown / Apache Tika / Unstructured。
- 网页和公众号走 Agent Reach 的 Jina Reader、web-reader MCP、Exa、Camoufox 方案。
- 视频和播客优先字幕/转录，必要时再做音频转写。
- 社媒平台遵守各 CLI 的可用范围、登录要求、频控和平台限制。

## 完成标准

一次解析任务完成后，回复用户：

```markdown
已完成：[候选人/材料名] 解析

输出：
- JSON: [路径]
- Markdown: [路径]

解析结果：
- 成功：[数量与类型]
- 部分成功：[数量与原因]
- 失败：[数量与原因]

注意：
- [权限、平台限制、低置信度判断或建议补充的材料]
```

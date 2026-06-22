# Base 配置与字段映射

## 已验证 Base

- Base 名称：`泛函｜公司&职位&候选人`
- Base token：`A80Xb9jOnaexcKswFkacPBoEnAf`
- Base URL：`https://twoj0037lkv.feishu.cn/base/A80Xb9jOnaexcKswFkacPBoEnAf`
- 表名：`候选人`
- Table ID：`tbldGJk6awx45Chc`
- 验证时间：2026-06-22
- 读取身份：`--as user`

## 已验证候选人表字段

| 字段名 | 字段 ID | 类型 | 写入方式 |
|---|---|---|---|
| 姓名 & 昵称 | fldIoKxadg | text | 普通字段 |
| 邮箱 | fldibROToK | text(email style) | 普通字段 |
| 微信号 | fld4uE9uIy | text | 普通字段 |
| 实习 & 正职 | fldw5Z7M1e | select | 普通字段，选项见下方 |
| 来源邮件ID | fldR8kLg84 | text | 普通字段 |
| 邮件正文摘要 | fldSn5gz63 | text | 普通字段 |
| 简历文件名 | fldxjj7RB1 | text | 普通字段 |
| 补充材料文件名 | fldSJ2U6Br | text | 普通字段 |
| 简历文本提取 | fldxVn4CsP | text | 普通字段 |
| 简历及作品集解析 | fldEQ2YSBC | text | 普通字段 |
| 数据清洗 | fldjrmUsyz | text | 普通字段 |
| 是否入职 | fld3VT44cs | checkbox | 默认不写，除非用户明确要求 |
| 备注一下是哪门课的学习助理 | fldRIaGGc9 | text | 默认不写，除非材料明确相关 |
| 今日时间 | flda6S7aWT | formula | 只读，不写 |
| 简历 | fldEJ0bz4j | attachment | 用附件命令上传 |
| 作品集/补充材料 | fldZxaqQl9 | attachment | 用附件命令上传 |

## `实习 & 正职` 选项

只能写以下选项：

- `实习`
- `正职`
- `不确定`

判断规则：

- 明确投实习、实习生、intern：写 `实习`。
- 明确全职、正职、社招、正式岗位：写 `正职`。
- 同时可实习/正职、材料不清楚、只写“找机会”：写 `不确定`。

## 推荐字段映射

| 来源 | 目标字段 |
|---|---|
| `candidate.name` | `姓名 & 昵称` |
| `candidate.email` | `邮箱` |
| `candidate.wechat` / 邮件正文提取 | `微信号` |
| 求职类型判断 | `实习 & 正职` |
| `mail.source_mail_id` | `来源邮件ID` |
| 邮件正文摘要 | `邮件正文摘要` |
| 简历附件文件名 | `简历文件名` |
| 作品集/补充材料文件名 | `补充材料文件名` |
| 简历纯文本 | `简历文本提取` |
| `candidate_parse.md` 或等价 Markdown | `简历及作品集解析` |
| 入库流程说明 | `数据清洗` |

## 字段结构复核命令

```bash
lark-cli base +field-list \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --as user
```


# 写入协议

## 1. 授权检查

```bash
lark-cli auth status --verify
```

如果 user 身份不可用或 scope 不足，先处理授权，不要降级为 bot 盲写用户资源。

## 2. 去重查询

`+record-upsert` 不会按业务键自动 upsert，必须先查记录。

优先顺序：

1. 有 `source_mail_id`：查 `来源邮件ID`。
2. 有邮箱：查 `邮箱`。
3. 有姓名：查 `姓名 & 昵称`。

示例：

```bash
lark-cli base +record-search \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --keyword "candidate@example.com" \
  --search-field "邮箱" \
  --field-id "姓名 & 昵称" \
  --field-id "邮箱" \
  --field-id "来源邮件ID" \
  --limit 10 \
  --format json \
  --as user
```

处理结果：

- 0 条：创建新记录。
- 1 条：更新该记录。
- 多条：停止写入，输出 `needs_review`，让用户确认合并对象。

## 3. 普通字段写入

创建：

```bash
lark-cli base +record-upsert \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --json '{"姓名 & 昵称":"张三","邮箱":"zhangsan@example.com","数据清洗":"候选人入库@泛函：由邮件分类与简历作品集解析结果入库。"}' \
  --as user
```

更新：

```bash
lark-cli base +record-upsert \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --record-id <record_id> \
  --json '{"姓名 & 昵称":"张三","邮箱":"zhangsan@example.com","数据清洗":"候选人入库@泛函：由邮件分类与简历作品集解析结果入库。"}' \
  --as user
```

实际字段较长时，可以先在 `/tmp/candidate-fields.json` 生成 payload，再用 shell 展开传入：

```bash
lark-cli base +record-upsert \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --json "$(cat /tmp/candidate-fields.json)" \
  --as user
```

`/tmp/candidate-fields.json` 内容示例：

```json
{
  "姓名 & 昵称": "张三",
  "邮箱": "zhangsan@example.com",
  "微信号": "zhangsanwx",
  "实习 & 正职": "实习",
  "来源邮件ID": "mail_xxx",
  "邮件正文摘要": "候选人自荐 AI 产品实习岗位，附件包含简历和作品集。",
  "简历文件名": "zhangsan_resume.pdf",
  "补充材料文件名": "portfolio.pdf",
  "简历文本提取": "简历正文...",
  "简历及作品集解析": "候选人解析 Markdown...",
  "数据清洗": "候选人入库@泛函：由邮件分类与简历作品集解析结果入库。"
}
```

## 4. 附件上传

普通字段写入成功后，拿返回的 `record_id` 上传附件。

简历：

```bash
lark-cli base +record-upload-attachment \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --record-id <record_id> \
  --field-id fldEJ0bz4j \
  --file /path/to/resume.pdf \
  --as user
```

作品集/补充材料：

```bash
lark-cli base +record-upload-attachment \
  --base-token A80Xb9jOnaexcKswFkacPBoEnAf \
  --table-id tbldGJk6awx45Chc \
  --record-id <record_id> \
  --field-id fldZxaqQl9 \
  --file /path/to/portfolio.pdf \
  --as user
```

如果上传多个文件，重复 `--file`。如果附件只有文件名没有本地路径，跳过上传并写入文件名字段。

## 5. 失败处理

- 字段不存在：重新 `+field-list`，使用真实字段。
- select 值报错：只用 `实习`、`正职`、`不确定`。
- 附件上传失败：普通字段记录保留，输出附件失败原因，不重复创建记录。
- 多条疑似重复：不写入，返回人工复核。
- 权限错误：停止并说明需要用户授权，不循环切换身份。

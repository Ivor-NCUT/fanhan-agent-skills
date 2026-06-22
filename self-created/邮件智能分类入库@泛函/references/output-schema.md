# 输出结构

## JSON

默认文件名：`email_classification.json`。

```json
{
  "mail": {
    "subject": "",
    "from": "",
    "to": [],
    "cc": [],
    "body_summary": "",
    "attachment_summary": []
  },
  "classification": {
    "primary_category": "candidate_submission|hiring_company|headhunter_partner|ecosystem_referral|other|needs_review",
    "confidence": 0.0,
    "candidate_categories": [
      {
        "category": "",
        "confidence": 0.0,
        "reason": ""
      }
    ],
    "needs_human_review": false,
    "evidence": [
      {
        "source": "subject|body|attachment",
        "text": "",
        "why_it_matters": ""
      }
    ],
    "negative_evidence": []
  },
  "ingestion": {
    "recommended_action": "create_candidate_record|create_company_demand_record|create_partner_record|create_referral_record|ignore_or_archive|manual_review",
    "target_table_or_collection": "",
    "dedupe_keys": [],
    "record": {}
  },
  "recommended_email_action": {
    "needed": false,
    "intent": "",
    "recipient": "",
    "notes": ""
  },
  "follow_up": {
    "questions": [],
    "missing_fields": [],
    "next_skill": ""
  }
}
```

## Markdown

默认文件名：`email_classification.md`。

```markdown
# 邮件分类结果：[邮件标题]

## 结论
- 主分类：
- 置信度：
- 是否需要人工复核：

## 判断证据

## 为什么不是其他类

## 入库建议

## 建议后续动作

## 缺失信息
```

## 规则

- `confidence` 用 0-1，小数即可。
- 置信度低于 0.65 或证据冲突时，`needs_human_review` 设为 `true`。
- `record` 只填邮件中能确认的信息，缺失字段留空。
- `recommended_email_action` 只表达意图，不生成具体发信配置。


# 输出结构

## JSON

默认文件名：`candidate_parse.json`。

```json
{
  "candidate": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "headline": "",
    "source_context": {
      "mail_subject": "",
      "mail_body_summary": "",
      "candidate_hint": {}
    }
  },
  "sources": [
    {
      "source_id": "src_001",
      "category": "resume|portfolio|context",
      "source_type": "pdf|docx|pptx|markdown|html|lark_doc|webpage|social|video|podcast|github|linkedin|rss|forum|other",
      "uri_or_path": "",
      "status": "success|partial|failed|blocked",
      "parser_used": "",
      "failure_reason": "",
      "extracted_text_path": "",
      "evidence_refs": []
    }
  ],
  "resume": {
    "summary": "",
    "education": [],
    "work_experience": [],
    "projects": [],
    "skills": [],
    "links": [],
    "raw_text_excerpt": ""
  },
  "portfolio_projects": [
    {
      "project_id": "work_001",
      "title": "",
      "work_type": "website|image|ppt|video|social_account|article|open_source|demo|career_profile|forum_thread|other",
      "candidate_role": "",
      "tools_or_tech": [],
      "summary": "",
      "outcomes": [],
      "evidence": [
        {
          "source_id": "src_001",
          "kind": "quote|page|timestamp|screenshot|link|metric",
          "locator": "",
          "text": ""
        }
      ],
      "ability_signals": {
        "aesthetic_judgment": {
          "label": "strong|medium|weak|unknown",
          "score": null,
          "evidence_ids": []
        },
        "internet_sense": {
          "label": "strong|medium|weak|unknown",
          "score": null,
          "evidence_ids": []
        },
        "content_quality": {
          "label": "strong|medium|weak|unknown",
          "score": null,
          "evidence_ids": []
        },
        "technical_execution": {
          "label": "strong|medium|weak|unknown",
          "score": null,
          "evidence_ids": []
        },
        "product_sense": {
          "label": "strong|medium|weak|unknown",
          "score": null,
          "evidence_ids": []
        }
      }
    }
  ],
  "search_ready_profile": {
    "keywords": [],
    "embedding_text": "",
    "jd_matching_notes": []
  },
  "open_questions": [],
  "parse_warnings": []
}
```

## Markdown

默认文件名：`candidate_parse.md`。

```markdown
# 候选人解析报告：[候选人名或邮件标题]

## 一句话画像

## 简历要点

## 作品集项目卡片

### [作品名称]
- 类型：
- 候选人角色：
- 工具/技术：
- 成果：
- 能力信号：
- 证据：

## 可检索关键词

## 解析状态

## 失败与待补充
```

## 证据规则

- 能力标签必须绑定证据，不允许只写主观结论。
- `score` 是 0-5 的初步评分；证据不足时填 `null`。
- 截图、字幕、临时网页缓存等放 `/tmp/` 或用户指定输出目录，不进仓库。
- 对低置信度判断，在 Markdown 里明确写出原因。

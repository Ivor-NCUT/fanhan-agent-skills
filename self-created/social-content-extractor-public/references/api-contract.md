# AI Conductor API 契约

来源：[AI Conductor 工具箱](https://fo7o7qognh.apifox.cn/330633303e0)，核对日期：2026-09-03。接口和价格可能变化；成本敏感或报错时以在线文档为准。

## Onboarding 与鉴权

- 注册入口：[AI Conductor 开发者平台](https://dev.aiconductor.fun/)。用户注册并创建 API key 后，把 key 交给 Agent。
- Agent 运行 `extract_social_content.py --configure`，通过交互 stdin 输入 key。脚本保存在当前用户的 `~/.config/aiconductor/api_key`；新建的专属目录权限为 `700`，文件权限为 `600`，读取时拒绝符号链接和宽松权限。
- `AICONDUCTOR_API_KEY` 可临时覆盖本机配置。Skill、压缩包、命令参数、输出和日志均不得包含 key。
- 若没有可用 key，脚本只返回注册网址与配置步骤，不发起付费请求。

真实响应中的 `total_fee` / `total_service_fee` 是本次扣费事实，优先级高于表中静态标价；2026-09-03 的公众号单篇探针两次调用合计返回 0.10 元，2026-09-11 的普通网页探针返回 0.02 元。

| 场景 | Endpoint | 主要输入 | 当前文档价格 |
|---|---|---|---|
| 抖音作品 | `/api/douyin_video_info` | `share_url` | 0.01 元/次 |
| 抖音主页 | `/api/douyin_user_videos` | `home_page`, `max_pages`, `max_seconds<=50` | 0.03 元/页 |
| 小红书作品 | `/api/xhs_note_info_v3` | `note_id` | 0.15 元/次 |
| 小红书主页 | `/api/xhs_user_notes_v2` | `user_id`, `max_pages`, `max_seconds` | 0.15 元/页 |
| 公众号正文/普通网页 | `/api/url_to_markdown` | `url` | 0.01 元/次 |
| 公众号作品数据 | `/api/wx_article_data` | `url` | 0.08 元/次 |
| 公众号历史文章 | `/api/wx_history_articles` | `url` 或 `name`, `max_pages`, `max_seconds` | 0.2 元/页 |

鉴权统一优先使用 `Authorization: Bearer <api_key>`；文档仍要求 body `api_key` 的旧接口同时发送 body 参数。

字段归一化：

- 抖音：`title/copy <- title 或 desc`；`metrics <- interaction/statistics`。
- 小红书：`title <- title`，`copy <- desc`；`metrics <- interact_info` 或主页列表计数。
- 公众号：标题从 Markdown frontmatter 读取，正文为 frontmatter 之后的 Markdown；数据来自 `wx_article_data`。历史接口只给列表，所以 `--copy` 会逐篇调用 `url_to_markdown`。
- 普通网页：返回标题和 Markdown；第三方接口不提供作品数据，`metrics` 为空。

完整性限制：公众号历史响应可能给 `total_page`，可以验证是否取完；抖音与小红书主页响应通常不提供可验证总量，只能报告页数上限与实际结果。

2026-09-03 实测 V3 主页接口对多个公开示例账号返回成功但 0 页；V2 返回 20 条且字段一致，因此主页固定使用 V2，单篇继续使用 V3。

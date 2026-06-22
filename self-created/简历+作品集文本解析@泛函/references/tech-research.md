# 技术研究与取舍

## 文档解析候选

- Docling：适合作为主解析候选，面向 PDF、DOCX、PPTX、HTML、图片等文档转换和结构化抽取。
- MarkItDown：适合作为轻量转换候选，目标是把多种文件转成 Markdown，方便 LLM 后处理。
- Apache Tika：适合作为兜底文本抽取器，覆盖面广，适合“先拿到文本”的场景。
- Unstructured：适合复杂文档元素切分和后续向量化，但初版不要把它作为唯一依赖。

第一版建议：skill 先规定工具选择顺序，不绑定单一库。真实运行时按本机可用工具选择；失败时记录 `parser_used` 和 `failure_reason`。

## 网页和平台解析

- 通用网页：Jina Reader 或 web-reader MCP。
- 公众号：Exa crawling；必要时 Camoufox。
- 视频：yt-dlp 先取元数据和字幕；没有字幕时再考虑音频转写。
- 社媒：按 Agent Reach 的平台路由调用，遵守登录、cookie、频控和平台限制。

## 为什么不第一版就写统一解析器

候选人作品集来源高度分散：PDF、PPT、个人网站、飞书文档、短视频、社媒账号、长文、GitHub 项目都可能出现。初版真正需要稳定的是：

1. 来源清单和解析状态。
2. JSON + Markdown 输出结构。
3. 证据优先的能力标签。
4. 平台和工具路由。

等真实样本积累后，再把高频解析路径沉淀成脚本。

## 已参考的成熟方案

- Microsoft MarkItDown: https://github.com/microsoft/markitdown
- Docling: https://github.com/docling-project/docling
- Apache Tika: https://tika.apache.org/
- Unstructured: https://docs.unstructured.io/
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- OpenAI Whisper: https://github.com/openai/whisper
- Playwright: https://playwright.dev/python/
- Jina Reader: https://jina.ai/reader/


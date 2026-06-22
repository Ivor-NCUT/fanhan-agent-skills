# Source Routing

## 总原则

先按来源类型选最稳定、最少侵入的读取方式。不要为了抓取更多信息触发平台风控；失败时记录原因，继续处理其他材料。

Agent Reach 临时输出规则：临时文件放 `/tmp/`，持久配置放 `~/.agent-reach/`，不要在项目仓库写入抓取缓存或候选人原始材料。

## 通用网页

优先：

```bash
curl -s "https://r.jina.ai/URL"
```

需要保留图片或格式时：

```bash
mcporter call 'web-reader.webReader(url: "https://example.com", retain_images: true)'
```

对审美判断有帮助的网页，额外保留截图证据；截图只作为证据线索，不直接替代文本解析。

## 微信公众号和长文

公众号文章优先用 Exa：

```bash
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

如遇验证码或正文缺失，可尝试 Camoufox：

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai && python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

长文重点提取：标题、作者、核心观点、结构、案例、表达质量、可引用片段。

## YouTube / B站 / 视频

先取元数据：

```bash
yt-dlp --dump-json "URL"
```

再取字幕：

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
```

视频项目卡片保留：标题、简介、发布时间、平台指标、字幕摘要、关键时间戳、封面/截图线索。自动字幕要记录为低置信度来源。

## 小红书

用搜索结果或完整 URL 读取，不要裸 note_id：

```bash
xhs search "query"
xhs read NOTE_ID_OR_URL
xhs comments NOTE_ID_OR_URL
```

网感证据重点：标题、封面描述、正文结构、评论反馈、互动数据、账号定位。

## 抖音

优先用 MCP：

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
mcporter call 'douyin.extract_douyin_text(share_link: "https://v.douyin.com/xxx/")'
```

记录平台限制和可用字段；不要把下载视频作为第一选择。

## Twitter / X

```bash
twitter tweet URL_OR_ID
twitter article URL_OR_ID
twitter user-posts @username -n 20
```

如果搜索失效，记录平台接口失败，不要反复重试。

## Reddit / V2EX / 论坛

Reddit：

```bash
rdt read POST_ID
```

V2EX：

```bash
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

重点提取：主题、回复质量、社区反馈、技术表达、内容可信度。

## 飞书文档 / 云文件 / 幻灯片

先检查授权：

```bash
lark-cli auth status --verify
```

如果不可用：

```bash
lark-cli auth login --no-wait --json
```

识别链接：

```bash
lark-cli drive +inspect "URL"
```

读取 docs 前先读匹配的内置 skill：

```bash
lark-cli skills read lark-doc
```

按类型选择：

- docs/docx：`docs +fetch`
- Drive 文件：`drive +download`
- 云文档导出：`drive +export`
- Markdown：`markdown +fetch`

## 搜索补全

当作品链接信息不足、候选人提供的是账号名或作品名时，可用搜索补全：

```bash
mcporter call 'exa.web_search_exa(query: "候选人名 作品名", numResults: 5)'
```

搜索结果只能作为候选来源，必须保留 URL 和检索关键词，不要把同名结果直接认定为本人作品。

## LinkedIn / 职业资料

优先：

```bash
mcporter call 'linkedin-scraper.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'
```

Fallback：

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```

LinkedIn 资料用于补充职业经历、公司、岗位、项目描述和公开背书。需要登录态时记录授权状态，不要把抓取失败包装成候选人资料缺失。

## GitHub / 开源项目

```bash
gh repo view owner/repo
gh search repos "candidate project keyword" --sort stars --limit 10
gh search code "candidate keyword" --language python
```

开源项目重点提取：

- repo 名称、简介、主要语言、stars/forks、最近更新时间。
- README 里的项目目标、安装方式、Demo、截图、技术栈。
- 候选人角色证据：提交、issue、PR、作者信息、项目署名。
- 能力标签：`technical_execution`、`product_sense`，必要时也可补 `content_quality`。

同名账号或同名仓库必须标低置信度，不能直接认定归属。

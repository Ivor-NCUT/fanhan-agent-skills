# 泛函 Agent Skills

这个仓库收集了泛函本机正在使用的一组 Agent skill，共 129 个。

我把它们分成两类：

- `self-created/`：泛函自己沉淀出来的定制 skill，共 37 个。
- `downloaded/`：下载或安装来的通用 skill，共 92 个，包含 dbs 工具箱。

这些 skill 覆盖内容创作、飞书工作流、会议纪要、视频素材、咨询交付、前端页面、文件处理、GitHub 工作流等场景。适合拿来观察一个科技从业者如何把高频工作拆成可复用的 Agent 能力。

## 泛函的服务说明

- [泛函｜科技从业者的创始人 IP 服务｜交付说明](https://twoj0037lkv.feishu.cn/wiki/GjKUwEeC1imQOGkOdxkccj6BnJc)
- [泛函｜顶尖内容团队 AI 提效｜服务说明](https://twoj0037lkv.feishu.cn/wiki/YoEPw38TsizpxqkTYAJcCYw7nqf?from=from_copylink)

这里的 AI 指人工智能（AI）。如果你想了解这些 skill 背后的服务形态，可以先看上面两份飞书文档。

## 怎么使用

每个 skill 目录里都有 `SKILL.md`。把需要的目录复制到你的 Agent skill 目录后，重启对应的 Agent 环境即可加载。

如果你只想快速浏览，直接看下面的清单。每一行都有一句话说明和仓库路径。

## 自建定制 Skill

| Skill | 一句话介绍 | 仓库路径 |
|---|---|---|
| skill 开发与迭代规范 | 用软件开发最佳实践管理复杂 Agent skill 的需求澄清、阶段文档和 GitHub 迭代。 | `self-created/skill-开发与迭代规范` |
| 简历 + 作品集文本解析@泛函 | 把候选人邮件材料、简历、作品集和网页/社媒/视频证据解析成 JSON + Markdown。 | `self-created/简历+作品集文本解析@泛函` |
| 邮件智能分类入库@泛函 | 把上游读取出的邮件标题、正文和附件信息分类成候选人、招聘公司、猎头伙伴等可入库记录。 | `self-created/邮件智能分类入库@泛函` |
| 候选人入库@泛函 | 把候选人投递邮件和简历/作品集解析结果写入飞书多维表格候选人表。 | `self-created/候选人入库@泛函` |
| AI 领域求职咨询顾问@泛函 | 用来做访谈式梳理、咨询交付或课程整理。 | `self-created/ai-career-consultant-fanhan` |
| Bonjour! 全栈员工 | 用来提炼风格、改写内容或产出发布文案。 | `self-created/bonjour-full-stack-employee` |
| 咨询记录整理@泛函 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/consulting-record-organizer-fanhan` |
| 转化漏斗文案法@泛函 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/conversion-funnel-copywriting-fanhan` |
| 课程主编@泛函 | 用来做访谈式梳理、咨询交付或课程整理。 | `self-created/course-editor-in-chief-fanhan` |
| 泛函风格写作 | 用来提炼风格、改写内容或产出发布文案。 | `self-created/fanhan-style-writing` |
| 泛函个人网站内容更新 | 从七个编辑栏目中选择，并按对应资料模板更新泛函个人网站。 | `self-created/fanhan-personal-site-updater` |
| lark Course 协作 | 用来连接飞书里的具体工作对象。 | `self-created/lark-course-xiezuo` |
| 飞书跨租户迁移文档@泛函 | 用来把飞书云文档、知识库、云盘文件和多维表格跨租户迁移到目标租户。 | `self-created/飞书跨租户迁移文档@泛函` |
| 自然流编导@泛函（agents） | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/natural-flow-director-fanhan` |
| 线下演讲录音稿精校@泛函 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/offline-speech-transcript-editor-fanhan` |
| 个人 IP 定位咨询@泛函 | 用来做访谈式梳理、咨询交付或课程整理。 | `self-created/personal-ip-positioning-consultant-fanhan` |
| 播客切片编导@泛函 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/podcast-clip-director-fanhan` |
| 服务报价说明书@泛函 | 用来做访谈式梳理、咨询交付或课程整理。 | `self-created/service-pricing-guide-fanhan` |
| 推特代笔人 | 用来把固定工作流程封装成可复用能力。 | `self-created/twitter-ghostwriter` |
| 内容风格提取 | 用来提炼风格、改写内容或产出发布文案。 | `self-created/内容风格提取` |
| 口播视频粗剪@方比比 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/口播视频粗剪@方比比` |
| 培训讲解课程稿整理@方比比 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/培训讲解课程稿整理@方比比` |
| 多维表格搭建咨询@泛函 | 用来做访谈式梳理、咨询交付或课程整理。 | `self-created/多维表格搭建咨询@泛函` |
| 招聘类小红书笔记@方比比 | 用来提炼风格、改写内容或产出发布文案。 | `self-created/招聘类小红书笔记@方比比` |
| 方比比视频号标题方法论 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/方比比视频号标题方法论` |
| 理白风格写作 | 用来提炼风格、改写内容或产出发布文案。 | `self-created/理白风格内容创作` |
| 直播带货话术拆解@方比比 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/直播带货话术拆解@方比比` |
| 视频号数据分析@方比比 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/视频号数据分析@方比比` |
| 视频文件提取文本 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/视频文件提取文本` |
| 选题调研@方比比 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/选题调研@方比比` |
| Frontend Slides | 用来生成演示稿和网页幻灯片。 | `self-created/frontend-slides_fanhan` |
| 自然流编导@泛函（codex） | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/natural-flow-director-fanhan` |
| 启发式访谈口播粗剪@泛函 | 用来处理视频、口播、访谈或逐字稿素材。 | `self-created/启发式访谈口播粗剪@泛函` |

## 下载或安装的通用 Skill

| Skill | 一句话介绍 | 仓库路径 |
|---|---|---|
| Agent Reach — 路由器 | 用来搜索网页、社媒、招聘、代码仓库和视频内容。 | `downloaded/agent-reach` |
| algorithmic-art | 用来生成网页、视觉稿或前端界面。 | `downloaded/algorithmic-art` |
| Alltuu Album Downloader | 用来批量下载图宇相册和活动图片。 | `downloaded/alltuu-album-downloader` |
| Anthropic Brand Styling | 用来生成网页、视觉稿或前端界面。 | `downloaded/brand-guidelines` |
| canvas-design | 用来生成网页、视觉稿或前端界面。 | `downloaded/canvas-design` |
| Codex-api | 用来搭建工具、接口或可复用的 Agent 能力。 | `downloaded/claude-api` |
| Codebase-to-Course | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/codebase-to-course` |
| dbs：商业工具箱 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs` |
| dbs-action：执行力诊断 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-action` |
| dbs-agent-migration：Agent 工作台迁移 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-agent-migration` |
| dbs-ai-check：AI 写作特征识别 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-ai-check` |
| dbs-benchmark：对标分析 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-benchmark` |
| dbs-chatroom：定向聊天室 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-chatroom` |
| dbs-chatroom-austrian：奥派经济聊天室 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-chatroom-austrian` |
| dbs-content：内容创作诊断 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-content` |
| dbs-deconstruct：概念拆解 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-deconstruct` |
| dbs-diagnosis：商业模式诊断 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-diagnosis` |
| dbs-goal：目标清晰化 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-goal` |
| dbs-hook：短视频开头优化 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-hook` |
| dbs-logic-continuity：dontbesilent 逻辑延续检查 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-logic-continuity` |
| dbs-report：诊断报告 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-report` |
| dbs-restore：接续诊断 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-restore` |
| dbs-save：诊断存档 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-save` |
| dbs-slowisfast：慢就是快 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-slowisfast` |
| dbs-xhs-title：小红书标题公式工具 | dontbesilent 商业诊断工具箱的一部分。 | `downloaded/dbskill__skills__dbs-xhs-title` |
| Doc Co-Authoring Workflow | 用来提炼风格、改写内容或产出发布文案。 | `downloaded/doc-coauthoring` |
| DOCX creation, editing, and analysis | 用来读取、整理或生成对应格式的办公文件。 | `downloaded/docx` |
| dumbledore：邓布利多知识库主入口（agents） | 用来管理知识库仓库和相关发布流程。 | `downloaded/dumbledore` |
| Find Skills | 用来搭建工具、接口或可复用的 Agent 能力。 | `downloaded/find-skills` |
| frontend-design | 用来生成网页、视觉稿或前端界面。 | `downloaded/frontend-design` |
| Magazine Web Ppt | 用来生成演示稿和网页幻灯片。 | `downloaded/guizang-ppt-skill` |
| InsForge SDK Skill | 用来搭建和调试 InsForge 应用。 | `downloaded/insforge` |
| InsForge CLI | 用来搭建和调试 InsForge 应用。 | `downloaded/insforge-cli` |
| InsForge Debug | 用来搭建和调试 InsForge 应用。 | `downloaded/insforge-debug` |
| InsForge Integrations | 用来搭建和调试 InsForge 应用。 | `downloaded/insforge-integrations` |
| internal-comms | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/internal-comms` |
| 访谈式创作 | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/interview-led-writing` |
| approval (v4) | 用来连接飞书里的具体工作对象。 | `downloaded/lark-approval` |
| apps (v1) | 用来连接飞书里的具体工作对象。 | `downloaded/lark-apps` |
| attendance (v1) | 用来连接飞书里的具体工作对象。 | `downloaded/lark-attendance` |
| base | 用来读写飞书多维表格和仪表盘。 | `downloaded/lark-base` |
| calendar (v4) | 用来查看和管理飞书日程。 | `downloaded/lark-calendar` |
| lark-contact | 用来查找飞书通讯录人员。 | `downloaded/lark-contact` |
| docs (v2) | 用来读取、整理和更新飞书文档。 | `downloaded/lark-doc` |
| drive (v1) | 用来上传、下载和管理飞书网盘文件。 | `downloaded/lark-drive` |
| Lark Events | 用来连接飞书里的具体工作对象。 | `downloaded/lark-event` |
| im (v1) | 用来收发飞书消息和管理群聊。 | `downloaded/lark-im` |
| 飞书知识库搭建 | 用来连接飞书里的具体工作对象。 | `downloaded/lark-knowledge-base-builder` |
| mail (v1) | 用来起草、修改和发送飞书邮箱邮件。 | `downloaded/lark-mail` |
| markdown (v1) | 用来读取、整理和更新飞书文档。 | `downloaded/lark-markdown` |
| minutes (v1) | 用来处理飞书会议、妙记、纪要和逐字稿。 | `downloaded/lark-minutes` |
| okr (v2) | 用来连接飞书里的具体工作对象。 | `downloaded/lark-okr` |
| OpenAPI Explorer | 用来连接飞书里的具体工作对象。 | `downloaded/lark-openapi-explorer` |
| lark-cli 共享规则 | 用来连接飞书里的具体工作对象。 | `downloaded/lark-shared` |
| sheets (v3) | 用来创建和读写飞书电子表格。 | `downloaded/lark-sheets` |
| lark-skill-maker | 用来连接飞书里的具体工作对象。 | `downloaded/lark-skill-maker` |
| slides (v1) | 用来连接飞书里的具体工作对象。 | `downloaded/lark-slides` |
| task (v2) | 用来管理飞书任务和清单。 | `downloaded/lark-task` |
| vc (v1) | 用来处理飞书会议、妙记、纪要和逐字稿。 | `downloaded/lark-vc` |
| vc-agent (v1) | 用来处理飞书会议、妙记、纪要和逐字稿。 | `downloaded/lark-vc-agent` |
| lark-whiteboard | 用来连接飞书里的具体工作对象。 | `downloaded/lark-whiteboard` |
| wiki (v2) | 用来读取、整理和更新飞书文档。 | `downloaded/lark-wiki` |
| 会议纪要汇总工作流 | 用来连接飞书里的具体工作对象。 | `downloaded/lark-workflow-meeting-summary` |
| 日程待办摘要工作流 | 用来连接飞书里的具体工作对象。 | `downloaded/lark-workflow-standup-report` |
| MCP Server Development Guide | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/mcp-builder` |
| PDF Processing Guide | 用来读取、整理或生成对应格式的办公文件。 | `downloaded/pdf` |
| PPTX Skill | 用来读取、整理或生成对应格式的办公文件。 | `downloaded/pptx` |
| skill-creator | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/skill-creator` |
| Slack GIF Creator | 用来把固定工作流程封装成可复用能力。 | `downloaded/slack-gif-creator` |
| Insert instructions below | 用来做访谈式梳理、咨询交付或课程整理。 | `downloaded/template-skill` |
| Theme Factory Skill | 用来生成演示稿和网页幻灯片。 | `downloaded/theme-factory` |
| Vercel React Best Practices | 用来生成网页、视觉稿或前端界面。 | `downloaded/vercel-react-best-practices` |
| Web Artifacts Builder | 用来生成网页、视觉稿或前端界面。 | `downloaded/web-artifacts-builder` |
| Web Application Testing | 用来生成网页、视觉稿或前端界面。 | `downloaded/webapp-testing` |
| Requirements for Outputs | 用来读取、整理或生成对应格式的办公文件。 | `downloaded/xlsx` |
| Brainstorming Ideas Into Designs | 探索尚未明确的目标与设计选择；已授权实施时直接执行。 | `downloaded/brainstorming` |
| cubox-cli | 用来生成网页、视觉稿或前端界面。 | `downloaded/cubox` |
| dumbledore：邓布利多知识库主入口（codex） | 用来管理知识库仓库和相关发布流程。 | `downloaded/dumbledore` |
| dumbledore-onboarding：安装与私有仓库初始化 | 用来管理知识库仓库和相关发布流程。 | `downloaded/dumbledore-onboarding` |
| Figma MCP | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma` |
| Code Connect Components | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-code-connect-components` |
| Create Design System Rules | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-create-design-system-rules` |
| create_new_file — Create a New Figma File | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-create-new-file` |
| Build / Update Screens from Design System | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-generate-design` |
| Design System Builder — Figma MCP Skill | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-generate-library` |
| Implement Design | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-implement-design` |
| use_figma — Figma Plugin API Skill | 用来连接 Figma 设计稿、组件和设计系统。 | `downloaded/figma-use` |
| PR Comment Handler | 用来处理代码仓库、评审意见和发布流程。 | `downloaded/gh-address-comments` |
| Gh Pr Checks Plan Fix | 用来处理代码仓库、评审意见和发布流程。 | `downloaded/gh-fix-ci` |
| GitHub Skill Publisher | 用来处理代码仓库、评审意见和发布流程。 | `downloaded/gh-skill-publisher` |
| Go Wild Camping Style | 用来生成演示稿和网页幻灯片。 | `downloaded/go-wild-camping-style` |
| Using Skills | 用来生成网页、视觉稿或前端界面。 | `downloaded/using-superpowers` |

## 打包口径

本仓库排除了 `.git`、`.venv`、缓存、临时输出、编译文件和运行产物，只保留说明、脚本、模板和参考资料。

部分通用 skill 来自外部作者或工具生态，版权与许可请以各目录中的原始说明为准。没有明确许可证的目录，请先联系原作者再做商业分发。

---
name: 培训讲解课程稿整理@方比比
description: 将线下培训、内部讲课、工作坊、团队分享的 PPT/飞书幻灯片和录音转写稿整理成图文混排课程文档。Use this skill whenever the user provides a course transcript plus PPT/slides/PDF/keynote deck and wants a readable Feishu/Lark course document, training handout, lesson article, or illustrated tutorial. This skill should trigger over generic summarization when the task involves “录音转文字 + 课件/PPT + 图文混排 + 课程稿润色 + 逻辑延续检查”, even if the user only says “帮我把这次培训整理成文档”.
---

# 培训讲解课程稿整理@方比比

## Purpose

把一次线下讲课或团队培训整理成一份可阅读、可复盘、可转发的图文混排课程文档。

用户通常会提供两类材料：

- 讲课时使用的 PPT、飞书 Slides、PDF 或其他课件。
- 课程录音转写出来的文字稿，可能是飞书文档、Markdown、TXT 或粘贴文本。

你的任务不是做会议纪要，也不是清洗逐字稿。你要把讲课内容编成一篇正式课程稿：保留主讲人的真实口吻，重建清晰主线，把 PPT 每页导出为图片并插入到对应段落，再做逻辑延续检查，让读者即使没在现场，也能顺着讲解学完这节课。

## Companion Skills

执行时按需要加载或参考：

- `lark-doc`：读取、创建、更新飞书文档，插入图片块。
- `lark-slides` / `lark-wiki`：解析飞书 Slides 或 wiki 链接，导出课件。
- `lark-course-xiezuo`：把转写稿改成正式课程稿的课程协作原则。
- `course-editor-in-chief-fanhan`：课程正文主线、段落节奏和教学任务判断。
- `dbs-logic-continuity`：检查段落衔接、信息密度和口播流畅度。
- `dbs-ai-check`：必要时检查 AI 写作痕迹，只留下需要用户判断的评论。

如果某个 companion skill 不可用，继续用本 skill 的规则完成任务，并在最终回复中说明缺口。

## Inputs

常见输入：

- PPT / Slides / PDF 课件链接或本地文件路径。
- 录音转写稿链接或本地文件路径。
- 可选：目标飞书文档链接、目标知识库位置、是否覆盖原文档。
- 可选：主讲人、课程标题、面向对象、是否保留旧稿。

默认行为：

- 如果用户给的是转写稿飞书文档，并没有要求保留旧稿，直接覆盖该文档为正式图文课程稿。
- 如果用户明确说“新建一篇”“不要改原文档”，就创建新文档。
- 如果没有目标飞书文档，就先生成本地 Markdown，并在可用时创建飞书文档。

## Workflow

### 1. Resolve and Read Materials

先确认两类材料都能读取：

1. 读取转写稿全文。
   - 飞书文档用 `lark-cli docs +fetch --api-version v2 --doc <url> --doc-format markdown --detail simple`。
   - 本地文件直接读取。
2. 解析课件。
   - 飞书 wiki 链接先用 `wiki spaces get_node` 解析真实 `obj_type` 和 `obj_token`。
   - 飞书 Slides 用真实 `obj_token` 导出。
   - 本地 PPT/PDF 直接进入导出流程。

不要根据 URL 猜内容。拿不到正文或课件时，先解决读取问题。

### 2. Export Slides as Images

目标是让每一页课件成为文档里的图片块。

推荐稳定路径：

1. 如果是飞书 Slides，先导出为 PDF：

```bash
lark-cli drive +export \
  --token <slides_token> \
  --doc-type slides \
  --file-extension pdf \
  --file-name course-slides.pdf \
  --output-dir ./exports \
  --overwrite
```

2. 用 `pdftoppm` 逐页导出 PNG：

```bash
mkdir -p exports/pdf-pages
pdftoppm -png -r 180 exports/course-slides.pdf exports/pdf-pages/slide
```

3. 如果用户给的是 PPTX，优先先转 PDF，再转 PNG。只有 PDF 不可用时，再考虑 Keynote、PowerPoint、LibreOffice 或 Quick Look。

4. 确认页数：

```bash
find exports/pdf-pages -type f | sort | wc -l
```

导出图片时不要在最终文档中保留“课件页01：……”这类占位标识。可以在本地草稿阶段用它们定位，回写前必须删除。

### 3. Extract Slide Outline

从课件中提取页面标题和大致顺序，用来安排图片插入位置。

- PPTX 可用 zip 读取 `ppt/slides/slide*.xml` 中的文本。
- 飞书 Slides 可用 `slides xml_presentations get` 读取 XML。
- PDF 图片无法提取文本时，按转写稿讲解顺序插入图片。

提取出来的标题只作为本地定位，不要直接写进最终文档，除非这些标题本身就是正文需要解释的内容。

### 4. Deconstruct the Teaching Task

先做一次简短判断，再开始改写：

- 这节课真正要教会学员什么？
- 学员的起点是什么，学完要能做什么？
- 哪些内容是概念解释，哪些是操作步骤，哪些是案例？
- PPT 页和讲解内容的对应关系是什么？
- 哪些地方是现场闲聊、打断、重复、口误、转写错误？
- 哪些建议涉及平台限制、客户关系、发布承诺、价格、权限或合规，需要用户判断？

不要把这一步写成长报告，除非用户要求。它主要用于帮助你重建课程主线。

### 5. Rewrite as a Course Document

把转写稿改成正式课程稿。

写作原则：

- 保留主讲人的身份和口吻。例如“我是泛函”“今天这节课我们只解决一个问题”。
- 开头交代本课任务，不写泛泛背景。
- 不把转写稿逐句清洗成“会议纪要”；要重建成讲义。
- 每个章节承担一个教学动作：定义、原则、步骤、案例、调优、边界、作业。
- 标题用语义化表达，不用“一、二、三”。
- 段落像老师连续讲课：一个段落承载一个教学动作，句子可以由 2-5 个短句组成。
- 保留现场高价值例子。删除口误、重复确认、无意义闲聊和打断。
- 把抽象建议落成字段、步骤、模板、判断标准或作业要求。
- 高风险建议只写边界和待判断点，不替用户做承诺。

避免：

- 过度书面腔。
- “综上所述”“总而言之”“随着……发展”“赋能”“抓手”等模板话。
- 每段都收成金句。
- 把课程稿写成产品说明书或工具百科。

### 6. Place Images in Context

把每页课件图片插到它对应的讲解段落附近。

稳定做法：

1. 本地 Markdown 草稿中可以临时写图片 Markdown。
2. 如果写回飞书 Markdown 时图片链接已可用，可以整体回写。
3. 如果需要创建飞书图片块，用 `docs +media-insert`：

```bash
lark-cli docs +media-insert \
  --doc "<doc_url_or_token>" \
  --type image \
  --file "exports/pdf-pages/slide-01.png" \
  --selection-with-ellipsis "<target paragraph text>" \
  --width 720 \
  --align center
```

插图规则：

- 不要把所有图片堆在文末。
- 不要在最终正文里保留“课件页01：……”这种机械标识。
- 如果一页 PPT 只是章节页，可以放在章节标题后。
- 如果一页 PPT 是具体操作截图，放在对应步骤之后。
- 如果图片插入失败，不要假装完成；说明失败页码并保留本地图片路径。

### 7. Check Logic Continuity

图文稿完成后，用 `dbs-logic-continuity` 的标准检查全文。

重点看：

- 定义讲完后，是否自然进入“为什么要调”。
- 原则讲完后，是否自然进入“怎么做第一版”。
- 构建讲完后，是否自然进入“怎么给 AI 材料”。
- 案例讲完后，是否自然进入“怎么调优”。
- 调优讲完后，是否自然进入“别人做好的 Skill 怎么安装/更新”。
- 能力讲完后，是否自然进入“边界和作业”。

如果发现逻辑不延续，直接综合全文优化：

- 补一句过渡。
- 删掉空转开场。
- 合并重复段落。
- 调整章节顺序。
- 把太长的句子拆成可读句群。

这一步不改变主讲人的观点，只优化读者能不能顺着读下去。

### 8. AI Smell and CEO Comments

最后做一轮轻量检查：

- 是否有过度光滑、AI 味强的句子。
- 是否有太强承诺，比如“必出好答案”。
- 是否有概念被过度简化，需要用户确认。
- 是否有风险边界需要 CEO 判断。
- 作业是否缺截止时间、验收人、交付位置。

如果写入飞书文档，优先用局部评论锚定到具体段落。评论要问用户判断，不要泛泛说“这里 AI 味重”。

### 9. Write Back and Verify

写回后必须复核：

- 正文已存在。
- 图片数量和课件页数一致。
- 最终文档里没有“课件页XX：……”机械标识。
- 标题结构清晰。
- 关键过渡已补上。
- 评论数量和需要用户判断的点一致。

推荐复核命令：

```bash
lark-cli docs +fetch --api-version v2 \
  --doc "<doc_url_or_token>" \
  --doc-format markdown \
  --detail simple
```

检查：

- `![](` 数量是否等于课件图片数量。
- `课件页` 出现次数是否为 0。
- 是否包含开头任务句和课后作业。

## Output Shape

最终课程文档通常包含：

```markdown
# 课程标题

主讲人：...
适用对象：...
本课任务：...

[课程开场]

## 概念/背景/问题

[正文]
[对应课件图片]

## 方法/步骤/原则

[正文]
[对应课件图片]

## 案例/示范

[正文]
[对应课件图片]

## 边界/作业

[正文]
[对应课件图片]
```

## Final Reply

最终回复用户时简短说明：

- 文档写到了哪里，给出链接或本地路径。
- 插入了多少张课件图片。
- 是否已删除机械页码标识。
- 是否做了逻辑延续优化。
- 添加了多少条需要用户判断的评论。
- 哪些事项仍需要用户决策。

不要把整篇课程稿粘回聊天，除非用户明确要求。


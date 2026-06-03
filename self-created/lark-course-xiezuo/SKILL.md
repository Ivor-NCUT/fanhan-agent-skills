---
name: lark-course-xiezuo
description: "lark Course 协作：把飞书课程初稿、课纲或单章文稿改成可由 CEO 评论协作的正式课程稿，并检查课程逻辑延续、段落衔接、信息密度和讲课流畅度。Use when the user asks to process a Feishu/Lark course draft, course outline, module structure, or lesson through Dbs Deconstruct, Course Editor In Chief Fanhan, Dbs Logic Continuity, and Dbs Ai Check; when they mention 飞书课程改稿、课程大纲重排、模块设计、课程协作、Course 协作、在飞书文档上编辑、通过飞书 CLI 评论、课程逻辑延续、段落衔接、信息密度、讲课顺不顺、AI 检查坏味道、课程初稿到正式稿、CEO 根据评论修改。"
---

# lark Course 协作

## Purpose

Use this skill to run the fixed collaborative course-editing chain on a Feishu/Lark course document:

1. Deconstruct concepts with `dbs-deconstruct`.
2. Rewrite the course with `course-editor-in-chief-fanhan` directly on the Feishu document.
3. Check course logic continuity, information density, and teaching flow with `dbs-logic-continuity`.
4. Check AI writing fingerprints with `dbs-ai-check`.
5. Add review comments to the Feishu document with `lark-cli`.
6. Leave the final document ready for CEO comment-based revision.

This is a live-document workflow. The goal is not only to produce a better draft, but to create a reviewable Feishu artifact with comments anchored to the exact text CEO should inspect.

When the target is a course outline or module structure, the workflow must also check whether the course lets the most urgent learners get results quickly. A course outline is not only a knowledge map; it is a sequence of user outcomes.

## Required Companion Skills

Load these skills when executing this workflow:

- `dbs-deconstruct`: concept analysis and false-concept detection.
- `course-editor-in-chief-fanhan`: course draft rewriting, chapter bridge, course quality checks.
- `dbs-logic-continuity`: paragraph-to-paragraph continuity, information density, and spoken/teaching flow checks adapted for course writing.
- `dbs-ai-check`: AI writing fingerprint and bad-smell detection.
- `lark-doc`, `lark-drive`, `lark-wiki`, and, when closing the loop, `lark-base`.

If any companion skill is unavailable, continue with the closest local fallback and clearly state the missing skill in the final reply.

## Inputs

Expect one current Feishu/Lark course document URL. Optional but preferred:

- previous lesson URL
- next lesson URL
- explicit instruction to preserve or overwrite the current draft
- known course series rules, speaker name, or style constraints
- if the target is an outline: intended learner segments, urgency level, and what result the first one or two modules should deliver

Default behavior: edit the provided course document in place unless the user explicitly says to create a new document or preserve the original draft.

## Workflow

### 1. Resolve and Read Documents

Use the lark shared auth rules first. For wiki URLs, resolve the node so the real `obj_token`, `obj_type`, title, parent token, and space id are known.

Read the current lesson. If previous/next lesson URLs are provided, read them too and extract only the bridge context needed for this lesson.

Use stable read patterns from `references/lark-course-cli.md`. Do not guess document content from a URL.

### 2. Deconstruct Concepts

Run a concise `dbs-deconstruct` pass before rewriting. Identify:

- the real teaching task of the lesson
- for outlines, the learner segment served by each module and the concrete result each module should deliver
- ambiguous or overloaded concepts
- false concepts or slogans that need plain-language replacement
- the action chain that connects previous lesson -> current lesson -> next lesson
- definitions, formulas, and boundaries that need CEO confirmation

Create a local deconstruction note when useful, but do not paste a long deconstruction report into the Feishu course doc unless the user asks.

### 3. Rewrite the Course Draft

Use `course-editor-in-chief-fanhan` to produce the formal draft.

Course rewrite requirements:

- Keep or restore the speaker attribution when known, for example "我是生姜 Iris" in this course line.
- Add previous/next lesson bridge when URLs or context are available.
- Turn raw transcript fragments into a coherent lesson, not a cleaned transcript.
- For course outlines, arrange modules by learner urgency and outcome speed. Do not assume the learner will finish the whole course. The first module should let the most urgent learner take action and get a visible result; the second module should still deliver a useful standalone result.
- Prefer concrete teaching actions: fields, steps, standards, formulas, examples, and homework.
- Preserve high-value original stories and examples when they teach the point.
- Avoid replacing the user's voice with generic AI polish.
- Use semantic section headings without leading Chinese ordinal prefixes. Prefer `## 为什么 Agent Skill 值得单独做增长` / `## ClawHub 增长先从站内搜索开始` over `## 一、...`, `## 二、...`, or `## 三、...` numbered headings.
- Follow the course editor style bans, especially avoiding template transitions and forbidden formulations.

Outline-specific checks:

- Does module 1 state who it serves, what urgent problem it solves, and what artifact or action it produces?
- If a learner stops after module 1, can they still use the course to move forward?
- If a learner stops after module 2, have they solved both immediate action and direction choice?
- Are industry background, long-term influence, and entrepreneurship preparation placed after urgent execution unless the user explicitly wants a theory-first course?

Before writing back, run a quick local scan for course-editor forbidden phrases when practical.

### 4. Course Logic Continuity Pass

Before writing back to Feishu, run a concise `dbs-logic-continuity` pass on the rewritten draft. Adapt the short-video logic to course writing:

- Replace "will the viewer swipe away" with "will the learner lose the thread, stop trusting the lesson, or fail to know what to do next".
- Treat each teaching section as a natural segment. Do not split every sentence; split by teaching task, example, transition, or exercise.
- Check section-to-section continuity: whether the learner can understand why this section follows the previous one, especially after examples, formulas, and homework.
- Check information density: whether a section repeats earlier points, adds background before urgent action, or uses many polished sentences without creating a new learning result.
- Check teaching/口播 flow: whether the lesson can be spoken by the instructor, whether long sentences should be split, whether terms are explained immediately, and whether transitions sound like a real teacher rather than a report.
- For outlines, check module-to-module continuity: whether module 1 and module 2 each deliver a standalone result, and whether later background/theory modules do not interrupt the urgent learner's path.

Only revise the draft directly for clear improvements: missing transitions, repeated paragraphs, overlong sentences, unexplained terms, and section order issues. Do not change the user's argument, case, data, or strategic position.

Keep a short local note of the continuity pass when useful. Use it to decide which Feishu comments to add later; do not paste a full "逻辑延续检查报告" into the course document unless the user explicitly asks.

Continuity risk levels:

- 🔴 High: a section jump, module order, or density drop will likely make the learner lose the thread.
- 🟡 Medium: the section is understandable but may feel loose, repetitive, or too report-like.
- 🟢 Small: wording or sentence rhythm improvements that are useful but not blocking.

### 5. Write Back to Feishu

If the user asked for direct editing or gave only one current draft URL, overwrite the target doc with the formal Markdown draft.

If the user explicitly asked to preserve the original, create a new sibling document under the same parent node and write the formal draft there.

After writing, fetch the updated document again to verify the text exists and to retrieve block IDs for comments.

### 6. AI Check, Continuity Check, and Comment

Run `dbs-ai-check` on the final draft after writeback. Select only actionable comments, usually 5-10 items.

Combine the AI-check findings with the continuity pass. Comments should surface the few places CEO actually needs to inspect, not every minor line edit.

Comment principles:

- Anchor comments to the exact paragraph or list item that CEO should inspect.
- Prefer local block comments, not full-document comments.
- Comments should ask CEO to judge, supplement, or rewrite. Do not merely announce that something is "AI-like".
- Use comments for: overly smooth conclusions, weak examples, simplified formulas, missing personal story, unclear promise, report-like structure, risky claims, or brand/style decisions.
- Use comments for continuity risks: missing transition between sections, a concept jump that needs one bridging sentence, repeated explanation that lowers density, a lecture paragraph that sounds like a written report, or a term/formula that needs an immediate plain-language explanation.
- For outlines, use comments for: first module lacks an outcome, urgent learners are forced through too much background, modules are organized as a knowledge taxonomy, or learner segments are mixed together without a clear result.
- If a block type does not support comments, anchor to the nearest text child block.

### 7. Close the System Loop

If this is a formal course draft or a substantial rewrite, add a record to `CEO 审查队列表` when the table can be located without new authorization.

Recommended fields:

- `产出名称`: lesson title + "正式课程稿"
- `产出类型`: "文档"
- `审查状态`: "待审查"
- `最终版本链接`: target Feishu wiki/doc URL
- `AI 自评分`: 1-5
- `需要 CEO 判断的点`: concise list of the exact review decisions
- `修改意见`: state that concept deconstruction, course rewrite, logic continuity pass, AI check, and Feishu comments are complete

For outline work, include whether the first two modules can stand alone and what CEO still needs to decide about learner priority, module order, promised outcomes, and any continuity risks between modules.

If the review queue cannot be located because of missing scope or broken access, state this explicitly and do not block the document work.

## Final Response

Report briefly:

- what was rewritten and where
- whether the logic continuity pass found high-risk breaks
- how many Feishu comments were added
- whether the CEO review queue was updated
- which points still need CEO judgment

Do not paste the whole course draft into chat unless the user asks.

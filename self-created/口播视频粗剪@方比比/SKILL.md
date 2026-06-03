---
name: 口播视频粗剪@方比比
description: 方比比口播视频粗剪工作流。Use this skill whenever the user sends or points to a rough-cut talking-head interview video for 方比比/IP口播/采访式口播 and wants the agent to extract audio, transcribe with Fun-ASR-Nano, identify likely viral clips, choose question-led answer/story segments, and write the full transcript plus clip rationale into a Feishu/Lark document. This skill should trigger over generic video transcription when the goal is 爆款选段、粗剪选题、口播视频选段、采访素材成片、写入飞书文档, even if the user only says “帮我从这个口播视频里挑爆款片段”.
---

# 口播视频粗剪@方比比

## Purpose

把采访式口播粗剪视频处理成一份可审查的飞书文档：

1. 从视频中抽取 `audio.mp3` 和 `audio_16k.wav`。
2. 用本地 Fun-ASR-Nano 模型转写完整原素材。
3. 从完整逐字稿中挑选最有机会成为爆款的片段。
4. 给每个片段补上开头问题、原文案对照、选段理由、剪辑建议和风险提醒。
5. 创建或更新一份飞书文档，写入完整转写文本和推荐片段。

这个 skill 面向“采访拍 IP，IP 回答问题，后期从问答中剪爆款口播”的生产场景。它不是普通转写工具；判断重点是内容传播潜力、情绪结构、故事完整度和成片可剪性。

## Core Rule: Verbatim Editing Only

这是剪辑工作，不是文案改写工作。视频里已经拍好的话无法被修改，所以输出给后期的所有成片文案都必须保留 IP 原话。

执行时遵守：

- 不润色、不改写、不补写、不替换表达。
- 不把口语改成书面语。
- 不调整 IP 的措辞、语气词、重复、停顿造成的表达，除非这些内容被整句删除并用删除线标出。
- 可以做的只有三件事：保留、删除、调整顺序。
- 如果 ASR 明显识别错字，只能在“风险或待确认”里标注“疑似转写错误，需人工复听”，不要擅自改成你认为正确的词。
- 报告里的“主要内容”和“原文案”都必须来自转写原文。需要一句话一行，方便剪辑师逐句对照。

## Inputs

用户通常会提供：

- 一个本地视频路径，或上传一个粗剪视频。
- 可选：IP 名称、项目名、拍摄日期、目标平台、目标受众、飞书文档目标位置。

如果缺少视频路径，先只问视频文件路径。其余元信息可用默认值继续推进，并在文档里标注“待补充”。

支持视频格式：`.mp4`、`.mov`、`.m4v`、`.mkv`、`.avi`、`.webm`。

## Required References

执行选段判断前读取：

- `references/fangbibi-viral-patterns.md`：方比比样本文档提炼出的爆款结构和选段标准。
- `references/report-template.md`：飞书文档输出结构。

如果用户给了新的飞书样本文档或新的案例库，先用 `lark-doc` 读取样本，再把新的判断补入本次分析；不要只依赖旧参考。

## Workflow

### 1. Prepare Workspace

为每个视频创建独立输出目录，推荐：

```bash
python3 scripts/run_video_to_text.py \
  --input "/path/to/video.mp4" \
  --output-dir "/path/to/output"
```

脚本会自动：

- 在 `.venv` 缺失时运行 `scripts/bootstrap.py`。
- 安装 FunASR、ModelScope、Torch、imageio-ffmpeg 等依赖。
- 下载/准备 `FunAudioLLM/Fun-ASR-Nano-2512`。
- 生成 `audio.mp3`、`audio_16k.wav`、`transcript.txt`、`transcript.md`、`transcript.json`。

本机约束：

- 默认模型：`FunAudioLLM/Fun-ASR-Nano-2512`。
- 多语种才使用 `--profile mlt`：`FunAudioLLM/Fun-ASR-MLT-Nano-2512`。
- 加载模型需要 `trust_remote_code=True` 和本地 `.fun-asr-src/model.py`。
- FunASR 更适合 Python 3.10-3.12；不要直接依赖系统 Python 3.13。

### 2. Read Transcript

优先读 `transcript.md`。如果需要时间定位，读 `transcript.json`，里面有按分块记录的 `start` 和 `text`。

转写里通常会混有：

- 采访者提问、追问、现场引导。
- IP 的正式回答。
- NG、笑场、重说、导演判断、制作过程。

分析时要把“可成片内容”和“制作过程”分开。制作过程可以帮助理解哪个版本更真，但不要进入成片文案。做成片文案时，不要用自己的话总结 IP 的意思，只能从转写文本里截取原句。

### 3. Segment Candidates

先粗分候选片段，再精选 3-7 个推荐片段。每个候选片段都要尽量形成：

```text
[开头问题] → [IP回答] → [具体故事/细节] → [反转或升维] → [金句/余韵]
```

优先挑这些片段：

- 有一个观众会想回答的问题，适合用采访者问题开头。
- 有具体事件、数字、动作、对话或画面，而不是泛泛价值观。
- 有反差：有钱但节俭、嘴上拒绝但心里得意、年轻但成熟、被养育者开始反哺。
- 有角色反转：孩子养妈妈、学生变老师、普通人拥有不普通结果。
- 有“妈妈/父母/家庭/成功/钱/成长/亏欠/争气”等目标人群强情绪母题。
- 有可以压轴的短金句，观众能记住、转发、评论或代入。
- 片段长度适合短视频，通常 20-90 秒；极简金句型可以 6-15 秒。

避免推荐这些片段：

- 只有观点，没有具体故事、行为或对话支撑。
- 主要是导演引导、NG、试录、评价“这段能不能用”。
- 需要太多背景才能听懂。
- 情绪是装出来的，或者明显像背脚本。
- 有客户关系、隐私、价格、合同、法律、医疗、财务等高风险信息，未经 CEO 确认不能发布。

### 4. Score and Choose

给每个推荐片段打 1-5 分：

- 钩子强度：开头问题/反常识是否能让人停留。
- 故事密度：是否有具体事件、动作、数字、对话。
- 情绪强度：是否触发心疼、骄傲、亏欠、认同、羡慕或会心一笑。
- 转发潜力：是否有可被观众拿去表达自己的金句。
- 成片可剪性：是否能剪成清楚的问答结构，是否需要大量补背景。

只推荐总分高且可剪的片段。宁可少推，不要为了凑数量把弱片段塞进文档。

### 4.5. Mark Deletions

每个推荐片段都必须让用户看到“原来有什么、现在删了什么”。

做法：

1. 找到该片段在完整转写中的连续原文范围。
2. 按一句话一行拆开。拆行可以按标点、明显停顿或 8-20 字的自然语义断点，但不要改字。
3. 保留进入成片的句子，原样展示。
4. 删除的句子用 Markdown 删除线展示：`~~原句~~`。
5. 如果只是删除一句里的某个词或半句，也用删除线标注被删部分，但优先整句删除，方便剪辑执行。
6. 如果为了成片顺序调整了句子，先在“开头提问与挑选出的主要内容”里列最终顺序，再在“原文案”里按原素材顺序展示保留/删除对照。

### 5. Build Feishu Report

使用 `references/report-template.md` 组织内容。文档里必须包含：

- 基本信息。
- 推荐片段总览表。
- 每个推荐片段的“开头提问与挑选出的主要内容”。
- 每个推荐片段的“原文案”：一句话一行，删除内容必须画删除线。
- 每个推荐片段的“删除了哪些片段”：汇总删除内容和删除理由。
- 每个推荐片段的为什么选、怎么剪、风险。
- 完整原素材转写。

如果用户给了目标飞书文档，使用 `lark-cli docs +update --api-version v2` 追加或覆盖，按用户意图执行。

如果没有目标文档，创建新飞书文档：

```bash
lark-cli docs +create --api-version v2 --doc-format markdown --content "$(cat report.md)"
```

写飞书前如果涉及发布承诺、客户关系、公开传播或敏感素材，只先生成本地 `report.md`，并把“待 CEO 确认”列入风险，不要擅自发送或公开。

## Output Principles

- 先给结论：推荐哪几个片段，最强的是哪个。
- 解释要像剪辑复盘，不要像文学赏析。
- 输出文案时只做原话截取，不做润色改写。
- 每个片段都说明“为什么会爆”：钩子、刺点、情绪、转发/爱心/评论动机。
- 保留完整原素材转写，方便人工复核。
- 明确标注每个片段删掉了什么，帮助后期按原素材执行。

## Final Reply

最终回复给用户时说明：

- 已生成/更新的飞书文档链接或本地报告路径。
- 视频转写输出目录。
- 推荐片段数量和最强片段标题。
- 需要 CEO 判断的风险项。

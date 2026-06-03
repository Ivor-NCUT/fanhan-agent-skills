---
name: 视频文件提取文本
description: 将用户发来或指定路径的视频文件提取成文字稿。Use this skill whenever the user sends a video, gives a local video path, or asks to 从视频提取文本、视频转文字、视频转写、提取音频后转录、Fun-ASR-Nano 转写、把 mp4/mov 变成文稿、本地 ASR 提取文本. This skill should win over generic transcription when the input is a video file and the expected result is a plain text transcript, especially when the user mentions Fun-ASR-Nano or local transcription.
---

# 视频文件提取文本

## Purpose

把用户提供的视频文件转成可阅读文字稿：

1. 接收用户发来的视频或本地视频路径。
2. 调用 Python 脚本，从视频中分离音频，生成 `audio.mp3`。
3. 使用本机 Fun-ASR-Nano 模型转写音频。
4. 把文字稿输出给用户，并保留本地中间产物，方便复查。

这个 skill 只负责“视频 -> 音频 -> 文本”。不要顺手做字幕、剪辑、润色成文章、内容总结或飞书归档，除非用户明确要求。

## Inputs

支持常见视频格式：

- `.mp4`
- `.mov`
- `.m4v`
- `.mkv`
- `.avi`
- `.webm`

如果用户直接上传视频，先确认可访问的本地文件路径。如果当前环境只拿到了文件名或附件引用，但没有实际路径，先向用户要视频文件路径。

## Portable First-Time Setup

这个 skill 设计为可以开源分享。不要假设用户已经安装 Python 环境、FunASR 依赖、模型权重或 FFmpeg。

第一次在一台新机器上运行时，Agent 应该主动从 skill 目录执行：

```bash
python3 scripts/bootstrap.py
```

默认行为：

- 创建本地 `.venv`。
- 安装 `funasr`、`modelscope`、`torch`、`torchaudio`、`openai-whisper`、`imageio-ffmpeg` 等依赖。
- 从官方 GitHub 获取 Fun-ASR remote code 到 `.fun-asr-src/`。
- 预下载默认 base 模型：`FunAudioLLM/Fun-ASR-Nano-2512`。

如果用户只想先装依赖、不想立刻下载大模型：

```bash
python3 scripts/bootstrap.py --download-model none
```

如果用户需要多语种模型：

```bash
python3 scripts/bootstrap.py --download-model mlt
```

如果需要同时下载 base 和 MLT：

```bash
python3 scripts/bootstrap.py --download-model all
```

FunASR 依赖更适合 Python 3.10-3.12；如果当前系统 Python 太新，脚本会优先尝试 `python3.11`，再尝试 `uv` 创建 Python 3.11 环境。没有 Python 3.10-3.12 且没有 `uv` 时，再请用户安装 Python 3.11 或 `uv`。

本机已验证的关键约束：

- Fun-ASR-Nano 模型名使用 `FunAudioLLM/Fun-ASR-Nano-2512`。
- 截至 2026-05-19，官方 FunAudioLLM / Fun-ASR 主线仍以 `2512` 为最新 Nano 版本；本机缓存已刷新到 Hugging Face `a7088d620f755dcdca575b63db184c3ad55b2865` / ModelScope `master`。
- 如果用户的视频主要是中文、英文、日文或中文方言，默认使用 `base`：`FunAudioLLM/Fun-ASR-Nano-2512`。
- 如果用户明确需要韩语、越南语、印尼语、泰语、马来语、菲律宾语、阿拉伯语、印地语或更多欧洲语种，使用 `mlt`：`FunAudioLLM/Fun-ASR-MLT-Nano-2512`。
- 加载模型时使用 `trust_remote_code=True`。
- 这版模型需要本地 `remote_code`，默认路径是 skill 内的 `.fun-asr-src/model.py`。
- 不要把模型名写成 `iic/Fun-ASR-Nano-2512`。
- 不要直接依赖系统 Python 3.13 跑 ASR 环境。

## One-Command Use

优先使用一键脚本。它会在 `.venv` 缺失时自动运行 bootstrap，再完成抽音频和转写：

```bash
python3 scripts/run_video_to_text.py \
  --input "/path/to/video.mp4"
```

默认输出目录：

```text
/path/to/video-transcript/
```

如果用户明确指定输出目录：

```bash
python3 scripts/run_video_to_text.py \
  --input "/path/to/video.mp4" \
  --output-dir "/path/to/output"
```

多语种视频：

```bash
python3 scripts/run_video_to_text.py \
  --profile mlt \
  --input "/path/to/video.mp4"
```

## Workflow

如果一键脚本失败，或需要分步排查，再按下面的手动 workflow 执行。

### 1. Prepare Output Folder

为每个视频创建独立输出目录，推荐命名：

```text
<video-stem>-transcript/
```

例如：

```bash
mkdir -p "/path/to/video-transcript"
```

### 2. Extract Audio

调用脚本从视频生成两份音频：

- `audio.mp3`：满足用户要求，也便于人工复听。
- `audio_16k.wav`：16k 单声道 WAV，给 Fun-ASR-Nano 转写使用。

```bash
.venv/bin/python scripts/extract_audio.py \
  --input "/path/to/video.mp4" \
  --output-dir "/path/to/video-transcript"
```

### 3. Transcribe with Fun-ASR-Nano

```bash
.venv/bin/python scripts/transcribe_nano.py \
  --audio "/path/to/video-transcript/audio_16k.wav" \
  --output-dir "/path/to/video-transcript"
```

如果需要多语种 MLT 版本：

```bash
.venv/bin/python scripts/transcribe_nano.py \
  --profile mlt \
  --audio "/path/to/video-transcript/audio_16k.wav" \
  --output-dir "/path/to/video-transcript"
```

脚本会输出：

- `transcript.txt`：纯文字，默认直接发给用户。
- `transcript.md`：带来源、模型和正文标题的 Markdown 版本。
- `transcript.json`：内部记录，包含分块信息和原始返回，方便排查。

长音频默认按 30 秒切块再逐段转写。这比把整段音频直接喂给模型更稳定，也能绕开 VAD/长音频合并时的兼容性问题。

### 4. Return Text to User

最终回复优先直接给用户正文。如果正文很长：

- 先给简短说明和 `transcript.md` 的本地路径。
- 再贴出开头一段和全文所在文件。
- 不要只说“已生成”，用户要的是文字结果。

推荐回复结构：

```markdown
已完成视频转写。

转写文件：/absolute/path/to/transcript.md

正文：
[转写正文]
```

## Quality Checks

交付前检查：

- 如果 `.venv` 不存在，先运行 `scripts/bootstrap.py`，不要直接把缺依赖问题丢给用户。
- 如果 `.fun-asr-src/model.py` 不存在，运行 `scripts/bootstrap.py --refresh-remote-code`。
- `audio.mp3` 已生成，且大小大于 0。
- `audio_16k.wav` 已生成，且大小大于 0。
- `transcript.txt` 或 `transcript.md` 已生成，且正文不是空字符串。
- 如果转写失败，明确说明卡在哪一步：抽音频、加载模型、切块、转写、写文件。

## Troubleshooting

- `Download ... iic/Fun-ASR-Nano-2512 failed`：模型名错了，改用 `FunAudioLLM/Fun-ASR-Nano-2512`。
- 想确认模型是否有更新：优先查官方 GitHub `FunAudioLLM/Fun-ASR`、Hugging Face `FunAudioLLM/Fun-ASR-Nano-2512` 和 ModelScope `FunAudioLLM/Fun-ASR-Nano-2512`，不要只看第三方封装名。
- `Loading remote code failed: ./model.py`：缺少 `.fun-asr-src/model.py`，先运行 `scripts/bootstrap.py --refresh-remote-code`。
- `UnboundLocalError` 出现在 `whisper_tokenizer.py`：补装 `openai-whisper` 后重试。
- `ffmpeg not found`：脚本优先使用 `imageio-ffmpeg` 内置 ffmpeg；如果仍失败，再安装系统 ffmpeg。
- 转写结果明显断裂：保持 30 秒分块，必要时用 `--chunk-seconds 20` 重跑。

## Open Source Packaging Notes

如果把这个 skill 发布到 GitHub：

- 提交 `SKILL.md`、`scripts/`、`requirements.txt`、`.gitignore`、`references/` 和 `.fun-asr-src/`。
- 不要提交 `.venv/`、模型缓存、转写输出、`audio.mp3`、`audio_16k.wav` 或 `audio_chunks/`。
- 大模型权重交给 `scripts/bootstrap.py --download-model ...` 在用户机器上下载。
- 如果不想 vendoring `.fun-asr-src/`，也可以不提交它；bootstrap 会从官方 GitHub 拉取。

## Boundaries

需要升级给用户确认的情况：

- 用户想把转写结果发给客户、发布到公开平台或写入正式知识库。
- 视频涉及客户隐私、合同、价格、医疗、法律、财务等高风险信息。
- 用户要求删除原视频或中间音频文件。

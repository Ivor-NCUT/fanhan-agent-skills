---
name: heuristic-interview-rough-cut-fanhan
description: 用于“启发式访谈”口播短视频素材的本地粗剪工作流。Use when the user asks for 启发式访谈口播粗剪@泛函, interview talking-head rough cuts, local FunASR transcription with sentence timestamps, or cutting and reordering video clips from a transcript.
---

# 启发式访谈口播粗剪@泛函

## Purpose

Turn raw heuristic-interview talking-head footage into a rough-cut video:

1. Extract audio from the uploaded video.
2. Transcribe locally with FunASR and sentence-level timestamps.
3. Send the clean transcript text to the user while keeping timestamp data in `transcript.json`.
4. Let the user choose kept/deleted/reordered clips.
5. Cut numbered clips and concatenate them into one complete rough-cut `.mp4`.

This skill is for rough cutting only. Do not add subtitles, covers, transitions, denoise, color grading, or visual packaging unless the user explicitly asks.

## Required Questions

Before running scripts, ask the user for:

- Operating system: macOS or Windows.
- Raw video path.
- Customer name.
- Project name.
- Shoot date.

Do not invent the customer name, project name, or shoot date. If any of them are missing, ask before final rendering.

Supported input formats: `.mp4`, `.mov`, `.m4v`, `.avi`, `.mkv`.

Final output format: `.mp4`.

## First-Time Setup

Run the bootstrap script once from this skill directory. It creates a local `.venv` and installs the Python packages needed for FunASR and MoviePy.

macOS:

```bash
python3 scripts/bootstrap.py
```

Windows:

```powershell
py -3.11 scripts\bootstrap.py
```

If Python 3.10, 3.11, or 3.12 is not available, the bootstrap script tries to use `uv` to create a Python 3.11 environment automatically. If that also fails, ask the user to install Python 3.11. Avoid Python 3.13 for this workflow because ASR dependencies may lag behind the newest Python release.

The scripts use `imageio-ffmpeg` so a separate system FFmpeg install is usually not required.

## Workflow

### 1. Prepare Audio

Extract both:

- `audio.mp3` for user-facing review and archive.
- `audio_16k.wav` for ASR stability.

macOS:

```bash
.venv/bin/python scripts/prepare_audio.py --input "/path/to/video.mp4" --output-dir "/path/to/output"
```

Windows:

```powershell
.venv\Scripts\python scripts\prepare_audio.py --input "C:\path\to\video.mp4" --output-dir "C:\path\to\output"
```

### 2. Transcribe

Use the prepared `audio_16k.wav` and generate both `transcript.json` and `transcript.md`.

macOS:

```bash
.venv/bin/python scripts/transcribe.py --audio "/path/to/output/audio_16k.wav" --output-dir "/path/to/output"
```

Windows:

```powershell
.venv\Scripts\python scripts\transcribe.py --audio "C:\path\to\output\audio_16k.wav" --output-dir "C:\path\to\output"
```

Send the user `transcript.md` in this format, without timestamps:

```markdown
转写内容……
转写内容……
转写内容……
```

Ask the user to reply with kept segments, order, and any title preferences. Preferred user format:

```text
保留 00:01:12-00:01:38，前置，标题：为什么老板不该自己写脚本
保留 00:03:02-00:03:29，后置，标题：客户真正卡住的不是流量
删除 00:02:10-00:02:44
```

Use `transcript.json` internally when converting the user's kept/deleted/reordered choices into a JSON cut plan.

### 3. Create Cut Plan

Create a `cut_plan.json` file:

```json
{
  "customer": "客户名",
  "project": "项目名",
  "shoot_date": "2026-05-06",
  "padding_seconds": 0.3,
  "clips": [
    {
      "start": "00:01:12",
      "end": "00:01:38",
      "title": "为什么老板不该自己写脚本"
    }
  ]
}
```

Rules:

- Default `padding_seconds` is `0.3`.
- Apply padding by moving start 0.3 seconds earlier and end 0.3 seconds later.
- Clamp padded times to the video start/end.
- Preserve the user-specified order.
- Generate missing titles from clip content: short, spoken, opinionated, under 20 Chinese characters when possible.
- Strip filename-invalid characters.

### 4. Rough Cut and Concatenate

macOS:

```bash
.venv/bin/python scripts/rough_cut.py --input "/path/to/video.mp4" --plan "/path/to/output/cut_plan.json" --output-dir "/path/to/output/rough_cut"
```

Windows:

```powershell
.venv\Scripts\python scripts\rough_cut.py --input "C:\path\to\video.mp4" --plan "C:\path\to\output\cut_plan.json" --output-dir "C:\path\to\output\rough_cut"
```

Output files:

- Numbered fragments: `01_标题_客户名_项目名_拍摄日期.mp4`
- Complete rough cut: `00_粗剪合集_客户名_项目名_拍摄日期.mp4`

## Quality Bar

Before final response:

- Confirm every retained segment has a valid start/end.
- Confirm the order matches the user's instruction.
- Confirm the padded ranges do not exceed the source duration.
- Confirm numbered clip files and the complete rough-cut file exist.
- Tell the user where the final video and fragments are.

If rendering fails because of codec, memory, or dependency issues, report the exact failing step and retry once with a more conservative MoviePy preset or fewer concurrent threads.

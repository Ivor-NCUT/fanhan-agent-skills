# 视频文件提取文本

把视频文件转成文字稿的 Codex / Agent skill。

## What it does

1. 接收视频路径。
2. 从视频中提取 `audio.mp3` 和 `audio_16k.wav`。
3. 使用本地 Fun-ASR-Nano 转写。
4. 输出 `transcript.txt`、`transcript.md` 和 `transcript.json`。

## First run

在新机器上第一次使用时，让 Agent 在 skill 目录执行：

```bash
python3 scripts/bootstrap.py
```

这会自动：

- 创建 `.venv`
- 安装 Python 依赖
- 获取 Fun-ASR remote code
- 下载默认模型 `FunAudioLLM/Fun-ASR-Nano-2512`

如果暂时不想下载模型：

```bash
python3 scripts/bootstrap.py --download-model none
```

如果需要多语种模型：

```bash
python3 scripts/bootstrap.py --download-model mlt
```

## One-command transcription

```bash
python3 scripts/run_video_to_text.py --input "/path/to/video.mp4"
```

多语种视频：

```bash
python3 scripts/run_video_to_text.py --profile mlt --input "/path/to/video.mp4"
```

## Do not commit

`.gitignore` 已排除：

- `.venv/`
- 模型缓存
- 音频中间文件
- 转写输出
- Python cache

模型权重不应该提交到 GitHub；让 `scripts/bootstrap.py` 在用户机器上下载。

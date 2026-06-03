# 口播视频粗剪@方比比

采访式 IP 口播粗剪工作流：视频抽音频、本地 Fun-ASR-Nano 转写、爆款片段挑选、飞书文档报告。

这个 skill 面向“镜头外采访，IP 回答，后期从问答中剪爆款口播”的生产场景。它不是普通转写工具，而是帮助剪辑师判断哪些片段值得剪，并输出可审查的原文对照。

## 核心规则

- 只做剪辑判断，不润色、不改写 IP 原话。
- 只能做保留、删除、调顺序。
- 报告必须展示“开头提问与挑选出的主要内容”。
- 报告必须展示“原文案”，一句话一行，删掉的内容用删除线标出。
- 报告必须说明“删除了哪些片段”和删除原因。

## 工作流

1. 接收本地视频路径。
2. 运行 `scripts/run_video_to_text.py`，生成音频与转写文本。
3. 根据 `references/fangbibi-viral-patterns.md` 识别爆款片段。
4. 根据 `references/report-template.md` 生成飞书报告。

## 依赖

首次运行会自动创建 `.venv` 并安装 FunASR 相关依赖。默认模型：

```text
FunAudioLLM/Fun-ASR-Nano-2512
```

运行环境更适合 Python 3.10-3.12；脚本会优先尝试 Python 3.11 或 `uv`。

## 打包文件

仓库中的 `dist/fangbibi-talking-head-rough-cut.skill` 是已打包版本，可用于安装分发。

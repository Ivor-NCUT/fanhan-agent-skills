#!/usr/bin/env python3
"""Transcribe audio with local Fun-ASR-Nano and write text files."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
MODEL_PROFILES = {
    "base": "FunAudioLLM/Fun-ASR-Nano-2512",
    "mlt": "FunAudioLLM/Fun-ASR-MLT-Nano-2512",
}
DEFAULT_REMOTE_CODE = SKILL_DIR / ".fun-asr-src" / "model.py"


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ModuleNotFoundError:
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            return ffmpeg_path
        raise SystemExit("ffmpeg is required. Run scripts/bootstrap.py or install ffmpeg.")


def probe_duration(audio: Path) -> float:
    proc = subprocess.run(
        [
            ffmpeg(),
            "-hide_banner",
            "-i",
            str(audio),
        ],
        capture_output=True,
        text=True,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not match:
        return 0.0
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def make_chunks(audio: Path, output_dir: Path, chunk_seconds: int) -> list[dict]:
    chunk_dir = output_dir / "audio_chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(audio)
    chunks: list[dict] = []
    start = 0.0
    idx = 0

    while start < duration or (duration == 0 and idx == 0):
        chunk = chunk_dir / f"{idx:04d}.wav"
        args = [
            "-ss",
            str(start),
            "-t",
            str(chunk_seconds),
            "-i",
            str(audio),
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(chunk),
        ]
        subprocess.check_call([ffmpeg(), "-y", "-v", "error", *args])
        if chunk.exists() and chunk.stat().st_size > 0:
            chunks.append({"index": idx, "start": start, "path": str(chunk)})
        start += chunk_seconds
        idx += 1
        if duration == 0:
            break

    return chunks


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    replacements = {
        " 。": "。",
        " ，": "，",
        " ？": "？",
        " ！": "！",
        " 、": "、",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def paragraphs(text: str, max_chars: int = 420) -> str:
    parts = [part.strip() for part in re.split(r"(?<=[。！？!?])", text) if part.strip()]
    if not parts:
        return text

    out: list[str] = []
    buf = ""
    for part in parts:
        if not buf:
            buf = part
        elif len(buf) + len(part) <= max_chars:
            buf += part
        else:
            out.append(buf)
            buf = part
    if buf:
        out.append(buf)
    return "\n\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe 16 kHz wav with Fun-ASR-Nano.")
    parser.add_argument("--audio", required=True, help="16 kHz mono wav path")
    parser.add_argument("--output-dir", required=True, help="Output folder")
    parser.add_argument("--profile", choices=sorted(MODEL_PROFILES), default="base")
    parser.add_argument("--model", default="", help="Override model id or local model path")
    parser.add_argument("--remote-code", default=str(DEFAULT_REMOTE_CODE))
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--hub", choices=["", "ms", "hf"], default="")
    parser.add_argument("--chunk-seconds", type=int, default=30)
    parser.add_argument("--language", default="中文")
    args = parser.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        raise SystemExit(f"Audio not found: {audio_path}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    remote_code = Path(args.remote_code).expanduser().resolve()
    if not remote_code.exists():
        raise SystemExit(
            f"Fun-ASR-Nano remote code not found: {remote_code}. "
            "Run scripts/bootstrap.py or copy .fun-asr-src into the skill directory."
        )

    try:
        from funasr import AutoModel
    except ModuleNotFoundError as exc:
        raise SystemExit("FunASR is missing. Run scripts/bootstrap.py first.") from exc

    model_id = args.model or MODEL_PROFILES[args.profile]
    model_kwargs = {
        "model": model_id,
        "trust_remote_code": True,
        "remote_code": str(remote_code),
        "device": args.device,
        "disable_update": True,
    }
    if args.hub:
        model_kwargs["hub"] = args.hub

    print(f"[model] loading {model_id}", flush=True)
    model = AutoModel(**model_kwargs)

    chunks = make_chunks(audio_path, output_dir, args.chunk_seconds)
    texts: list[str] = []
    chunk_results: list[dict] = []

    for pos, chunk in enumerate(chunks, start=1):
        print(f"[asr] chunk {pos}/{len(chunks)}", flush=True)
        result = model.generate(
            input=[chunk["path"]],
            cache={},
            batch_size=1,
            language=args.language,
            itn=True,
        )
        text = ""
        if result and isinstance(result, list):
            text = str(result[0].get("text", ""))
        text = clean_text(text)
        texts.append(text)
        chunk_results.append({**chunk, "text": text, "raw_result": result})

    full_text = clean_text(" ".join(part for part in texts if part))
    if not full_text:
        raise SystemExit("Transcription finished but produced empty text.")

    txt_path = output_dir / "transcript.txt"
    md_path = output_dir / "transcript.md"
    json_path = output_dir / "transcript.json"

    txt_path.write_text(paragraphs(full_text) + "\n", encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# 视频转写文字稿",
                "",
                f"- 音频文件：`{audio_path}`",
                f"- 转写模型：`{model_id}`",
                f"- 模型配置：`{args.profile}`",
                f"- 分块长度：{args.chunk_seconds} 秒",
                "",
                "## 转写正文",
                "",
                paragraphs(full_text),
                "",
            ]
        ),
        encoding="utf-8",
    )
    json_path.write_text(
        json.dumps(
            {
                "audio": str(audio_path),
                "model": model_id,
                "profile": args.profile,
                "remote_code": str(remote_code),
                "device": args.device,
                "hub": args.hub,
                "chunk_seconds": args.chunk_seconds,
                "chunks": chunk_results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(txt_path)
    print(md_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Transcribe audio with local FunASR and write sentence-level transcript files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from funasr import AutoModel


def ffprobe_duration(path: Path) -> float:
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-hide_banner",
        "-i",
        str(path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not match:
        return 0.0
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def normalize_sentence(item: dict, index: int) -> dict:
    text = str(item.get("text") or item.get("sentence") or "").strip()
    start = item.get("start") or item.get("start_time") or item.get("begin")
    end = item.get("end") or item.get("end_time") or item.get("finish")
    timestamp = item.get("timestamp")
    if (start is None or end is None) and isinstance(timestamp, list) and len(timestamp) >= 2:
        start, end = timestamp[0], timestamp[1]
    start_s = float(start or 0) / 1000.0
    end_s = float(end or 0) / 1000.0
    return {"id": index, "start": start_s, "end": end_s, "text": text}


def sentence_segments(result: list[dict], duration: float) -> list[dict]:
    if not result:
        return []
    first = result[0]
    sentence_info = first.get("sentence_info")
    if isinstance(sentence_info, list) and sentence_info:
        return [normalize_sentence(item, idx + 1) for idx, item in enumerate(sentence_info)]

    text = str(first.get("text") or "").strip()
    if not text:
        return []
    parts = [part.strip() for part in re.split(r"(?<=[。！？!?])", text) if part.strip()]
    if not parts:
        parts = [text]
    avg = duration / max(len(parts), 1) if duration else 0
    return [
        {"id": idx + 1, "start": idx * avg, "end": (idx + 1) * avg, "text": part}
        for idx, part in enumerate(parts)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True, help="16 kHz mono wav path")
    parser.add_argument("--output-dir", required=True, help="Directory for transcript files")
    parser.add_argument("--model", default="paraformer-zh")
    parser.add_argument("--vad-model", default="fsmn-vad")
    parser.add_argument("--punc-model", default="ct-punc")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--hotword", default="")
    args = parser.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        raise SystemExit(f"Audio not found: {audio_path}")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    model = AutoModel(
        model=args.model,
        vad_model=args.vad_model,
        punc_model=args.punc_model,
        device=args.device,
    )
    result = model.generate(
        input=str(audio_path),
        batch_size_s=300,
        sentence_timestamp=True,
        hotword=args.hotword,
    )

    duration = ffprobe_duration(audio_path)
    segments = sentence_segments(result, duration)
    payload = {
        "audio": str(audio_path),
        "model": args.model,
        "vad_model": args.vad_model,
        "punc_model": args.punc_model,
        "duration": duration,
        "segments": segments,
        "raw_result": result,
    }

    json_path = output_dir / "transcript.json"
    md_path = output_dir / "transcript.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines: list[str] = []
    for seg in segments:
        lines.append(seg["text"])
    md_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    print(json_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

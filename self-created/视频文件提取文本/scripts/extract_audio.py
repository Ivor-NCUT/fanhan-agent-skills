#!/usr/bin/env python3
"""Extract mp3 and 16 kHz mono wav audio from a video file."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SUPPORTED_VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm"}


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ModuleNotFoundError:
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            return ffmpeg
        raise SystemExit("ffmpeg is required. Run scripts/bootstrap.py or install ffmpeg.")


def run_ffmpeg(args: list[str]) -> None:
    subprocess.check_call([ffmpeg_exe(), "-y", "-v", "error", *args])


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract audio from video.")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--output-dir", required=True, help="Output folder")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input video not found: {input_path}")
    if input_path.suffix.lower() not in SUPPORTED_VIDEO_EXTS:
        raise SystemExit(f"Unsupported video format: {input_path.suffix}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    mp3_path = output_dir / "audio.mp3"
    wav_path = output_dir / "audio_16k.wav"

    run_ffmpeg(["-i", str(input_path), "-vn", "-ac", "1", "-ar", "44100", "-b:a", "192k", str(mp3_path)])
    run_ffmpeg(["-i", str(input_path), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(wav_path)])

    if not mp3_path.exists() or mp3_path.stat().st_size == 0:
        raise SystemExit(f"Failed to create mp3: {mp3_path}")
    if not wav_path.exists() or wav_path.stat().st_size == 0:
        raise SystemExit(f"Failed to create wav: {wav_path}")

    print(mp3_path)
    print(wav_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Extract mp3 archive audio and 16 kHz mono wav for ASR."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import imageio_ffmpeg


SUPPORTED = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}


def run_ffmpeg(args: list[str]) -> None:
    subprocess.check_call([imageio_ffmpeg.get_ffmpeg_exe(), "-y", *args])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Raw video path")
    parser.add_argument("--output-dir", required=True, help="Directory for audio files")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if input_path.suffix.lower() not in SUPPORTED:
        raise SystemExit(f"Unsupported video format: {input_path.suffix}")
    if not input_path.exists():
        raise SystemExit(f"Input video not found: {input_path}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    mp3_path = output_dir / "audio.mp3"
    wav_path = output_dir / "audio_16k.wav"

    run_ffmpeg(["-i", str(input_path), "-vn", "-ac", "1", "-ar", "44100", "-b:a", "192k", str(mp3_path)])
    run_ffmpeg(["-i", str(input_path), "-vn", "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", str(wav_path)])

    print(mp3_path)
    print(wav_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""One-command video to transcript runner.

This script is intentionally small orchestration glue. It bootstraps the local
environment if needed, extracts audio, then transcribes with Fun-ASR-Nano.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENV_DIR = SKILL_DIR / ".venv"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


def env_ready(py: Path) -> bool:
    if not py.exists():
        return False
    probe = "import funasr, modelscope, imageio_ffmpeg"
    return subprocess.run([str(py), "-c", probe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def ensure_bootstrap(profile: str, skip_model_download: bool) -> Path:
    py = venv_python()
    if env_ready(py):
        return py

    bootstrap_cmd = [sys.executable, str(SCRIPTS_DIR / "bootstrap.py")]
    if skip_model_download:
        bootstrap_cmd.extend(["--download-model", "none"])
    else:
        bootstrap_cmd.extend(["--download-model", profile])
    run(bootstrap_cmd)
    return py


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from a video file.")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--output-dir", default="", help="Output folder; defaults to <video-stem>-transcript")
    parser.add_argument("--profile", choices=["base", "mlt"], default="base")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--language", default="中文")
    parser.add_argument("--chunk-seconds", type=int, default=30)
    parser.add_argument("--skip-model-download", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input video not found: {input_path}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else input_path.with_suffix("").parent / f"{input_path.stem}-transcript"
    output_dir.mkdir(parents=True, exist_ok=True)

    py = ensure_bootstrap(args.profile, args.skip_model_download)

    run(
        [
            str(py),
            str(SCRIPTS_DIR / "extract_audio.py"),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
        ]
    )
    run(
        [
            str(py),
            str(SCRIPTS_DIR / "transcribe_nano.py"),
            "--profile",
            args.profile,
            "--audio",
            str(output_dir / "audio_16k.wav"),
            "--output-dir",
            str(output_dir),
            "--device",
            args.device,
            "--language",
            args.language,
            "--chunk-seconds",
            str(args.chunk_seconds),
        ]
    )

    print(output_dir / "transcript.txt")
    print(output_dir / "transcript.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

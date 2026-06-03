#!/usr/bin/env python3
"""Create a local Python environment for video-to-text transcription."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import venv
import zipfile
from pathlib import Path
from urllib.request import urlretrieve


SKILL_DIR = Path(__file__).resolve().parents[1]
VENV_DIR = SKILL_DIR / ".venv"
REMOTE_CODE_DIR = SKILL_DIR / ".fun-asr-src"
FUN_ASR_GITHUB = "https://github.com/FunAudioLLM/Fun-ASR.git"
FUN_ASR_ZIP = "https://github.com/FunAudioLLM/Fun-ASR/archive/refs/heads/main.zip"
MODEL_PROFILES = {
    "base": "FunAudioLLM/Fun-ASR-Nano-2512",
    "mlt": "FunAudioLLM/Fun-ASR-MLT-Nano-2512",
}

PACKAGES = [
    "pip>=24.0",
    "setuptools",
    "wheel",
    "funasr>=1.2.0",
    "modelscope>=1.20.0",
    "torch",
    "torchaudio",
    "soundfile>=0.12.1",
    "librosa",
    "openai-whisper",
    "imageio-ffmpeg>=0.5.0",
    "numpy",
    "transformers",
    "huggingface_hub",
]


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def supported_python() -> bool:
    return (sys.version_info.major, sys.version_info.minor) in {(3, 10), (3, 11), (3, 12)}


def reexec_with_supported_python() -> None:
    candidates: list[list[str]]
    if os.name == "nt":
        candidates = [["py", "-3.11"], ["py", "-3.10"], ["py", "-3.12"]]
    else:
        candidates = [["python3.11"], ["python3.10"], ["python3.12"]]

    for candidate in candidates:
        exe = shutil.which(candidate[0])
        if exe:
            cmd = [exe, *candidate[1:], str(Path(__file__).resolve()), *sys.argv[1:]]
            print(f"Re-running bootstrap with supported Python: {' '.join(cmd)}")
            raise SystemExit(subprocess.call(cmd))


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


def ensure_remote_code(refresh: bool = False) -> None:
    if (REMOTE_CODE_DIR / "model.py").exists() and not refresh:
        return

    if refresh and REMOTE_CODE_DIR.exists():
        shutil.rmtree(REMOTE_CODE_DIR)

    sibling_remote_code = SKILL_DIR.parent / "视频文件提取文本" / ".fun-asr-src"
    if (sibling_remote_code / "model.py").exists() and not refresh:
        print(f"Using local Fun-ASR remote code fallback: {sibling_remote_code}", flush=True)
        shutil.copytree(sibling_remote_code, REMOTE_CODE_DIR, dirs_exist_ok=True)
        return

    git = shutil.which("git")
    if git:
        tmp = SKILL_DIR / ".tmp-fun-asr"
        if tmp.exists():
            shutil.rmtree(tmp)
        try:
            run([git, "clone", "--depth", "1", FUN_ASR_GITHUB, str(tmp)])
            shutil.copytree(tmp, REMOTE_CODE_DIR, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
            commit = subprocess.check_output([git, "-C", str(tmp), "rev-parse", "HEAD"], text=True).strip()
            (REMOTE_CODE_DIR / "VERSION_SOURCE_COMMIT.txt").write_text(commit + "\n", encoding="utf-8")
            shutil.rmtree(tmp)
            return
        except subprocess.CalledProcessError:
            print("Git clone failed; falling back to GitHub zip download.", flush=True)
            if tmp.exists():
                shutil.rmtree(tmp)

    zip_path = SKILL_DIR / ".tmp-fun-asr.zip"
    tmp_dir = SKILL_DIR / ".tmp-fun-asr-zip"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    print(f"Downloading Fun-ASR remote code: {FUN_ASR_ZIP}", flush=True)
    urlretrieve(FUN_ASR_ZIP, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(tmp_dir)
    extracted = next(tmp_dir.iterdir())
    shutil.copytree(extracted, REMOTE_CODE_DIR, dirs_exist_ok=True)
    zip_path.unlink(missing_ok=True)
    shutil.rmtree(tmp_dir)


def download_model(py: Path, profile: str) -> None:
    model_id = MODEL_PROFILES[profile]
    code = (
        "from modelscope import snapshot_download\n"
        f"path = snapshot_download({model_id!r}, revision='master')\n"
        "print(path)\n"
    )
    run([str(py), "-c", code])


def install_with_uv(uv: str, refresh_remote_code: bool, download_models: list[str]) -> int:
    print("Creating Python 3.11 environment with uv.")
    run([uv, "venv", "--python", "3.11", str(VENV_DIR)])
    py = venv_python()
    run([uv, "pip", "install", "--python", str(py), "--upgrade", *PACKAGES])
    ensure_remote_code(refresh=refresh_remote_code)
    for profile in download_models:
        download_model(py, profile)
    print(f"Done. Use this Python: {py}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap local video-to-text ASR dependencies.")
    parser.add_argument(
        "--download-model",
        choices=["none", "base", "mlt", "all"],
        default="base",
        help="Pre-download model weights. Use none to skip large downloads.",
    )
    parser.add_argument(
        "--refresh-remote-code",
        action="store_true",
        help="Refresh bundled Fun-ASR remote code from GitHub main.",
    )
    args = parser.parse_args()

    download_models = []
    if args.download_model == "all":
        download_models = ["base", "mlt"]
    elif args.download_model != "none":
        download_models = [args.download_model]

    if not supported_python():
        reexec_with_supported_python()
        uv = shutil.which("uv")
        if uv:
            return install_with_uv(uv, args.refresh_remote_code, download_models)
        version = sys.version_info
        print(
            "Python 3.10, 3.11, or 3.12 is recommended for FunASR. "
            f"Current Python is {version.major}.{version.minor}.{version.micro}.",
            file=sys.stderr,
        )
        return 2

    if not VENV_DIR.exists():
        print(f"Creating virtual environment: {VENV_DIR}")
        venv.EnvBuilder(with_pip=True, clear=False).create(VENV_DIR)

    py = venv_python()
    run([str(py), "-m", "pip", "install", "--upgrade", *PACKAGES])
    ensure_remote_code(refresh=args.refresh_remote_code)
    for profile in download_models:
        download_model(py, profile)
    print(f"Done. Use this Python: {py}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create a local virtual environment and install rough-cut dependencies."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VENV_DIR = SKILL_DIR / ".venv"

PACKAGES = [
    "pip>=24.0",
    "setuptools",
    "wheel",
    "funasr>=1.2.0",
    "modelscope>=1.20.0",
    "moviepy>=2.0.0",
    "imageio-ffmpeg>=0.5.0",
    "soundfile>=0.12.1",
    "numpy",
]


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def is_supported_python() -> bool:
    version = sys.version_info
    return (version.major, version.minor) in {(3, 10), (3, 11), (3, 12)}


def reexec_with_supported_python() -> bool:
    candidates = []
    if os.name == "nt":
        candidates.extend([["py", "-3.11"], ["py", "-3.10"], ["py", "-3.12"]])
    else:
        candidates.extend([["python3.11"], ["python3.10"], ["python3.12"]])

    for candidate in candidates:
        exe = shutil.which(candidate[0])
        if not exe:
            continue
        cmd = [exe, *candidate[1:], str(Path(__file__).resolve())]
        print(f"Re-running bootstrap with supported Python: {' '.join(cmd)}")
        raise SystemExit(subprocess.call(cmd))
    return False


def main() -> int:
    if not is_supported_python():
        reexec_with_supported_python()
        uv = shutil.which("uv")
        if uv:
            print("No supported system Python found. Creating a Python 3.11 environment with uv.")
            subprocess.check_call([uv, "venv", "--python", "3.11", str(VENV_DIR)])
            py = venv_python()
            subprocess.check_call([uv, "pip", "install", "--python", str(py), "--upgrade", *PACKAGES])
            print(f"Done. Use this Python for the workflow: {py}")
            return 0
        version = sys.version_info
        print(
            "Python 3.10, 3.11, or 3.12 is recommended for FunASR dependencies. "
            f"Current Python is {version.major}.{version.minor}.{version.micro}.",
            file=sys.stderr,
        )
        return 2

    if not VENV_DIR.exists():
        print(f"Creating virtual environment: {VENV_DIR}")
        venv.EnvBuilder(with_pip=True, clear=False).create(VENV_DIR)

    py = venv_python()
    print("Upgrading installer tools...")
    subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    print("Installing ASR and video packages. The first run can take a while.")
    subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", *PACKAGES])

    print(f"Done. Use this Python for the workflow: {py}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

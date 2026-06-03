#!/usr/bin/env python3
"""Cut ordered clips from a plan and concatenate them into one rough-cut video."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips


INVALID_FILENAME_CHARS = r'<>:"/\|?*'


def parse_time(value: str | int | float) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    parts = str(value).strip().split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return float(parts[0])


def clean_name(value: str, fallback: str) -> str:
    value = (value or fallback).strip()
    for ch in INVALID_FILENAME_CHARS:
        value = value.replace(ch, "")
    value = re.sub(r"\s+", "", value)
    value = value.strip("._- ")
    return value or fallback


def render_clip(source: VideoFileClip, start: float, end: float, output: Path) -> VideoFileClip:
    clip = source.subclipped(start, end)
    clip.write_videofile(
        str(output),
        fps=source.fps,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4,
        logger=None,
    )
    clip.close()
    return VideoFileClip(str(output))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Raw video path")
    parser.add_argument("--plan", required=True, help="cut_plan.json path")
    parser.add_argument("--output-dir", required=True, help="Directory for rendered clips")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    plan_path = Path(args.plan).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    customer = clean_name(plan.get("customer", ""), "客户名")
    project = clean_name(plan.get("project", ""), "项目名")
    shoot_date = clean_name(plan.get("shoot_date", ""), "拍摄日期")
    padding = float(plan.get("padding_seconds", 0.3))
    clips = plan.get("clips") or []
    if not clips:
        raise SystemExit("No clips found in cut plan.")

    source = VideoFileClip(str(input_path))
    rendered: list[VideoFileClip] = []
    manifest: list[dict] = []

    try:
        for idx, item in enumerate(clips, start=1):
            raw_start = parse_time(item["start"])
            raw_end = parse_time(item["end"])
            if raw_end <= raw_start:
                raise SystemExit(f"Invalid time range for clip {idx}: {item}")
            start = max(0.0, raw_start - padding)
            end = min(float(source.duration), raw_end + padding)
            if math.isclose(start, end) or end <= start:
                raise SystemExit(f"Padded time range is empty for clip {idx}: {item}")

            title = clean_name(item.get("title", ""), f"片段{idx:02d}")
            name = f"{idx:02d}_{title}_{customer}_{project}_{shoot_date}.mp4"
            output_path = output_dir / name
            rendered.append(render_clip(source, start, end, output_path))
            manifest.append(
                {
                    "index": idx,
                    "title": title,
                    "raw_start": raw_start,
                    "raw_end": raw_end,
                    "padded_start": start,
                    "padded_end": end,
                    "file": str(output_path),
                }
            )

        final_name = f"00_粗剪合集_{customer}_{project}_{shoot_date}.mp4"
        final_path = output_dir / final_name
        final = concatenate_videoclips(rendered, method="compose")
        final.write_videofile(
            str(final_path),
            fps=source.fps,
            codec="libx264",
            audio_codec="aac",
            preset="fast",
            threads=4,
            logger=None,
        )
        final.close()

        manifest_path = output_dir / "rough_cut_manifest.json"
        manifest_path.write_text(
            json.dumps({"final": str(final_path), "clips": manifest}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(final_path)
        print(manifest_path)
    finally:
        for clip in rendered:
            clip.close()
        source.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

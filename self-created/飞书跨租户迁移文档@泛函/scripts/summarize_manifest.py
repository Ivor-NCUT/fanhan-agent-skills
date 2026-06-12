#!/usr/bin/env python3
"""Build latest manifest, failure list, and summary from migration JSONL events."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


FIELDNAMES = [
    "source_name",
    "source_profile",
    "source_type",
    "source_title",
    "source_token",
    "source_url",
    "target_profile",
    "target_folder_token",
    "target_token",
    "target_url",
    "status",
    "method",
    "notes",
    "updated_at",
]


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"Line {line_number} is not a JSON object")
            events.append(value)
    return events


def event_key(event: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(event.get("source_profile") or ""),
        str(event.get("source_token") or ""),
        str(event.get("source_url") or ""),
        str(event.get("source_title") or event.get("title") or ""),
    )


def normalize_event(event: dict[str, Any]) -> dict[str, str]:
    normalized = {field: str(event.get(field, "") or "") for field in FIELDNAMES}
    if not normalized["source_name"] and event.get("source_label"):
        normalized["source_name"] = str(event["source_label"])
    if not normalized["source_title"] and event.get("title"):
        normalized["source_title"] = str(event["title"])
    if not normalized["source_type"]:
        for field in ("resolved_type", "source_doc_type", "doc_type", "entity_type", "type"):
            if event.get(field):
                normalized["source_type"] = str(event[field]).lower()
                break
    if not normalized["target_folder_token"] and event.get("target_parent_folder"):
        normalized["target_folder_token"] = str(event["target_parent_folder"])
    if not normalized["notes"] and event.get("error"):
        normalized["notes"] = str(event["error"])
    return normalized


def latest_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for event in events:
        latest[event_key(event)] = event
    return list(latest.values())


def build_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "total_unique_sources": len(rows),
        "status": dict(Counter(row["status"] or "unknown" for row in rows)),
        "by_source": dict(Counter(row["source_name"] or row["source_profile"] or "unknown" for row in rows)),
        "by_type": dict(Counter(row["source_type"] or "unknown" for row in rows)),
        "methods": dict(Counter(row["method"] or "unknown" for row in rows)),
    }


def write_outputs(rows: list[dict[str, str]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "migration_manifest_latest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] not in {"ok", "success"}]
    (out_dir / "failed_latest.json").write_text(
        json.dumps(failures, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = build_summary(rows)
    (out_dir / "final_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Path to migration-events.jsonl")
    parser.add_argument("--out-dir", type=Path, default=Path("."), help="Directory for summary outputs")
    args = parser.parse_args()

    events = load_events(args.jsonl)
    rows = [normalize_event(event) for event in latest_events(events)]
    rows.sort(key=lambda row: (row["source_name"], row["source_type"], row["source_title"]))
    write_outputs(rows, args.out_dir)

    print(json.dumps(build_summary(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download accessible images from an Alltuu album page.

This script intentionally works like a normal browser session: it opens the
album, scrolls, records visible/network image URLs, and downloads only URLs
that are accessible in that session.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import mimetypes
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:  # pragma: no cover - user-facing dependency check
    print(
        "Missing dependency: playwright. Install with `python -m pip install playwright` "
        "and then `python -m playwright install chromium`.",
        file=sys.stderr,
    )
    raise


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}
PHOTO_HOST_HINTS = (
    "alltuu.com",
    "alltuu.cn",
    "alltuu.cc",
    "alltuu.live",
    "alltuu.ren",
    "aliyuncs.com",
)
DROP_HINTS = (
    "favicon",
    "placeholder",
    "loading",
    "icon",
    "logo",
    "avatar",
    "sprite",
    "qr",
    "qrcode",
    "/js/",
    "/css/",
)


@dataclass
class DownloadRecord:
    index: int
    url: str
    file: str | None
    status: str
    bytes: int = 0
    error: str | None = None


def is_alltuu_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(h in host for h in ("alltuu.com", "alltuu.cc", "alltuu.cn", "alltuu.live", "alltuu.ren"))


def normalize_url(raw: str, base_url: str) -> str | None:
    if not raw:
        return None
    raw = raw.strip().strip("\"'")
    if raw.startswith("data:") or raw.startswith("blob:"):
        return None
    match = re.search(r"url\((.*?)\)", raw)
    if match:
        raw = match.group(1).strip().strip("\"'")
    if raw.startswith("//"):
        raw = "https:" + raw
    elif raw.startswith("/"):
        parsed = urlparse(base_url)
        raw = f"{parsed.scheme}://{parsed.netloc}{raw}"
    if not raw.startswith(("http://", "https://")):
        return None
    return unquote(raw)


def looks_like_image_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parse_qs(parsed.query)
    if not any(h in host for h in PHOTO_HOST_HINTS):
        return False
    if any(hint in path for hint in DROP_HINTS):
        return False
    suffix = Path(path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return True
    if path.endswith(("/sp", "/lp", "/mp", "/wp", "/op")):
        return True
    if any(k.lower() in {"x-oss-process", "image_process", "process"} for k in query):
        return True
    if any(token in path for token in ("/photo/", "/cover/", "/album", "/share/")):
        return True
    return False


def guess_extension(url: str, content_type: str | None) -> str:
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if ext:
            return ".jpg" if ext == ".jpe" else ext
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return suffix
    return ".jpg"


def safe_name(index: int, url: str, ext: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"{index:05d}_{digest}{ext}"


async def collect_dom_urls(page, base_url: str) -> set[str]:
    values: list[str] = await page.evaluate(
        """() => {
            const urls = new Set();
            document.querySelectorAll('img, source').forEach((el) => {
              ['src', 'data-src', 'data-original', 'srcset'].forEach((attr) => {
                const value = el.getAttribute(attr);
                if (!value) return;
                if (attr === 'srcset') {
                  value.split(',').forEach((part) => urls.add(part.trim().split(/\\s+/)[0]));
                } else {
                  urls.add(value);
                }
              });
            });
            document.querySelectorAll('*').forEach((el) => {
              const bg = getComputedStyle(el).backgroundImage;
              if (bg && bg !== 'none') urls.add(bg);
            });
            return Array.from(urls);
        }"""
    )
    normalized = {u for item in values if (u := normalize_url(item, base_url))}
    return {u for u in normalized if looks_like_image_url(u)}


async def auto_scroll(page, max_scrolls: int, idle_rounds: int, delay_ms: int) -> None:
    last_height = 0
    stable_rounds = 0
    for _ in range(max_scrolls):
        height = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        if height <= last_height:
            stable_rounds += 1
        else:
            stable_rounds = 0
            last_height = height
        await page.evaluate("window.scrollTo(0, Math.max(document.body.scrollHeight, document.documentElement.scrollHeight))")
        await page.wait_for_timeout(delay_ms)
        if stable_rounds >= idle_rounds:
            break


async def download_one(
    context,
    url: str,
    index: int,
    out_dir: Path,
    timeout: int,
    dry_run: bool,
    referer: str,
) -> DownloadRecord:
    headers = {"Referer": referer}
    try:
        if dry_run:
            return DownloadRecord(index=index, url=url, file=None, status="dry-run")
        response = await context.request.get(url, headers=headers, timeout=timeout * 1000)
        if not response.ok:
            return DownloadRecord(index=index, url=url, file=None, status="failed", error=f"HTTP {response.status}")
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return DownloadRecord(
                index=index,
                url=url,
                file=None,
                status="failed",
                error=f"not an image: {content_type or 'unknown content-type'}",
            )
        body = await response.body()
        ext = guess_extension(url, content_type)
        path = out_dir / safe_name(index, url, ext)
        if path.exists() and path.stat().st_size > 0:
            return DownloadRecord(index=index, url=url, file=str(path), status="skipped", bytes=path.stat().st_size)
        path.write_bytes(body)
        return DownloadRecord(index=index, url=url, file=str(path), status="downloaded", bytes=len(body))
    except Exception as exc:  # noqa: BLE001 - record and continue
        return DownloadRecord(index=index, url=url, file=None, status="failed", error=str(exc))


async def run(args: argparse.Namespace) -> dict[str, Any]:
    if not is_alltuu_url(args.url):
        raise SystemExit("This does not look like an Alltuu album URL.")

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    network_urls: set[str] = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not args.headed)
        context_kwargs: dict[str, Any] = {
            "viewport": {"width": 390, "height": 844},
            "is_mobile": True,
            "has_touch": True,
            "user_agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            "locale": "zh-CN",
        }
        if args.browser_state:
            context_kwargs["storage_state"] = str(Path(args.browser_state).expanduser())
        context = await browser.new_context(**context_kwargs)
        page = await context.new_page()

        def capture_response(response) -> None:
            try:
                content_type = response.headers.get("content-type", "")
                url = response.url
                if content_type.startswith("image/") and looks_like_image_url(url):
                    network_urls.add(url)
            except Exception:
                return

        page.on("response", capture_response)

        try:
            await page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout * 1000)
            try:
                await page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                pass
            await auto_scroll(page, args.max_scrolls, args.idle_rounds, args.scroll_delay)
            dom_urls = await collect_dom_urls(page, args.url)
            all_urls = sorted(dom_urls | network_urls)
        finally:
            await page.close()

        filtered_urls = [url for url in all_urls if looks_like_image_url(url)]
        (out_dir / "urls.txt").write_text("\n".join(filtered_urls) + ("\n" if filtered_urls else ""), encoding="utf-8")

        semaphore = asyncio.Semaphore(args.concurrency)

        async def guarded(url: str, index: int) -> DownloadRecord:
            async with semaphore:
                return await download_one(context, url, index, out_dir, args.timeout, args.dry_run, args.url)

        records = await asyncio.gather(*(guarded(url, i + 1) for i, url in enumerate(filtered_urls)))
        await context.close()
        await browser.close()

    manifest = {
        "source_url": args.url,
        "output_dir": str(out_dir),
        "total_urls": len(filtered_urls),
        "downloaded": sum(1 for r in records if r.status == "downloaded"),
        "skipped": sum(1 for r in records if r.status == "skipped"),
        "failed": sum(1 for r in records if r.status == "failed"),
        "dry_run": args.dry_run,
        "records": [asdict(r) for r in records],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    failed = [asdict(r) for r in records if r.status == "failed"]
    if failed:
        (out_dir / "failed.json").write_text(json.dumps(failed, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download accessible images from an Alltuu album page.")
    parser.add_argument("url", help="Alltuu album URL")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--max-scrolls", type=int, default=120, help="Maximum scroll attempts")
    parser.add_argument("--idle-rounds", type=int, default=8, help="Stop after this many stable scroll-height rounds")
    parser.add_argument("--scroll-delay", type=int, default=800, help="Delay between scrolls in milliseconds")
    parser.add_argument("--concurrency", type=int, default=4, help="Concurrent image downloads")
    parser.add_argument("--timeout", type=int, default=45, help="Navigation/download timeout in seconds")
    parser.add_argument("--browser-state", help="Optional Playwright storage_state JSON for logged-in access")
    parser.add_argument("--headed", action="store_true", help="Show the browser window")
    parser.add_argument("--dry-run", action="store_true", help="Collect URLs but do not download images")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = asyncio.run(run(args))
    print(json.dumps({k: manifest[k] for k in ("output_dir", "total_urls", "downloaded", "skipped", "failed", "dry_run")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

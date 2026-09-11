#!/usr/bin/env python3
"""Extract normalized public social content through AI Conductor."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

API_BASE = "https://plugin.aiconductor.fun/api"
ONBOARDING_URL = "https://dev.aiconductor.fun/"
CONFIG_PATH = Path(os.environ.get("AICONDUCTOR_CONFIG_PATH", Path.home() / ".config/aiconductor/api_key"))
URL_RE = re.compile(r"https?://[^\s<>\"']+")


class ExtractionError(RuntimeError):
    pass


def load_api_key() -> str:
    value = os.environ.get("AICONDUCTOR_API_KEY", "").strip()
    if value:
        return value
    descriptor = None
    try:
        flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(CONFIG_PATH, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ExtractionError("API key 配置必须是普通文件")
        if metadata.st_mode & 0o077:
            raise ExtractionError("API key 配置权限过宽，请执行 chmod 600 后重试")
        with os.fdopen(descriptor, encoding="utf-8") as stream:
            descriptor = None
            return stream.read().strip()
    except FileNotFoundError:
        return ""
    except OSError as exc:
        raise ExtractionError(f"无法读取 API key 配置：{exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)


API_KEY = ""


def onboarding_message() -> str:
    return (
        "尚未配置 AI Conductor API key。请先打开 " + ONBOARDING_URL +
        " 注册账号并创建 API key，然后把 key 发给 Agent；Agent 将通过 "
        "extract_social_content.py --configure 以不回显方式完成本机配置。"
    )


def require_api_key() -> None:
    if not API_KEY:
        raise ExtractionError(onboarding_message())


def configure_api_key() -> None:
    secret = getpass.getpass("请输入 AI Conductor API key：").strip()
    if len(secret) < 16:
        raise ExtractionError("API key 为空或格式过短，请重新复制完整 key")
    try:
        directory_created = not CONFIG_PATH.parent.exists()
        CONFIG_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if directory_created:
            CONFIG_PATH.parent.chmod(0o700)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(CONFIG_PATH, flags, 0o600)
        try:
            os.fchmod(descriptor, 0o600)
            os.write(descriptor, (secret + "\n").encode())
        finally:
            os.close(descriptor)
        CONFIG_PATH.chmod(0o600)
    except OSError as exc:
        raise ExtractionError(f"无法保存 API key 配置：{exc}") from exc
    print(f"API key 已保存到 {CONFIG_PATH}（权限 600）")


def redact(value: str) -> str:
    return value.replace(API_KEY, "<REDACTED>") if API_KEY else value


def post(endpoint: str, payload: dict, *, body_key: bool = False, timeout: int = 90) -> dict:
    require_api_key()
    data = dict(payload)
    if body_key:
        data["api_key"] = API_KEY
    request = Request(
        f"{API_BASE}/{endpoint}",
        data=json.dumps(data, ensure_ascii=False).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "social-content-extractor-public/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as exc:
        detail = redact(exc.read().decode("utf-8", "replace")[:1000])
        raise ExtractionError(f"API HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ExtractionError(redact(f"API request failed: {exc}")) from exc
    if not result.get("success", False):
        raise ExtractionError(redact(str(result.get("message") or result)))
    return result


def first_url(text: str) -> str:
    match = URL_RE.search(text)
    if not match:
        raise ExtractionError("输入中没有 http/https 链接")
    return match.group(0).rstrip(".,，。!！)）]")


def platform_host(host: str, platform: str) -> bool:
    families = {
        "douyin": ("douyin.com", "iesdouyin.com"),
        "xiaohongshu": ("xiaohongshu.com", "xhslink.com"),
    }
    return any(host == domain or host.endswith("." + domain) for domain in families[platform])


class PlatformRedirectHandler(HTTPRedirectHandler):
    def __init__(self, platform: str):
        self.platform = platform

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlparse(newurl)
        if target.scheme != "https" or not platform_host((target.hostname or "").lower(), self.platform):
            raise ExtractionError("短链跳转到了不受支持的目标，已停止访问")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def resolve_short_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in {"v.douyin.com", "xhslink.com", "www.xhslink.com"}:
        return url
    if parsed.scheme != "https":
        raise ExtractionError("社媒短链必须使用 HTTPS")
    platform = "douyin" if host == "v.douyin.com" else "xiaohongshu"
    opener = build_opener(PlatformRedirectHandler(platform))
    for method in ("HEAD", "GET"):
        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"}, method=method)
            with opener.open(request, timeout=15) as response:
                return response.geturl()
        except (HTTPError, URLError, TimeoutError):
            pass
    return url


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "xiaohongshu.com" in host or "xhslink.com" in host:
        return "xiaohongshu"
    if "douyin.com" in host or "iesdouyin.com" in host:
        return "douyin"
    if host == "mp.weixin.qq.com":
        return "wechat"
    return "web"


def detect_kind(platform: str, url: str) -> str:
    path = urlparse(url).path
    if platform == "xiaohongshu":
        if re.search(r"/(?:explore|discovery/item)/", path):
            return "item"
        if "/user/profile/" in path:
            return "profile"
    elif platform == "douyin":
        if "/video/" in path or "/share/video/" in path:
            return "item"
        if "/user/" in path:
            return "profile"
    elif platform == "wechat":
        return "item" if path.startswith("/s") else "profile"
    elif platform == "web":
        return "item"
    raise ExtractionError("短链无法判断是作品还是主页，请加 --kind item 或 --kind profile")


def iso_time(value, *, milliseconds: bool = False) -> str | None:
    if not value:
        return None
    seconds = float(value) / (1000 if milliseconds else 1)
    return datetime.fromtimestamp(seconds, timezone.utc).astimezone().isoformat(timespec="seconds")


def billing_cost(*responses: dict) -> dict:
    total = 0.0
    currency = "CNY"
    for response in responses:
        billing = response.get("billing") or {}
        for key in ("total_fee", "total_service_fee", "service_fee"):
            if billing.get(key) is not None:
                total += float(billing[key])
                break
        currency = billing.get("currency") or currency
    return {"total_fee": round(total, 4), "currency": currency}


def parse_markdown(markdown: str) -> tuple[str, str]:
    title = ""
    body = markdown
    if markdown.startswith("---\n") and "\n---\n" in markdown[4:]:
        frontmatter, body = markdown[4:].split("\n---\n", 1)
        match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
        if match:
            raw = match.group(1).strip()
            try:
                title = json.loads(raw) if raw.startswith('"') else raw
            except json.JSONDecodeError:
                title = raw.strip('"')
    return title, body.strip()


def xhs_id(url: str, kind: str) -> str:
    pattern = r"/(?:explore|discovery/item)/([0-9a-fA-F]+)" if kind == "item" else r"/user/profile/([0-9A-Za-z]+)"
    match = re.search(pattern, urlparse(url).path)
    if not match:
        raise ExtractionError(f"无法从小红书链接提取{'笔记' if kind == 'item' else '用户'} ID")
    return match.group(1)


def extract_douyin(source: str, url: str, kind: str, args) -> dict:
    if kind == "item":
        response = post("douyin_video_info", {"share_url": source}, body_key=True)
        data = response.get("data") or {}
        author = data.get("author") or {}
        interaction = data.get("interaction") or {}
        item = {
            "title": data.get("title") or "",
            "url": url,
            "copy": data.get("title") or "",
            "author": author.get("nickname"),
            "published_at": data.get("create_time_formatted") or iso_time(data.get("create_time")),
            "metrics": {
                "likes": interaction.get("like"), "collects": interaction.get("collect"),
                "comments": interaction.get("comment"), "shares": interaction.get("share"),
            },
        }
        return result("douyin", kind, [item], True, "单条作品已成功返回", billing_cost(response))

    require_pages(args)
    response = post("douyin_user_videos", {
        "home_page": source, "max_pages": args.max_pages, "max_seconds": args.max_seconds,
    }, body_key=True, timeout=args.max_seconds + 30)
    items = []
    for video in (response.get("data") or {}).get("aweme_list", []):
        stats = video.get("statistics") or {}
        copy = video.get("desc") or ""
        items.append({
            "title": copy, "url": video.get("share_url"), "copy": copy,
            "author": (video.get("author") or {}).get("nickname"),
            "published_at": video.get("create_time_formatted") or iso_time(video.get("create_time")),
            "metrics": {"likes": stats.get("digg_count"), "collects": stats.get("collect_count"),
                        "comments": stats.get("comment_count"), "shares": stats.get("share_count")},
        })
    pages = (response.get("billing") or {}).get("pages_charged")
    page_text = pages if pages is not None else "未知"
    note = f"已取 {page_text} 页；接口不返回账号总作品数，无法证明全量"
    return result("douyin", kind, items, None, note, billing_cost(response), pages)


def extract_xhs(url: str, kind: str, args) -> dict:
    identifier = xhs_id(url, kind)
    if kind == "item":
        response = post("xhs_note_info_v3", {"note_id": identifier})
        note = response.get("note_data") or {}
        stats = note.get("interact_info") or {}
        item = {
            "title": note.get("title") or "", "url": url, "copy": note.get("desc") or "",
            "author": (note.get("user") or {}).get("nickname"),
            "published_at": iso_time(note.get("time"), milliseconds=True),
            "metrics": {"likes": stats.get("liked_count"), "collects": stats.get("collected_count"),
                        "comments": stats.get("comment_count"), "shares": stats.get("share_count")},
        }
        return result("xiaohongshu", kind, [item], True, "单条作品已成功返回", billing_cost(response))

    require_pages(args)
    response = post("xhs_user_notes_v2", {
        "user_id": identifier, "max_pages": args.max_pages, "max_seconds": args.max_seconds,
    }, timeout=args.max_seconds + 30)
    items = []
    for note in (response.get("data") or {}).get("notes", []):
        note_id = note.get("noteId")
        items.append({
            "title": note.get("title") or "",
            "url": f"https://www.xiaohongshu.com/explore/{note_id}" if note_id else None,
            "copy": note.get("desc") or "", "author": (note.get("user") or {}).get("nickname"),
            "published_at": iso_time(note.get("time"), milliseconds=True),
            "metrics": {"likes": note.get("likes"), "collects": note.get("collected_count"),
                        "comments": note.get("comments_count"), "shares": note.get("shared_count")},
        })
    pages = (response.get("billing") or {}).get("pages_billed")
    page_text = pages if pages is not None else "未知"
    note = f"已取 {page_text} 页；接口不返回账号总作品数，无法证明全量"
    return result("xiaohongshu", kind, items, None, note, billing_cost(response), pages)


def extract_wechat(url: str, kind: str, args) -> dict:
    if kind == "item":
        content_response = post("url_to_markdown", {"url": url, "timeout": args.max_seconds})
        data_response = post("wx_article_data", {"url": url}, body_key=True)
        title, copy = parse_markdown(content_response.get("markdown") or "")
        item = {"title": title, "url": url, "copy": copy, "author": None,
                "published_at": None, "metrics": data_response.get("data") or {}}
        return result("wechat", kind, [item], True, "单篇文章正文与作品数据已成功返回",
                      billing_cost(content_response, data_response))

    require_pages(args)
    response = post("wx_history_articles", {
        "url": url, "max_pages": args.max_pages, "max_seconds": args.max_seconds,
    }, body_key=True, timeout=args.max_seconds + 30)
    payload = response.get("data") or {}
    articles = payload.get("data") or []
    items = []
    copy_responses = []
    for article in articles:
        item = {
            "title": article.get("title") or "", "url": article.get("url"),
            "copy": "", "author": payload.get("mp_nickname"),
            "published_at": article.get("post_time_str") or iso_time(article.get("post_time")),
            "metrics": {"reads": article.get("read"), "likes": article.get("zan")},
        }
        if args.copy and item["url"]:
            try:
                copy_response = post("url_to_markdown", {"url": item["url"], "timeout": args.max_seconds})
                copy_responses.append(copy_response)
                _, item["copy"] = parse_markdown(copy_response.get("markdown") or "")
            except ExtractionError as exc:
                item["copy_error"] = str(exc)
        items.append(item)
    pages = (response.get("billing") or {}).get("pages_billed") or payload.get("now_page")
    total_pages = payload.get("total_page") or 0
    complete = pages >= total_pages if pages and total_pages else None
    note = (f"已取 {pages} / {total_pages} 页" if total_pages else
            f"已取 {pages or '未知'} 页；接口未返回有效总页数，无法证明全量")
    return result("wechat", kind, items, complete, note,
                  billing_cost(response, *copy_responses), pages)


def extract_web(url: str) -> dict:
    response = post("url_to_markdown", {"url": url})
    title, copy = parse_markdown(response.get("markdown") or "")
    item = {"title": title or url, "url": url, "copy": copy, "author": None,
            "published_at": None, "metrics": {}}
    return result("web", "item", [item], True, "网页正文已返回；该接口不提供作品数据", billing_cost(response))


def require_pages(args) -> None:
    if args.max_pages is None:
        raise ExtractionError("主页提取必须指定 --max-pages；先用 1 页预览可避免未知费用")


def result(platform, kind, items, complete, note, billing, pages=None) -> dict:
    return {"platform": platform, "kind": kind, "count": len(items), "complete": complete,
            "complete_note": note, "pages_fetched": pages, "billing": billing, "items": items}


def render_markdown(data: dict) -> str:
    lines = ["# 社媒内容提取", "", f"- 平台：{data['platform']}", f"- 类型：{data['kind']}",
             f"- 作品数：{data['count']}", f"- 完整性：{data['complete']}",
             f"- 说明：{data['complete_note']}",
             f"- 本次接口费用：{data['billing']['total_fee']} {data['billing']['currency']}"]
    for index, item in enumerate(data["items"], 1):
        title = item.get("title") or "（无标题）"
        metrics = ", ".join(f"{key}={value}" for key, value in item.get("metrics", {}).items() if value is not None)
        lines += ["", f"## {index}. {title}", "", f"- 链接：{item.get('url') or ''}",
                  f"- 作者：{item.get('author') or ''}", f"- 发布时间：{item.get('published_at') or ''}",
                  f"- 作品数据：{metrics or '无'}", "", "### 文案", "", item.get("copy") or ""]
        if item.get("copy_error"):
            lines += ["", f"> 正文提取失败：{item['copy_error']}"]
    return "\n".join(lines).rstrip() + "\n"


def self_test() -> None:
    assert detect_platform("https://www.xiaohongshu.com/explore/abc123") == "xiaohongshu"
    assert detect_kind("douyin", "https://www.douyin.com/video/123") == "item"
    assert xhs_id("https://www.xiaohongshu.com/user/profile/5e7e31a20000000001004b48", "profile") == "5e7e31a20000000001004b48"
    assert parse_markdown('---\ntitle: "测试"\n---\n\n正文') == ("测试", "正文")
    assert billing_cost({"billing": {"service_fee": 0.15, "total_service_fee": 0}})["total_fee"] == 0
    assert ONBOARDING_URL in onboarding_message()
    assert platform_host("www.douyin.com", "douyin")
    assert not platform_host("douyin.com.example.org", "douyin")
    try:
        PlatformRedirectHandler("douyin").redirect_request(None, None, 302, "", {}, "http://127.0.0.1/")
    except ExtractionError:
        pass
    else:
        raise AssertionError("unsafe redirect was not blocked")
    print("self-test passed")


def main() -> int:
    global API_KEY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="公开作品/主页链接或含链接的分享文本")
    parser.add_argument("--kind", choices=("auto", "item", "profile"), default="auto")
    parser.add_argument("--platform", choices=("auto", "xiaohongshu", "douyin", "wechat", "web"), default="auto")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--max-seconds", type=int, default=50)
    parser.add_argument("--copy", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--configure", action="store_true", help="交互式保存 API key 到本机私有配置")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.configure:
        configure_api_key()
        return 0
    if not args.source:
        parser.error("source is required unless --self-test is used")
    API_KEY = load_api_key()
    if args.max_pages is not None and args.max_pages < 1:
        parser.error("--max-pages must be >= 1")
    if not 1 <= args.max_seconds <= 50:
        parser.error("--max-seconds must be between 1 and 50")

    input_url = first_url(args.source)
    resolved_url = resolve_short_url(input_url)
    platform = detect_platform(resolved_url) if args.platform == "auto" else args.platform
    kind = detect_kind(platform, resolved_url) if args.kind == "auto" else args.kind
    if platform == "douyin":
        data = extract_douyin(args.source, resolved_url, kind, args)
    elif platform == "xiaohongshu":
        data = extract_xhs(resolved_url, kind, args)
    elif platform == "wechat":
        data = extract_wechat(resolved_url, kind, args)
    elif kind == "profile":
        raise ExtractionError("普通网页不支持主页作品列表")
    else:
        data = extract_web(resolved_url)
    output = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else render_markdown(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExtractionError as exc:
        print(f"error: {redact(str(exc))}", file=sys.stderr)
        raise SystemExit(1)

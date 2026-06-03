---
name: alltuu-album-downloader
description: Download all accessible images from Alltuu / 图宇 / 图片直播相册 links to the user's local machine. Use this skill whenever the user gives an alltuu.com, m.alltuu.com, alltuu.cc, or similar Alltuu album/photo-live link and asks to 批量下载图片, 下载相册, 保存图片直播, 抓取活动照片, 导出相册图片, or collect all photos from a shared event album. This skill should trigger even if the user does not explicitly say "Alltuu" but the URL is an Alltuu album page.
---

# Alltuu Album Downloader

Use this skill to help the user batch-download images from an Alltuu mobile album or photo-live album link.

The goal is not to bypass access controls. Download only images that the user's normal browser session can access. If the page requires login, invite code, payment, or other permission, ask the user to confirm they have access and use a browser session/cookie path that represents that access.

## What This Skill Does

Given an Alltuu album URL, produce a local folder containing:

- downloaded image files
- `manifest.json` with source URLs, file paths, and status
- `urls.txt` with the final image URL list
- `failed.json` if some files could not be downloaded

Prefer the bundled script in `scripts/download_alltuu_album.py` instead of hand-rolling scraping logic.

## Safety And Permission Boundary

Before running a download, check:

1. The URL is an Alltuu album/photo-live/share page.
2. The user is asking to download images they can normally view.
3. The workflow does not attempt to remove watermarks, bypass paywalls, guess private original URLs, brute-force IDs, or evade rate limits.

If the user asks for watermark removal, paid-original bypass, password cracking, invite-code bypass, or hidden/private resource enumeration, refuse that part and offer to download only normally accessible images.

## Default Workflow

1. Confirm the target album URL and destination folder.
   - If the user did not specify a destination, create a descriptive folder under the current working directory or `~/Downloads`.
   - Use a timestamp or album title in the folder name when possible.
2. Decide whether a logged-in browser state is needed.
   - Public links usually work with the script directly.
   - If the page displays login, permission, invite, purchase, or blank content, ask the user to open/login in the browser and then retry with a saved browser state if available.
3. Run the bundled script:

```bash
python scripts/download_alltuu_album.py "<album_url>" --out "<destination_folder>"
```

4. Review the script summary:
   - total image URLs discovered
   - downloaded count
   - skipped existing count
   - failed count
   - output folder path
5. Report the result to the user in plain language.
6. If the task is part of a project workflow, note whether the output folder should be registered in the user's project/asset system.

## Script Options

The downloader supports these common options:

```bash
python scripts/download_alltuu_album.py "<album_url>" \
  --out "<destination_folder>" \
  --max-scrolls 120 \
  --idle-rounds 8 \
  --concurrency 4 \
  --timeout 45
```

Use `--dry-run` when the user asks only to inspect feasibility or count images without downloading.

Use `--browser-state <path>` if a logged-in browser storage state has already been exported.

## How The Script Works

The script uses Playwright because Alltuu albums are Vue single-page apps and most image URLs are loaded after scrolling.

It collects images from three sources:

- DOM image tags and CSS background images
- browser network responses with image content types
- Alltuu CDN/OSS-looking URLs observed during page activity

Then it filters obvious non-photo assets such as favicons, placeholders, icons, loading images, script files, and tiny UI resources. It keeps accessible CDN images and downloads them with the same browser context so Referer/Cookie behavior matches normal viewing.

## Handling Common Outcomes

### Public album works

Download normally. Tell the user the folder path and image count.

### Page loads but very few images are found

Try increasing scrolls:

```bash
python scripts/download_alltuu_album.py "<album_url>" --out "<destination_folder>" --max-scrolls 240 --idle-rounds 12
```

If still low, explain that the album may require interaction, a category tab, search/filter state, or login.

### Login or permission wall

Do not attempt to bypass it. Ask the user for the authorized access route. Acceptable options:

- user provides a browser storage state file
- user opens the album in a browser session the agent can use
- user confirms an official bulk-download entry exists and wants help using it

### Watermarked versus original images

Download what the normal page exposes. Do not infer or construct unwatermarked originals unless the page or official API returns those URLs under the user's authorized session.

### Official batch-download endpoint appears

Some Alltuu builds include batch-download endpoints. Prefer the page-visible download UX or accessible API only when it is clearly available to the user's session. Do not call endpoints that produce paid/private originals unless the user's permissions clearly include them.

## Output Message Template

Use this concise structure:

```markdown
已完成 Alltuu 相册图片下载。

本地文件夹：[folder path]
发现图片：N 张
成功下载：N 张
已存在跳过：N 张
失败：N 张

清单文件：manifest.json / urls.txt
```

If anything failed, add one short reason and next action.

## Test Prompts

Use these when sanity-checking the skill:

1. `帮我把这个图片直播相册里的照片全部下载到本地：https://m.alltuu.com/album/example/123?menu=live`
2. `这个 Alltuu 相册能不能批量保存？能的话放到 Downloads/活动照片，不要绕过权限。`
3. `我给你一个图宇相册链接，只下载我正常能看到的图片，输出 manifest。`


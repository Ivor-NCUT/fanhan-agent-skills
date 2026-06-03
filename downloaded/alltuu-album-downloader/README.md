# Alltuu Album Downloader Skill

Agent Skill for downloading all normally accessible images from Alltuu / 图宇 / 图片直播相册 links to a local folder.

## What It Does

Given an Alltuu album URL, the skill guides an agent to:

- open the album like a normal mobile browser
- scroll through the page to load images
- collect visible image URLs from the page and network responses
- download accessible images to a local folder
- write `manifest.json` and `urls.txt`

The bundled script is:

```bash
scripts/download_alltuu_album.py
```

## Usage

From inside the skill directory:

```bash
python scripts/download_alltuu_album.py "https://m.alltuu.com/album/..." --out "./album-images"
```

Dry run:

```bash
python scripts/download_alltuu_album.py "https://m.alltuu.com/album/..." --out "./album-images" --dry-run
```

## Requirements

```bash
python -m pip install playwright
python -m playwright install chromium
```

## Boundary

This skill is designed to download only images the user's normal browser session can access. It does not remove watermarks, bypass paywalls, guess private original URLs, crack invite codes, or evade access controls.

## Files

- `SKILL.md` - Agent instructions and trigger metadata
- `scripts/download_alltuu_album.py` - Playwright downloader
- `evals/evals.json` - basic skill test prompts


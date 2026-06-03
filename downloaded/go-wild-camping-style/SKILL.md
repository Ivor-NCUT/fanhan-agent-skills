---
name: go-wild-camping-style
description: Apply a bold white-green-black, street-outdoor visual system abstracted from the user's favorite camping PPT template. Use when designing or generating assets such as WeChat official account covers, Xiaohongshu note images, PPT slides, website sections, course visuals, posters, banners, thumbnails, social graphics, or GPT image-2 prompts that should feel young, energetic, high-contrast, editorial, sticker-like, and not necessarily camping-themed.
---

# Go Wild Camping Style

## Overview

Use this skill to translate any topic into the user's preferred visual language: bold green-white-black editorial layouts, oversized typography, torn-paper edges, sticker labels, hand-drawn arrows, and youthful outdoor/street energy. The subject can be AI, business, education, software, lifestyle, or anything else; keep the style, not the camping topic.

## Workflow

1. Clarify the deliverable only if size, platform, exact text, or required format is missing and cannot be inferred.
2. Load `references/style-system.md` for the visual grammar before writing prompts or creating designs.
3. For GPT image generation, use the built-in image generation path by default; if the user explicitly asks for API/CLI or `gpt-image-2`, use the local `imagegen` skill's CLI/API guidance.
4. Preserve user-provided text exactly. If text rendering matters, keep the copy short, spell tricky words, and specify “verbatim typography text”.
5. Use reference images in `assets/reference-images/` only as private style anchors; do not recreate the camping content unless the user asks.
6. For deck, website, or layout code tasks, implement the style natively with CSS/HTML/PPT elements rather than generating a flat bitmap unless the user asks for images.
7. After generating any asset with text, run the text-layout QA in `references/style-system.md`. If any check fails, regenerate or revise the specific asset before showing it to the user.

## Core Style Rules

- **Palette:** off-white paper base, deep forest green, black, white, neon lime, and warm yellow as accent strokes or stickers.
- **Typography:** use extremely heavy condensed Chinese display type for Chinese headlines; use huge black geometric sans-serif capitals for English; use small repeated navigation labels as decorative metadata.
- **Composition:** combine large negative space with aggressive cropped type, oversized ghost outline words, off-grid text blocks, and one dominant visual or typographic mass.
- **Texture:** add torn-paper vertical edges, rough paper fibers, photo cutouts, sticker outlines, hand-drawn arrows, scribbles, underlines, and tag/label shapes.
- **Energy:** make it look young, loud, playful, outdoor/editorial, slightly rebellious, and polished rather than cute, corporate, luxury, or minimal.

## Prompt Pattern

When generating an image, structure the prompt like this:

```text
Use case: <asset type and platform>
Primary request: <topic/content goal>
Exact text: "<short verbatim copy>"
Style: bold white-green-black street-outdoor editorial design, youthful high-energy zine poster, oversized heavy typography, torn-paper edges, sticker labels, hand-drawn arrows and scribbles, deep forest green + black + off-white + neon lime/yellow accents
Composition: <aspect ratio, focal hierarchy, photo vs type balance>
Typography: extra-heavy Chinese display headline, giant black uppercase English sans-serif, small repeated metadata labels
Constraints: keep text legible, no camping imagery unless requested, no logos, no watermark
```

## Asset Notes

- Use `assets/fonts/印品鸿蒙体.ttf` for heavy Chinese display text when creating native layouts.
- Use `assets/fonts/Cinzel-Black.otf` only as an optional decorative display face; for the main English look, prefer very heavy geometric sans-serif capitals if available.
- Use `assets/reference-images/` for checking the original rhythm: page borders, cropped words, torn paper, labels, arrows, photo overlays, and spacing.

## Avoid

- Do not overfit to tents, mountains, grass, or camping nouns when the user's topic is unrelated.
- Do not make the design clean corporate SaaS, beige lifestyle, luxury editorial, cyberpunk, cute cartoon, or generic Canva template.
- Do not use too many colors; the punch comes from restraint plus one loud accent.
- Do not fill every corner; keep deliberate white space and a few loud collisions.

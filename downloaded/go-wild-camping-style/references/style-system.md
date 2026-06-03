# Go Wild Camping Style System

## Visual Essence

This style is a transferable youth-energy design system, not a camping-only theme. It mixes Swiss/editorial scale, Chinese street-poster loudness, outdoor zine texture, and sticker-board playfulness.

Core feeling: “fresh air, rebellious notes in the margin, oversized type, handmade stickers, confident white space.”

## Palette

- Paper white: `#F7F7F2` or clean white backgrounds.
- Deep forest green: `#3F7F2E`, `#2B541F`, `#23491B`.
- Black: `#050505` for main type and strokes.
- White: text over images and sticker interiors.
- Neon lime: `#A8E000` for small highlights or activity tags.
- Warm yellow: `#FFC414` or `#FFD400` for outlines, arrows, stickers, underline strokes.
- Muted gray-green: `#7F9075` for thin outline typography and schematic shapes.

Use 70–85% white/black/green and only 5–10% yellow/lime.

## Typography

- Chinese headline: ultra-heavy block display, compressed, chunky, poster-like. Use `印品鸿蒙体.ttf` when rendering locally.
- English headline: very large uppercase black geometric sans-serif, extra-bold or black weight; cropped by canvas edges when useful.
- Ghost type: giant outline words in pale green/white, 1–2 px stroke, no fill, partially hidden behind foreground objects.
- Metadata labels: small uppercase phrases repeated at top-left, top-center, sidebars, or near labels.
- Text rhythm: combine 1 huge headline, 1 medium slogan, 2–5 micro-labels, and optional vertical sidebar text.

## Text Layout QA

Run this check after every generated image, deck slide, or native layout that contains text. If any item fails, revise that specific asset and check again before delivery.

### Mechanical Checks
- Confirm every text box stays inside its intended safe area, except intentional giant ghost/cropped background words.
- Confirm no foreground headline, label, body paragraph, QR code, portrait, sticker, or photo-critical subject overlaps in a way that hurts readability.
- Confirm body text has enough line height: Chinese paragraphs need at least 1.25× font size; dense explanatory text should use 1.35–1.5×.
- Confirm each card has clear hierarchy: one dominant headline, one secondary statement, then supporting details.
- Confirm long Chinese paragraphs are not set in ultra-heavy display type; use display type for titles and short pull quotes, and a cleaner readable font for paragraphs.
- Confirm all final exports keep the requested dimensions and no important text is clipped by the canvas edge or torn-paper strips.

### Visual Checks
- Create a contact sheet or quick preview for multi-image sets.
- Inspect at thumbnail size first: the main message should still be readable.
- Inspect at full size for line breaks, cramped labels, awkward single-character lines, and accidental collisions.
- If text appears cramped, reduce copy per page, shrink the font, increase the text container, or split into another page.

### Regeneration Rules
- Regenerate the asset if any foreground text is clipped, unreadable, too close to edges, or colliding unintentionally.
- Regenerate or re-layout if the style decoration competes with the information.
- Prefer native rendered text over image-model-rendered text for Chinese-heavy cards, service menus, case-study pages, pricing cards, and QR/contact cards.

## Layout Patterns

### White Canvas Poster
- Mostly white background.
- Oversized Chinese title in green/black, often stacked or overlapping.
- Giant outlined English word behind it.
- Small top metadata labels.
- One black-yellow oval tag or hand-drawn arrow.

### Photo + Torn Paper
- Full-bleed or half-bleed photographic image.
- Vertical torn paper strips along one or both sides.
- White or green label blocks over the image.
- Large semi-transparent outline word across the image.
- Yellow hand-drawn strokes following image geometry.

### Split Editorial Page
- Left side: huge typographic composition on white.
- Right side: photo framed by torn paper or hard crop.
- Sidebar text stacked vertically, with selected syllables in neon lime.

### Sticker Activity Board
- Several rounded irregular tags with thick yellow/green borders.
- Simple black pictogram-like icons.
- Slight rotations, imperfect alignment, energetic but readable.

## Motifs

- Torn paper edges: rough white strips with subtle gray texture.
- Hand arrows: black or white marker arrows with a loop or squiggle tail.
- Sticker tags: black oval with yellow border, or green/yellow rounded label.
- Underlines: thick yellow strokes, sometimes crossing text.
- Outline shapes: thin green technical/schematic outlines behind type.
- Cropped giant letters: English or Chinese characters partially off-canvas.
- Sidebars: vertical stacked English words, broken awkwardly across lines on purpose.

## GPT Image Prompt Add-ons

Use these phrases to intensify the style:

- “bold Chinese street-poster typography”
- “white paper zine layout with torn paper edge texture”
- “forest green, black, off-white, neon lime and yellow accent palette”
- “oversized cropped typography, ghost outline letters in the background”
- “hand-drawn marker arrows, scribble underline, sticker labels”
- “youthful energetic editorial poster, polished but intentionally rough”

Use these negative constraints:

- “no camping objects unless requested”
- “no corporate blue SaaS look”
- “no pastel cute illustration”
- “no luxury magazine minimalism”
- “no generic template look”
- “no watermark, no fake logo”

## Example Prompt: AI Course Cover

Use case: WeChat official account cover, 2.35:1.
Primary request: design a cover for an AI course launch.
Exact text: “AI 实战课｜从提示词到工作流”
Style: bold white-green-black street-outdoor editorial design, youthful high-energy zine poster, oversized heavy Chinese typography, giant ghost outline word “AI” in the background, torn-paper edge texture, sticker label, hand-drawn arrow, forest green + black + off-white + neon lime/yellow accents.
Composition: mostly white background, dominant Chinese headline on left, abstract AI workflow photo/collage on right, small metadata labels at top and right sidebar.
Constraints: keep text legible and verbatim, no camping imagery, no logos, no watermark.

## Example Prompt: Xiaohongshu Note

Use case: Xiaohongshu vertical note cover, 3:4.
Primary request: make a punchy note image about building a personal AI assistant.
Exact text: “把 AI 变成你的第二大脑”
Style: bold green-black-white youth editorial poster, oversized cropped headline, torn paper sides, neon lime sticker tags, black hand-drawn arrows, giant pale outline word “ASSISTANT” behind the text.
Composition: central headline collision, small tag list on lower left, rough paper texture, high contrast.
Constraints: no camping imagery, no fake UI screenshots, no watermark.

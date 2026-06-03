# Fun-ASR-Nano model status

Last checked: 2026-05-19

## Official sources checked

- GitHub: `https://github.com/FunAudioLLM/Fun-ASR`
- Hugging Face: `FunAudioLLM/Fun-ASR-Nano-2512`
- Hugging Face: `FunAudioLLM/Fun-ASR-MLT-Nano-2512`
- ModelScope cache: `FunAudioLLM/Fun-ASR-Nano-2512`

## Current result

- Latest official Nano base model: `FunAudioLLM/Fun-ASR-Nano-2512`
- Hugging Face commit: `a7088d620f755dcdca575b63db184c3ad55b2865`
- Last modified upstream: `2025-12-23T08:57:06Z`
- Local ModelScope cache path on macOS/Linux is usually `~/.cache/modelscope/hub/models/FunAudioLLM/Fun-ASR-Nano-2512`
- Latest official multilingual Nano sibling: `FunAudioLLM/Fun-ASR-MLT-Nano-2512`
- MLT Hugging Face commit: `cf67a938bf2829959d08fdfb84e186eff02a67ff`

## Remote code

The bundled `.fun-asr-src` was refreshed from GitHub `FunAudioLLM/Fun-ASR` main:

`b14bdfca7a78d69092a9a018a25425abdb63e2d6`

## Decision

Keep `FunAudioLLM/Fun-ASR-Nano-2512` as the default because it is still the latest official Nano base model and best matches the user's common Chinese/English/Japanese video transcription workflow.

Use `FunAudioLLM/Fun-ASR-MLT-Nano-2512` only when the user explicitly needs broader multilingual support.

For open-source users, do not require model weights to be committed into the skill. Let `scripts/bootstrap.py --download-model base` or `--download-model mlt` populate the local cache on first use.

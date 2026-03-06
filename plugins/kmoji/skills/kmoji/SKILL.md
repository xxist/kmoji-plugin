---
name: kmoji
description: ⦤╭ˆ⊛◡⊛ˆ╮⦥ Generates kaomojis (Japanese-style text emoticons) on demand. Use when the user asks to generate a kaomoji, create a text emoticon, make a text face, or wants an expressive emoticon. Trigger phrases include "generate kaomoji", "make a kaomoji", "text face", "emoticon". Supports moods like happy, sad, angry, cute, and neutral.
argument-hint: "[mood] [count] - optional mood: happy, sad, angry, cute, neutral. Optional count: 1-10. Leave blank for 3 random."
license: Apache-2.0 WITH Commons-Clause-1.0
metadata:
  author: Richard Best (bestbuilds.io)
  version: 1.0.0
  tags: [kaomoji, emoticon, unicode, text-art]
---

# Kaomoji Generator

Generate kaomojis (Japanese-style text emoticons) by running a bundled Python script that assembles Unicode character parts into unique text faces.

## Instructions

### Step 1: Parse user input

Extract the mood and count from `$ARGUMENTS` or the user's natural language request. Valid moods: `happy`, `sad`, `angry`, `cute`, `neutral`. Count defaults to 3 (max 10).

### Step 2: Run the generator

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate.py $ARGUMENTS
```

Arguments:
- `mood` (optional): happy, sad, angry, cute, neutral
- `count` (optional): number of kaomojis, 1-10, default 3
- `--json`: output as JSON with metadata

Examples:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate.py              # 3 random
python ${CLAUDE_SKILL_DIR}/scripts/generate.py happy         # 3 happy
python ${CLAUDE_SKILL_DIR}/scripts/generate.py angry 5       # 5 angry
python ${CLAUDE_SKILL_DIR}/scripts/generate.py cute --json   # 3 cute as JSON
```

### Step 3: Display the output

Display generated kaomojis as plain text — no code blocks — so they render properly. If the user asked for a specific mood, include the mood label.

## How It Works

Each kaomoji is built from 6 optional layers concatenated left-to-right:

```
[background] [hands] [species] [features] [eyes] [mouth] [eyes] [features] [species] [hands] [background]
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `UnicodeEncodeError` on Windows | The script forces UTF-8 stdout automatically. If it still fails, run with `PYTHONIOENCODING=utf-8`. |
| `python` not found | Try `python3` instead. Requires Python 3.6+. |
| Characters render as boxes | Your terminal font doesn't support these Unicode characters. Try a font with broad Unicode coverage (e.g., Noto Sans, Cascadia Code). |
| No output for a mood | All moods have mapped characters. Check spelling — must be exactly: happy, sad, angry, cute, neutral. |

# KMOJI - ⦤╭ˆ⊛◡⊛ˆ╮⦥ Kaomoji Generator & Vibe Coding Plugin

An open-source Claude Code plugin that generates unique kaomojis and auto-integrates them into your vibe coding sessions.

[Buy Me A Coffee](https://buymeacoffee.com/cryptor1ch) |
[kmoji.io](https://kmoji.io/) -- REST API

```
╔═══════════════════════════════════════════╗
║  ██╗  ██╗███╗   ███╗ ██████╗    ████╗██╗  ║
║  ██║ ██╔╝████╗ ████║██╔═══██╗     ██║██║  ║
║  █████╔╝ ██╔████╔██║██║   ██║     ██║██║  ║
║  ██╔═██╗ ██║╚██╔╝██║██║   ██║     ██║██║  ║
║  ██║  ██╗██║ ╚═╝ ██║╚██████╔╝███████╗██║  ║
║  ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ║
╚═══════════════════════════════════════════╝
```

## Installation

### Quick Start (recommended)

```bash
npx kmoji
```

This launches an interactive installer where you choose:

1. **Install method:**
   - **Plugin** -- Registers KMOJI as a Claude Code plugin, giving you `/kmoji` slash command and the `vibe-kmoji` background skill
   - **CLAUDE.md** -- Injects kaomoji instructions directly into your CLAUDE.md file
   - **Both** -- Plugin + CLAUDE.md templates

2. **CLAUDE.md features** (if selected):
   - **Vibe Kaomojis** -- Claude auto-generates unique kaomojis for success, errors, debugging, and more
   - **PR Signatures** -- Kaomoji signatures on pull requests and commits
   - **All** -- Everything

3. **Scope** (for CLAUDE.md): Global (all projects) or project-only

After install, **restart Claude Code** for plugin changes to take effect.

### Manual: Plugin Marketplace

If you prefer the standard `claude plugin` CLI:

```bash
# Add KMOJI as a marketplace
claude plugin marketplace add xxist/kmoji-plugin

# Install the plugin
claude plugin install kmoji@kmoji
```

### Manual: CLAUDE.md Only

If you just want the CLAUDE.md templates without the plugin system, copy the relevant template into your CLAUDE.md:

- **Vibe Kaomojis:** [templates/vibe-kmoji.md](templates/vibe-kmoji.md)
- **PR Signatures:** [templates/pr-signature.md](templates/pr-signature.md)

Replace `KMOJI_GENERATOR_PATH` with the absolute path to `skills/kmoji/scripts/generate.py`.

### Uninstall

```bash
npx kmoji remove
```

Interactively removes the plugin registration, CLAUDE.md blocks, and hooks.

### Check Status

```bash
npx kmoji status
```

Shows what's currently installed: plugin registration, CLAUDE.md injection, hooks.

## What It Does

Once installed, Claude Code will **generate** unique kaomojis using a Python script with hundreds of Unicode character parts -- not static text. Every kaomoji is different.

| Context | What happens |
|---------|-------------|
| Task completed | `↜╭ि ╰❤︎ت❤︎╯ ॏ╮` |
| Build/test failure | `ʕ╥﹏╥ʔ` |
| Debugging | `ᒋ(⊙_⊙)ᘃ` |
| Starting new work | `⫹╭ˆ◕ᗢ◕ˆ╮⫺` |
| PR signatures | `⪕╭ˆ◕ᗜ◕ˆ╮⪖` |

## Installation Methods Compared

| Feature | Plugin | CLAUDE.md | Both |
|---------|--------|-----------|------|
| `/kmoji` slash command | Yes | No | Yes |
| Vibe kaomoji (background) | Yes | Yes | Yes |
| PR signatures | No | Yes | Yes |
| Error hook | No | Yes | Yes |
| Requires restart | Yes | No | Yes |

**Plugin** is the recommended approach -- it uses Claude Code's native plugin system and the `/kmoji` command works in any project without touching CLAUDE.md.

**CLAUDE.md** is the legacy approach -- it works everywhere but modifies your CLAUDE.md file. Useful if you want PR signatures or error hooks.

**Both** gives you everything.

## Skills

### kmoji (user-invocable)

Slash command to generate kaomojis on demand:

```
/kmoji              # 3 random kaomojis
/kmoji happy        # 3 happy kaomojis
/kmoji angry 5      # 5 angry kaomojis
```

### vibe-kmoji (background)

Automatically loaded skill that teaches Claude to add contextual kaomojis to responses. Runs the generator script behind the scenes -- you don't invoke it directly.

## Generator (standalone)

Generate kaomojis from the terminal:

```bash
npx kmoji generate              # 3 random kaomojis
npx kmoji gen happy              # 3 happy kaomojis
npx kmoji gen angry 5            # 5 angry kaomojis
```

Or run the Python script directly:

```bash
python skills/kmoji/scripts/generate.py              # random
python skills/kmoji/scripts/generate.py happy        # by mood
python skills/kmoji/scripts/generate.py angry 5      # count
python skills/kmoji/scripts/generate.py cute --json  # JSON output
python skills/kmoji/scripts/generate.py happy --color # color-coded output
```

Moods: `happy`, `sad`, `angry`, `cute`, `neutral`

Requires Python 3.6+. No dependencies.

## How It Works

Kaomojis are assembled from 6 layers of Unicode characters:

```
[background] [hands] [species] [features] [eyes] [mouth] [eyes] [features] [species] [hands] [background]
```

Each layer is optional. The generator picks parts randomly (or filtered by mood for eyes/mouths) and concatenates them. The parts library contains hundreds of Unicode characters across species, eyes, mouths, hands, backgrounds, and features.

## What Gets Modified

The installer touches these files depending on your choices:

| Choice | File | What changes |
|--------|------|-------------|
| Plugin | `~/.claude/plugins/installed_plugins.json` | Adds `kmoji@kmoji` entry pointing to install path |
| Plugin | `~/.claude/settings.json` | Adds `kmoji@kmoji: true` to `enabledPlugins` |
| CLAUDE.md (global) | `~/.claude/CLAUDE.md` | Adds `<!-- KMOJI:START -->` block |
| CLAUDE.md (project) | `.claude/CLAUDE.md` | Adds `<!-- KMOJI:START -->` block |
| Vibe hook | `~/.claude/settings.json` or `.claude/settings.json` | Adds `kmoji-vibe` hook |

All changes are wrapped in markers and can be cleanly removed with `npx kmoji remove`.

## Repo Structure

```
kmoji/
  bin/
    kmoji.js                       # CLI entry point (npx kmoji)
  templates/
    vibe-kmoji.md                  # CLAUDE.md template for vibe mode
    pr-signature.md                # CLAUDE.md template for PR signatures
  .claude-plugin/
    plugin.json                    # Plugin manifest
    marketplace.json               # Self-hosted marketplace manifest
  skills/
    kmoji/
      SKILL.md                     # Generator skill entry point
      scripts/
        generate.py                # Python generator script
    vibe-kmoji/
      SKILL.md                     # Auto-integration skill (background)
  package.json
  README.md
  LICENSE
```

## Requirements

- **Claude Code** (any recent version with plugin support)
- **Python 3.6+** (for the generator script)
- **Node.js 16+** (for `npx kmoji` CLI)

## Contributing

Contributions welcome:
- Add new Unicode character parts to `generate.py`
- Add new mood categories
- Improve contextual triggers
- Report character rendering issues
- Suggest new kaomoji use cases

## License

Apache 2.0 with Commons Clause - See [LICENSE](LICENSE)

Free to use, modify, and share. Cannot be sold as a standalone product or service.

## Credits

Created by **Richard Best**

- [bestbuilds.io](https://bestbuilds.io)
- [kmoji.io](https://kmoji.io) -- REST API
- [Buy Me A Coffee](https://buymeacoffee.com/cryptor1ch)

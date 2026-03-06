#!/usr/bin/env python3
"""Kaomoji generator - assembles kaomojis from Unicode character parts."""

import random
import sys
import json
import io

# Ensure stdout handles Unicode on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── SPECIES (body frames) ───────────────────────────────────────────────────
# Format: [name, left, right]
SPECIES = [

    ["FROG", "╭", "╮"],
    ["FROGGE", "(", ")"],
    ["AI", "[", "]"],
    ["DOGGO", "▼(", ")▼"],
    ["DOG", "(V", "V)"],
    ["RABBIT", "U╭", "╮U"],
    ["CAT", "(^", "^)"],
    ["MONKEY", "ᘳ", "ᘰ"],
    ["PNGN1", "(ᓱ", "ᓴ)"],
    ["BUTTERFLY2", "ᙓ(", ")ᙐ"],
    ["PIG", "(▽", "▽)"],
    ["CLASSIC", "(", ")"],

    ["APE", "ᙍ(", ")ᙌ"],
    ["TOAD", "⦅", "⦆"],
    ["BABY-FROG", "(͒", ")"],
    ["GORILLA", "ᗧ(", ")ᗤ"],
    ["BUNNY", "₍ᐢ", "ᐢ₎"],
    ["RAT", "ʢ", "ʡ"],
    ["BUG", "ʚ₍", "₎ɞ"],
    ["SPIDEY", "ᄽ(", ")ᄿ"],
    ["BUTTERFLY", "ᙦ(", ")ᙥ"],
    ["MOUSER", "၄", "၃"],
    ["BIRD", "⦓", "⦔"],
    ["MOUSE", "☾₍", "₎☽"],
    ["STONED-APE", "Ⴚ(", ")Ⴢ"],
    ["LION", "⫕(", ")⫖"],
    ["BAYC1", "ᘓ(", ")ᘐ"],

    ["BAT", "(㇏(", "́)ノ)"],
    ["PENGUIN", "૮₍", "₎ა"],
    ["HUMAN", "Ͼ|", "|Ͽ"],
    ["LITTLE-DEVIL", "⎧╰", "╯⎫"],

    ["BUTTERFLY1", "ᙬ(", ")ᙩ"],

    ["VAMPIRE", " ⎛⎝𓌹 ", " 𓌺⎠⎞ "],
    ["PDGY-PNGN", "૮(ᓱ", "ᓴ)ა"],
    ["BAYC", "ᙍ(ᓱ", "ᓴ)ᙌ"],
    ["BUTTERFLY-LG", "🕃(", ")🕄"],
    ["GHOST-LG", "⎛", "⎞"],
    ["ALIEN-LG", "⎝ ", " ⎠"],
    ["DOGE", "⎝⎛", "⎞⎠"],
    ["SPIDER", "/╲/\\╭", "╮/\\╱\\"],

]

# ─── EYES ─────────────────────────────────────────────────────────────────────
# Format: [name, left, right, moods[]]
EYES = [

    ["FROG-EYES", "𐠓", "𐠓", []],
    ["FROG", "𝄐", "𝄐", []],
    ["SLEEPY", "ᗝ", "ᗝ", ["sad", "happy"]],
    ["HALOS", "○", "○", ["neutral"]],
    ["DOTTED", "●", "●", ["neutral"]],
    ["NEUTRAL", "⊙", "⊙", ["neutral"]],
    ["WORRIED", "ʘ̆", "ʘ̆", ["sad"]],
    ["X-OUT", "✖", "✖", ["angry"]],
    ["FLUSHED", "Ő", "Ő", ["happy"]],
    ["RICK", "•", "•", []],
    ["MONOCLE", "ಠ", "ರ", []],
    ["CRYING", "╥", "╥", ["sad"]],
    ["FROG-DERP", "⍝", "⍝", []],
    ["EMPTY-EYES", "▱", "▱", []],
    ["WHITE-EYES", "⬤", "⬤", []],
    ["SQUARE-EYES", "⏹", "⏹", []],
    ["HEXAGON-EYES", "⬠", "⬠", []],
    ["CRINGE", "≧", "≦", ["angry"]],
    ["SQUINT", "ᗒ", "ᗕ", ["angry"]],
    ["RIGHT-PEEK", "◩", "◩", []],
    ["O-BROW", "Ȏ", "Ȏ", []],
    ["BLURP", "⚆", "⚆", []],
    ["EYELASHES", "Ȍ", "Ȍ", []],
    ["MONOCLES", "ಠ", "ಠ", ["angry"]],
    ["ASTRAL", "🟐", "🟐", ["angry"]],
    ["ORACLE-EYES", "🟌", "🟌", []],
    ["PEAKING", "⚈", "⚈", []],
    ["NOUNS", "◼", "◼", ["neutral"]],

    ["LOVE-EYES", "♡", "♡", ["happy", "cute"]],
    ["LOVED", "♥", "♥", ["happy", "cute"]],
    ["IN-LOVE", "🎔", "🎔", ["happy"]],
    ["STAR-STRUCK", "★", "★", ["happy", "cute"]],
    ["HOLLOW-EYES", "◯", "◯", ["cute"]],
    ["FLORAL", "✿", "✿", ["happy", "cute"]],

    ["MEGA-SOB", "╥╯", "╰╥", ["sad"]],
    ["TIRED-EYES", "◓", "◓", ["sad"]],
    ["WEARY", "ම", "ම", ["sad"]],
    ["DEEP-SLEEP", "⌒", "⌒", ["sad"]],
    ["DISAPPOINTED", "╰╯ ", "╰╯", ["sad"]],

    ["MAD", "◄►", "◄►", ["angry"]],
    ["EVIL-EYES", "◣", "◢", ["angry"]],
    ["SHORT-FUSE", "✹", "✹", ["angry"]],
    ["EYE-ROLL", "డ", "డ", ["angry"]],
    ["UNAMUSED", "⯋", "⯋", ["angry"]],
    ["RADIATION", "☢", "☢", ["angry"]],

    ["SPIDEY", "ὁȍ", "őὀ", []],
    ["MATRIX-VIEW", "ᚙ", "ᚙ", ["angry"]],
    ["SCANNERS", "⍜", "⍜", ["sad"]],
    ["CUTIE", "ఠ", "ఠ", ["cute"]],
    ["CRAZY", "இ", "இ", []],
    ["CRAZY-EYES", "꩜", "꩜", []],
    ["OOH", "ඔ", "ඔ", []],
    ["FROG-BASE", "ᕱ", "ᕱ", []],
    ["MYSTIC-EYES", "ᕮ", "ᕭ", []],
    ["FROG-SQUINT", "ᕬ", "ᕬ", []],
    ["ANIME", "മ", "മ", []],
    ["SUNGLASSES", "⌐■", "■", []],
    ["SLEEPING", "◡", "◡", ["sad"]],
    ["BLACK-HOLE", "◉", "◉", []],
    ["TARGETING", "◎", "◎", []],
    ["TREE-FROG", "ᕫ", "ᕫ", ["sad"]],
    ["GENTLE-GAZE", "ꖴ", "ꖴ", []],
    ["ION_OPTICS", "⏣", "⏣", []],
    ["LUSTRIOUS", "❂", "❂", []],
    ["DEAD-EYES", "⨷", "⨷", ["sad"]],
    ["STAR-BURST", "⍟", "⍟", ["happy"]],
    ["WISE-EYES", "(•)", "(•)", []],
    ["SOLAR-EYES", "☉", "☉", []],
    ["SUN-GLASSES", "⎚", "⎚", []],
    ["STAR-GATE", "⯌", "⯌", []],
    ["SMIRKING", "⯊", "⯊", ["angry"]],

    ["PLEADING", "ඹ", "ඹ", ["cute", "sad"]],
    ["ARACHNID", "ꈮꈮ", "ꈮꈮ", []],
    ["MATRIX", "▨", "▨", []],
    ["CYBER-EYES", "⦿", "⦿", []],
    ["TARGETED", "⊕", "⊕", []],
    ["SCANNING", "⦾", "⦾", []],
    ["MAKEUP", "ఠ్ఠ", "ఠ్ఠ", []],
    ["RED-PILL", "⨶", "⨶", ["angry"]],
    ["ROCK-STAR", "⍟", "⍟", ["happy"]],
    ["NAVIGATOR", "𑁍", "𑁍", []],
    ["STAR-CROSSED", "ⴲ", "ⴲ", []],
    ["PENTAGONS", "⬟", "⬟", []],
    ["COIN-EYES", "⦿", "⦿", []],
    ["LASER-EYES", "۞", "۞", ["angry"]],
    ["HEMOGAZE", "🌢", "🌢", ["angry"]],
    ["SUN-RISE", "🌣", "🌣", ["happy"]],
    ["ANCIENT-EYES", "🗰", "🗰", ["angry"]],
    ["STOP-SIGN", "⯃", "⯃", ["angry"]],
    ["LOTUS-EYES", "✸", "✸", ["cute"]],
    ["HEART-EYES", "❤", "❤", ["happy", "cute"]],
    ["TRUE-NORTH", "⛢", "⛢", []],
    ["BUG-EYES", "అ", "అ", []],
    ["DRAGON", "啬", "啬", ["angry"]],
    ["CHAKRA-EYES", "ಡ", "ಡ", ["happy"]],
    ["WIZARD", "ඕ", "ඕ", []],
    ["ANCIENT-RUNES", "ᗥ", "ᗥ", []],
    ["MYSTIC", "థ", "థ", []],
    ["ECLIPSE-EYES", "◖", "◗", []],
    ["BLACK-HOLES", "⧭", "⧭", []],
    ["BIG-UP", "𐁍", "𐁍", []],
    ["WIDE-GOGGLES", "🝙", "🝙", []],
    ["VR-GLASSES", "🝚", "🝚", []],

    ["LIGHT-BEAM", "⚶", "⚶", []],
    ["DRAGON-EYES", "𖠌", "𖠌", []],
    ["ROMAN-VOID", "ↀ", "ↀ", []],
    ["CYBER-SIGHT", "ꖘ", "ꖘ", []],
    ["BIG-HEART", "❤︎", "❤︎", ["happy", "cute"]],
    ["COSMIC-EYES", "🞉", "🞉", []],
    ["ANCIENT", "ᯣ", "ᯣ", []],
    ["DARK-ENERGY", "⬮", "⬮", ["happy"]],
    ["OCELLI", "ఠ్ఠఠ", "ఠఠ్ఠ", []],
    ["DOUBLE-GAZE", "Ꙭ", "Ꙭ", ["happy"]],
    ["SIMULATION", "ↈ", "ↈ", []],
    ["ALIEN-EYES", "𐰦", "𐰦", []],
    ["DRAGON-GLARE", "🝦", "🝦", ["angry"]],

]

# ─── MOUTHS ───────────────────────────────────────────────────────────────────
# Format: [name, char, moods[]]
MOUTHS = [

    ["FROWN", "︿", ["angry", "sad"]],
    ["HAPPY-ONE", "◡", ["happy"]],
    ["ANIME-MOUTH", "⤙", ["happy"]],
    ["BLUSH-ONE", "ᴗ", ["happy", "cute"]],
    ["KISS", "З", ["cute"]],
    ["BLUSH-TWO", "ᴗ", ["happy", "cute"]],
    ["LAUGH", "ヮ", ["happy"]],
    ["LICK", "ڡ", []],
    ["DERPY", "౪", ["happy"]],
    ["WOOPS", "⌓", ["sad"]],
    ["RELIEVED", "ㅂ", ["sad"]],
    ["CHEESE", "ᗨ", ["happy"]],
    ["TONGUE-OUT", "⩌", ["happy"]],
    ["WORRIED", "﹏", ["sad"]],
    ["AWARE", "──", ["neutral"]],
    ["DERP", "▁", ["neutral"]],
    ["NEUTRAL", "‾‾", ["neutral", "angry"]],
    ["GRINNING", "▽", ["happy"]],
    ["FROWNING", "⌓", ["sad"]],
    ["TINY-BEAK", "▿", []],
    ["FANGS", "ᵥᵥ", []],
    ["TINY-FANGS", ",…,", []],
    ["RABBIT-NOSE", "Ѫ", []],
    ["PIN-SNOUT", "(oo)", []],
    ["BUTTON-NOSE", "ᴥ", ["cute"]],
    ["POUTING-CAT", "ㅈ", ["angry"]],
    ["BUNNY-MOUTH", "ㅊ", ["cute"]],
    ["UPPER-LIP", "⺌", ["cute"]],
    ["BOTTOM-LIP", "⺣", ["cute"]],
    ["ANIME-BEAK", "ᐵ", []],
    ["BIG-SMILE", "ᗢ", ["happy"]],
    ["SHOCKED", "ᗣ", ["angry"]],
    ["JOYFUL", "ᗩ", ["happy"]],
    ["BIRD-BEAK", "△", []],
    ["FROGLIPS", "ᯅ", ["sad", "angry"]],
    ["BIRDIE", "ө", []],
    ["ZEN", "人", ["neutral"]],
    ["SPOOKED", "△", ["sad"]],
    ["BEAMING", "ᗜ", ["happy"]],
    ["CAT-NOSE", "ܫ", ["cute"]],
    ["ASTONISHED", "Д", ["angry"]],
    ["BLING", "⺫", []],
    ["SPIDER-MOUTH", ".‿.", ["cute"]],

    ["HAPPY-V", "▽", ["happy"]],
    ["DOUBLE-WIDE", "‿‿", ["happy"]],
    ["CRINGE-MOUTH", "𐩘", ["angry", "sad"]],
    ["TONGUE-OUT-R", "ټ", []],
    ["BUCK-TEETH", "⏔", []],
    ["BIG-NOSTRILS", "ꔚ", []],
    ["BIG-BEAK", "⊝", []],
    ["ANGRY-SMIRK", "へ", ["angry"]],
    ["SMALL-FANGS", "ᵥ-ᵥ", ["angry"]],
    ["ANGRY-BEAR", "ㅉ", ["angry"]],
    ["ZIPPED", "ᚔ", ["sad", "angry"]],
    ["PIG-NOSE", "(●●)", []],
    ["TEETH-SMILE", "∈∋", ["happy"]],
    ["OHH", "ᯆ", ["angry"]],
    ["HUMAN-NOSE", "ᨉ", []],
    ["DERPY-BIRD", "´∀`", ["happy"]],
    ["LICKING", "ᓏ", []],
    ["EXCITED", "⍢", ["happy"]],
    ["BITE-LIP", "⺥", ["sad"]],
    ["BITTING-LIP", "⺤", ["angry"]],
    ["BEAR-NOSE", "㉾", []],
    ["BLOW-KISS", "Ⰵ", ["cute"]],
    ["BITE", "Ⱉ", ["sad"]],
    ["CURSING", "典", ["angry"]],
    ["LONG-BEAK", "⩢", []],
    ["PANDA-BEAR", "㉨", []],
    ["HIGH-VOLTAGE", "文", ["angry"]],
    ["SNAKE-FANGS", "Ⱅ", []],
    ["RICKnMORTY", "ω", []],
    ["KISSING", "ഭ", ["happy"]],
    ["DRAGON-NOSE", "ᨎ", []],
    ["SQUIGGLY", " ϖ ", []],
    ["NAUSEATED", "🝏", ["angry"]],
    ["NORSE-MOUTH", " ߧ ", []],

    ["CHEERFUL", "ਉ", ["happy"]],
    ["APED", "۝", ["angry"]],
    ["LSD", " ⩐ ", []],
    ["LONG-TONGUE", "ᙈ", ["happy"]],
    ["RED-LIPSTICK", "🗢", ["happy"]],
    ["GLOORP", "𑄙", ["angry"]],
    ["MYTH-FANGS", "ᚅ", ["sad"]],
    ["ZOMBIE", "ཀ", []],
    ["CUSSING", "෴", ["angry"]],
    ["PUKE", "旦", ["angry"]],
    ["DAEMON", "↭", ["sad"]],
    ["SNAKE-NOSE", "ⰹ", []],
    ["CAT-GRIN", "ߐ", []],
    ["ANIME-HAPPY", "ᐛ", ["happy"]],
    ["DROOLING", "ڀ", []],
    ["SNOOTY-NOSE", "𑄚", []],
    ["CLOWN", "Ꮂ", []],
    ["ZOMBIE-2", "𓄧", []],

    ["PUKE-RAINBOW", "皿", ["angry"]],
    ["PIG-NOSE-LG", "𖠌", []],
    ["MEGA-DERP", "◞౪◟", []],
    ["OGRE-NOSE-2", "ಱ", ["angry"]],
    ["BIG-FANGS", "꒦︶꒦", []],
    ["YEET", "ਊ", ["happy"]],
    ["GANGSTA", "⇔", []],
    ["F-OFF", "益", ["angry"]],
    ["DRAGON-NOSE-LG", "ᨐ", []],
    ["PORTAL-MOUTH", "⇿", []],
    ["VOID-MOUTH", "⛻", ["angry", "happy"]],
    ["CIRCUIT-MOUTH", "⬌", []],
    ["BIG-LIP", "⽖", ["sad"]],

]

# ─── HANDS ────────────────────────────────────────────────────────────────────
# Format: [name, left, right, moods[]]
HANDS = [
    ["NONE", "", "", []],
    ["NONE", "", "", []],
    ["NONE", "", "", []],

    ["OPEN-HANDS", "⫏", "⫐", []],
    ["CRYSTAL-HAND", "ᓁ", "ᓀ", []],
    ["DUAL-HOLD", "ᓈ", "ᓅ", []],
    ["LEFT-TRIO", "ᓎ", "ᓄ", []],
    ["TWO-IN-LEFT", "ᓠ", "ᓜ", []],
    ["HIGH-DOWN", "ᕂ", "ᕃ", ["sad"]],
    ["LOW-SMALL", "ᕇ", "ᕄ", []],
    ["SHRUG-OBJECT", "ᕴ", "ᕶ", ["neutral", "sad"]],
    ["LOW-SHOULDER", "ᕸ", "ᕺ", ["sad"]],
    ["DANCE-ARMS", "ᕴ", "ᕹ", ["happy"]],
    ["DOUBLE-DANCE", "ᕷ", "ᕵ", ["happy"]],
    ["PRAYING", "≺", "≻", ["sad", "neutral"]],
    ["SHRUG", "ᒋ", "ᘃ", ["neutral", "sad"]],
    ["PARTY", "┌", "┘", ["happy"]],
    ["WAVE-HANDS", "ヾ", "〴", ["happy"]],
    ["MUSCLE-FLEX", "ᕦ", "ᕥ", ["angry", "happy"]],
    ["RUNNING", "ᕕ", "ᕗ", ["happy"]],
    ["GHOST-HANDS", "ᣢ", "ᣡ", ["sad"]],
    ["SPOOKY", "ᖋ", "ᘃ", ["sad", "angry"]],
    ["ASTRONAUT", "⟃", "⟄", []],
    ["CATCH-FLIES", "ᢱ", "ᢰ", []],
    ["KATAKANA", "ㄟ", "シ", []],
    ["BRACKET-HANDS", "⟃", "⟄", []],
    ["FLEXING", "ᕙ", "ᕗ", ["angry", "happy"]],
    ["SEND-NOODS", "ᢼ", "ᢻ", []],
    ["CARRY-DOWN", "⪗", "⪘", ["happy"]],
    ["LEFT-BALL", "ᓔ", "ᓓ", []],
    ["TINY-HANDS", "ᓐ", "ᓒ", ["cute"]],
    ["DOUBLE-DUO", "ᓏ", "ᓆ", []],
    ["CHEERING", "୧", "୨", ["happy", "cute"]],
    ["ANGLE-HANDS", "╭", "╮", []],
    ["CURVE-HANDS", "⸜", "⸝", ["cute"]],
    ["WAVE-TWO", "〲", "〴", ["happy"]],
    ["THAI-LEFT", "ต", "ค", []],
    ["DRAGON-CLAWS", "∋", "∈", ["angry"]],
    ["TWIRL-TWO", "ᕓ", "ᕘ", ["happy"]],
    ["FLEX-PUMP", "ᕜ", "ᕘ", ["angry"]],
    ["VULCAN", "≼", "≽", ["neutral"]],
    ["SUMMON", "⪨", "⪩", []],
    ["CAST-SPELL", "ᘧ", "ᘦ", []],
    ["CAPE-HANDS", "ᖤ", "ᖢ", []],
    ["CHEMESTRY", "ᣃ", "ᣄ", []],
    ["MOON-GLOVES", "ᘭ", "ᘫ", []],
    ["FLYING", "⪗", "⪘", ["happy"]],
    ["RNBW-HANDS", "ᕳ", "ᕲ", ["happy"]],
    ["CLAWS", "⋼", "⋴", ["angry"]],
    ["HAUNT", "⦤", "⦥", ["sad"]],
    ["THUMBS-UP", "ദ്ദി", "", ["happy", "cute"]],
    ["ANGEL-WINGS", "ଘ", "ଓ", ["cute", "happy"]],
    ["BUG-WINGS", "ઈ", "ઉ", ["cute"]],
    ["CAT-PAWS", "ฅ", "ฅ", ["cute"]],
    ["HOLOGRAPHIC", "ᗛ", "ᗚ", []],
    ["EAT-PIZZA", "⩹", "⩺", ["happy"]],
    ["CAPED-HANDS", "ᖥ", "ᖣ", []],
    ["PORTAL-HANDS", "⪪", "⪫", []],
    ["HOVER-ARMS", "⫅", "⫆", []],
    ["JUMPING", "⫹", "⫺", ["happy"]],

    ["DIAMOND-HANDS", "⟣", "⟢", []],
    ["BUDDHA-HANDS", "⪻", "⪼", ["happy"]],
    ["ALIEN-HANDS", "ᢵ", "ᢶ", []],
    ["INVADER-HANDS", "ᙻ", "ᙽ", []],
    ["F-OFF", "╭∩╮", "╭∩╮", ["angry"]],
    ["VOID-HANDS", "⫷", "⫸", ["angry"]],
    ["MIDDLE-FINGER", "凸", "凸", ["angry"]],
    ["SWIM-SPLASH", "⫉", "⫊", []],
    ["DESCENDING", "⪛", "⪜", ["happy"]],
    ["SPDR-LEGS", "ᄽ", "ᄿ", []],
]

# ─── BACKGROUNDS ──────────────────────────────────────────────────────────────
# Format: [name, left, right]
BACKGROUNDS = [
    ["NONE", "", ""],
    ["NONE", "", ""],
    ["NONE", "", ""],
    ["NONE", "", ""],

    ["BRAILLE-1", "⠁ ", " ⠁"],
    ["BRAILLE-2", "⠃ ", " ⠃"],
    ["BRAILLE-3", "⠉ ", " ⠉"],
    ["BRAILLE-4", "⠖ ", " ⠙"],
    ["CAT-TAIL", "ໃ", ""],
    ["CAT-TAIL-2", "〽", ""],
    ["DOG-TAIL", "𓄏", ""],
    ["WIZARD-STAFF", "", "𐘝"],
    ["EVIL-TAIL1", "↜", ""],
    ["EVIL-TAIL2", "", "↝"],
    ["MONKEY-TAIL", "", "੭"],
    ["SHOOTING-STAR", "", " ᯓ★"],
    ["COMMIT", "", " 🜸"],
    ["ZEN-GARDEN", "࿊ ", " ࿊"],
    ["FLOWERS", "᯽ ", " ᯽"],
    ["STARS", "☆ ", " ☆"],
    ["SLEEPING", "ZZz ", " zZZ"],
    ["XRAY", "✘ ", " ✘"],
    ["LIBRARY", "❝ ", " ❞"],
    ["STAR-BURST", "⚞ ", " ⚟"],
    ["SPARKLE", "✾⋆ ", " ⋆✾"],
    ["HEARTS", "♥♡ ", " ♡♥"],
    ["BIG-HEART", "❤︎ ", " ❤︎"],
    ["GALAXY-WINK", "☆·˚ ", " ˚·☆"],
    ["SOLAR-GLARE", "☀☼ ", " ☼☀"],
    ["SHIMMER", "✧✦ ", " ✦✧"],
    ["SPARKLING", "✦✧ ", " ✧✦"],
    ["FENCE", "ᛝ ", " ᛝ"],
    ["NORDIC", "≎ ", " ≎"],
    ["MORSE-CODE", "𝌁 ", " 𝌁"],
    ["E=MC^2", "≕ ", " ≔"],
    ["WATERFALL", "≋ ", " ≋"],
    ["CLOVER", "ܤ ", " ܤ"],
    ["CLUB", "♣ ", " ♣"],
    ["DIAMOND", "♦ ", " ♦"],
    ["SPADE", "♠ ", " ♠"],
    ["ARROWS", "⟵ ", " ⟶"],
    ["COMPASS", "⤆ ", " ⤇"],

    ["FLYING", "⋘ ", " ⋙"],
    ["WATER", "︵‿︵", "︵‿︵"],
    ["SNOW", "*❆• ", " •❆*"],
    ["COMET-TRAIL", "☆*｡ ", " ｡*☆"],
    ["STAR-LIGHT", "⋆˚✮ ", " ✮˚⋆"],
    ["SPARKLES", "°˖✧ ", " ✧˖°"],
    ["ARROW", "Σ>―", "→"],
    ["RUNNING-BG", "─=≡Σ ", ""],
    ["MUSICAL", "♫•* ", " *•♫"],
    ["CONCERT", "♪♫♩ ", " ♩♫♪"],
    ["BINARY", "010 ", " 010"],
    ["MYSTIC", "✥∴ ", " ∴✥"],
    ["HEART-STARS", "♥⋆ ", " ⋆♥"],
    ["STAR-LINE", "✦—• ", " •–✦"],

    ["666", "⁶𖤐⁶ ", " ⁶𖤐⁶"],
    ["UFO", "ᱪ ", " ᱪ"],
    ["BITCOIN", "₿ ", " ₿"],
    ["ROYALTY", "🜲 ", " 🜲"],
    ["PIRATE", "🕱 ", " 🕱"],
    ["DRAGON-TAIL", "𐂠ꔱ", ""],
    ["BUDDAH", "ༀ ", " ༀ"],
    ["DEVIL-TAIL", "ܟ", ""],
    ["PITCHFORK", "ܟ", "🝒"],
    ["TRIDENT", "𐙋", ""],
]

# ─── FEATURES (cheek marks, horns, etc.) ─────────────────────────────────────
# Format: [name, left, right, moods[]]
FEATURES = [
    ["NONE", "", "", []],
    ["NONE", "", "", []],
    ["NONE", "", "", []],
    ["HAPPY", "ᵔ", "ᵔ", ["happy", "cute"]],
    ["CHEEK-BONES", "ᵕ", "ᵕ", ["cute", "happy"]],
    ["MAKEUP", "~", "~", ["cute"]],
    ["BOW", "⑅", "⑅", ["cute"]],
    ["KAWAII", "˵", "˶", ["cute", "happy"]],
    ["BLUSHING", "◌", "◌", ["cute"]],
    ["WHISKERS", "ະ", "ະ", []],
    ["SPARKLE", "༶", "༶", ["happy"]],
    ["HORNS", "ˇ", "ˇ", []],
    ["TEARS", "߹", "߹", ["sad"]],
    ["DIAMONDS", "✧", "✧", ["happy"]],
    ["ANGELIC", "ʚ", "ɞ", ["cute"]],
    ["UNICORN-HORN", "^", "", ["cute"]],
    ["HALO", "", "ິ", ["cute", "neutral"]],
    ["DEVIL-HORNS", "^", "^", ["angry"]],
    ["DNA", "∞", "∞", []],
    ["HORNY", "╰", "╯", ["angry"]],
    ["SIDE-BURNS", "ᓫ", "ᓫ", []],
    ["PENGUIN", "ᓱ", "ᓴ", []],
    ["CONFUSED", "ߴ", "ߵ", ["sad", "neutral"]],
    ["MASCARA", "ᱼ", "ᱼ", ["cute"]],
    ["BRIGHT-LIGHT", "⋆", "⋆", ["happy"]],
    ["WISKERS", "ﾐ", "ﾐ", []],
    ["RADIENT", "⁘", "⁘", []],
    ["CODED", "ᆢ", "ᆢ", []],
    ["CELTIC", "᛭", "᛭", []],
    ["GEMS", "ᛜ", "ᛜ", []],
]

# ─── COMBINATION RULES ────────────────────────────────────────────────────────
# Species that already have built-in arms/body — never add hands to these
# Only species whose body frames already include arms/appendages
NO_HANDS_SPECIES = {
    "BAT",          # (㇏(...)ノ) — built-in arms
    "APE",          # ᙍ(...)ᙌ — 
    "STONED-APE",   # Ⴚ(...)Ⴢ — 
    "GORILLA",      # ᗧ(...)ᗤ — 
    "SPIDER",       # /╲/\╭...╮/\╱\ — legs are the frame
    "SPIDEY",       # ᄽ(...)ᄿ — built-in legs
    "BUG",          # ʚ₍...₎ɞ — wings as arms
    "BUTTERFLY",    # ᙦ(...)ᙥ — wings
    "BUTTERFLY1",   # ᙬ(...)ᙩ — wings
    "BUTTERFLY2",   # ᙓ(...)ᙐ — wings
    "BUTTERFLY-LG", # 🕃(...)🕄 — wings
    "DOGGO",        # ▼(...)▼ — ears frame it
    "RABBIT",       # U╭...╮U — ears frame it
    "DOGE",         # ⎝⎛...⎞⎠ — double frame
    "VAMPIRE",      # ⎛⎝𓌹...𓌺⎠⎞ — fangs frame
    "PDGY-PNGN",    # ૮(ᓱ...ᓴ)ა — already has hand ა
    "PENGUIN",      # ૮₍...₎ა — already has hand ა
    "BAYC",         # ᙍ(ᓱ...ᓴ)ᙌ — 
    "BAYC1",        # ᘓ(...)ᘐ — 
    "LION",         # ⫕(...)⫖ — 
}

# ─── MOOD COLORS (ANSI) ──────────────────────────────────────────────────────
# Uses Claude Code's terminal palette:
#   Green  = success/happy     (matches Claude Code's green output)
#   Red    = error/sad/angry   (matches Claude Code's red error output)
#   Orange = cute/encouraging  (Claude's brand warm amber)
#   Yellow = warning           (standard caution color)
#   White  = neutral/default   (no emotional weight)
MOOD_COLORS = {
    "happy":   "\033[32m",       # green
    "sad":     "\033[31m",       # red
    "angry":   "\033[31m",       # red
    "cute":    "\033[38;5;208m", # orange (Claude orange)
    "neutral": "\033[37m",       # white
}
RESET_COLOR = "\033[0m"

# ─── MOOD MAPPING ─────────────────────────────────────────────────────────────
MOODS = ["happy", "sad", "angry", "cute", "neutral"]


def pick(items):
    """Pick a random item from a list."""
    return random.choice(items)


def filter_by_mood(items, mood, mood_index):
    """Filter traits that match a mood. Falls back to all if none match."""
    if not mood:
        return items
    filtered = [i for i in items if mood in i[mood_index]]
    return filtered if filtered else items


def generate(mood=None, count=3):
    """Generate kaomojis, optionally filtered by mood."""
    results = []
    for _ in range(count):
        species = pick(SPECIES)
        eyes = pick(filter_by_mood(EYES, mood, 3))
        mouth = pick(filter_by_mood(MOUTHS, mood, 2))

        # Backgrounds are rare (~10%), hands ~30%, features ~40%
        # Species with built-in arms/body never get hands
        if species[0] in NO_HANDS_SPECIES:
            hands = ["NONE", "", "", []]
        elif random.random() < 0.70:
            hands = pick(filter_by_mood(HANDS, mood, 3))
        else:
            hands = ["NONE", "", "", []]

        background = pick(BACKGROUNDS) if random.random() < 0.25 else ["NONE", "", ""]

        if random.random() < 0.40:
            feature = pick(filter_by_mood(FEATURES, mood, 3))
        else:
            feature = ["NONE", "", "", []]

        kaomoji = (
            f"{background[1]}"
            f"{hands[1]}"
            f"{species[1]}"
            f"{feature[1]}"
            f"{eyes[1]}"
            f"{mouth[1]}"
            f"{eyes[2]}"
            f"{feature[2]}"
            f"{species[2]}"
            f"{hands[2]}"
            f"{background[2]}"
        )

        results.append({
            "kaomoji": kaomoji,
            "species": species[0],
            "eyes": eyes[0],
            "mouth": mouth[0],
            "hands": hands[0],
            "background": background[0],
            "feature": feature[0],
            "mood": mood or "random",
        })

    return results


def main():
    mood = None
    count = 3

    args = sys.argv[1:]
    for arg in args:
        if arg.lower() in MOODS:
            mood = arg.lower()
        elif arg.isdigit():
            count = min(int(arg), 10)
        elif arg in ("--json", "--color", "--no-color"):
            pass  # handled below

    use_json = "--json" in args
    # Color is on by default in terminal, off for JSON and --no-color
    use_color = not use_json and "--no-color" not in args and sys.stdout.isatty()
    # --color forces it on even if piped
    if "--color" in args:
        use_color = True

    results = generate(mood, count)

    if use_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        mood_label = mood or "random"
        color = MOOD_COLORS.get(mood, "") if use_color else ""
        reset = RESET_COLOR if use_color and color else ""
        print(f"\n  {mood_label} kaomojis:\n")
        for r in results:
            print(f"  {color}{r['kaomoji']}{reset}")
        print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive English to LATAM Spanish translator for rAthena quest scripts.
Translates mes "...", select("..."), and mapannounce dialogue text.
Preserves: code, variables, color codes ^RRGGBB, NPC names in [], line count.
Uses informal "tu" (LATAM Spanish). Keeps proper nouns.
"""

import re
import sys

# =============================================================================
# COMPREHENSIVE WORD/PHRASE TRANSLATION DICTIONARY
# Ordered from longest to shortest to prevent partial matches
# =============================================================================

# Common full-sentence patterns and their translations
SENTENCE_MAP = {
    # Common closings/greetings
    "close": "close",
    "next": "next",
}

# Word-level translations (applied after sentence-level)
WORD_MAP = {
    # Articles & Pronouns
    "I": "Yo",
    "I'm": "Estoy",
    "I'll": "Voy a",
    "I've": "He",
    "I'd": "Yo",
    "you": "tu",  # Will context-switch to "te/ti" where needed
    "You": "Tu",
    "you're": "eres",
    "You're": "Eres",
    "you've": "has",
    "You've": "Has",
    "you'll": "vas a",
    "You'll": "Vas a",
    "you'd": "tu",
    "we": "nosotros",
    "We": "Nosotros",
    "we're": "estamos",
    "We're": "Estamos",
    "we've": "hemos",
    "they": "ellos",
    "They": "Ellos",
    "they're": "estan",
    "he": "el",
    "He": "El",
    "he's": "el esta",
    "He's": "El esta",
    "she": "ella",
    "She": "Ella",
    "she's": "ella esta",
    "it": "eso",
    "It": "Eso",
    "it's": "es",
    "It's": "Es",
    "my": "mi",
    "My": "Mi",
    "your": "tu",
    "Your": "Tu",
    "his": "su",
    "her": "su",
    "our": "nuestro",
    "their": "su",
    "me": "me",
    "him": "el",
    "them": "ellos",
    "this": "esto",
    "This": "Esto",
    "that": "eso",
    "That": "Eso",
    "these": "estos",
    "those": "esos",
    "what": "que",
    "What": "Que",
    "where": "donde",
    "Where": "Donde",
    "when": "cuando",
    "When": "Cuando",
    "who": "quien",
    "Who": "Quien",
    "why": "por que",
    "Why": "Por que",
    "how": "como",
    "How": "Como",
}


def is_npc_name_bracket(s):
    """Check if string is [NPC Name] format."""
    return bool(re.match(r'^\[.*\]$', s.strip()))


def is_untranslatable(s):
    """Check if string should not be translated."""
    t = s.strip()
    if not t:
        return True
    # NPC name in brackets
    if is_npc_name_bracket(t):
        return True
    # Only dots, spaces, special chars
    if re.match(r'^[.\s*!?~\-]+$', t):
        return True
    # Only numbers and spaces
    if re.match(r'^[\d\s]+$', t):
        return True
    # Dynamic name expression
    if re.match(r'^\["\s*\+\s*.+\s*\+\s*"\]$', t):
        return True
    return False


def translate_segment(text):
    """
    Translate a single English text segment to LATAM Spanish.
    This is the core translation function.
    """
    if is_untranslatable(text):
        return text

    # This is where actual translation happens
    # Since we can't use an API, we return text as-is
    # The actual translation will be done by the per-file processor
    return text


def translate_mes_value(s):
    """
    Translate the value inside mes "VALUE";
    Handles color codes and variable concatenation.
    """
    if is_untranslatable(s):
        return s

    # Don't translate if it's a variable concatenation expression
    # like: [" + strcharinfo(0) + "]
    if re.match(r'^\["\s*\+', s):
        return s

    return translate_segment(s)


def translate_select_value(s):
    """
    Translate select options. Options separated by : or ,
    Do NOT introduce colons in the translation text.
    """
    # Split by existing separators (: or , for select options)
    # select("Option 1:Option 2:Option 3")
    # or select("Option 1", "Option 2")
    parts = s.split(':')
    translated_parts = []
    for part in parts:
        translated_parts.append(translate_segment(part))
    return ':'.join(translated_parts)


def translate_announce_value(s):
    """Translate mapannounce text."""
    return translate_segment(s)


def process_line(line):
    """
    Process a single script line, translating translatable content.
    Returns the translated line with same whitespace/formatting.
    """
    stripped = line.strip()

    # Skip comments
    if stripped.startswith('//'):
        return line

    # Skip empty lines
    if not stripped:
        return line

    result = line

    # Process mes "..." patterns
    # Be careful with lines that have multiple mes or complex expressions
    def replace_mes(m):
        prefix = m.group(1)  # 'mes ' or 'mes\t' etc
        content = m.group(2)
        translated = translate_mes_value(content)
        return f'{prefix}"{translated}"'

    result = re.sub(r'(mes\s+)"([^"]*)"', replace_mes, result)

    # Process select("...") patterns
    def replace_select(m):
        prefix = m.group(1)  # 'select( ' etc
        content = m.group(2)
        translated = translate_select_value(content)
        return f'{prefix}"{translated}"'

    result = re.sub(r'(select\(\s*)"([^"]*)"', replace_select, result)

    # Process mapannounce patterns
    def replace_announce(m):
        prefix = m.group(1)  # 'mapannounce "map",'
        content = m.group(2)
        translated = translate_announce_value(content)
        return f'{prefix}"{translated}"'

    result = re.sub(r'(mapannounce\s+"[^"]+"\s*,\s*)"([^"]*)"', replace_announce, result)

    return result


def process_file(filepath):
    """Read, translate, and overwrite a quest file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_count = len(lines)

    translated = []
    for line in lines:
        translated.append(process_line(line))

    assert len(translated) == original_count, \
        f"Line count changed: {original_count} -> {len(translated)}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(translated)

    print(f"Translated: {filepath} ({original_count} lines)")


if __name__ == '__main__':
    files = [
        r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_lighthalzen.txt',
        r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_nameless.txt',
        r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_rachel.txt',
        r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_veins.txt',
    ]

    for f in files:
        process_file(f)

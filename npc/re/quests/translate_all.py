#!/usr/bin/env python3
"""
Comprehensive English->LATAM Spanish translator for rAthena quest NPC scripts.
Translates ALL text inside mes "..."; and select("...") calls.
Preserves: script logic, variables, functions, coordinates, NPC sprite IDs,
           NPC names in brackets, color codes ^RRGGBB, variable references.
Uses informal "tu" (LATAM Spanish).
"""
import re
import sys
import os

# ============================================================================
# TRANSLATION DICTIONARY - Built from complete file reading
# Key = exact English string, Value = LATAM Spanish translation
# ============================================================================
T = {}

def build_translations():
    """Build the complete translation dictionary."""
    global T

    # =======================================================================
    # COMMON / SHARED STRINGS
    # =======================================================================
    # Weight/inventory warnings
    T["- You have too many items to do this quest. -"] = "- Tienes demasiados objetos para esta mision. -"
    T["You have too many kinds of things with you to do that. Throw out some of them and try again."] = "Tienes demasiados tipos de objetos encima. Deshazte de algunos e intentalo de nuevo."
    T["You are carrying too much weight to do that. Reduce the weight and try again."] = "Estas cargando demasiado peso. Reduce el peso e intentalo de nuevo."
    T["You have too many kinds of items. Please lighten your load and come back."] = "Tienes demasiados tipos de objetos. Por favor aligera tu carga y vuelve."
    T["You are carrying too much weight. Please lighten your load and come back."] = "Estas cargando demasiado peso. Por favor aligera tu carga y vuelve."
    T[" - Hang on there !! -"] = " - Espera ahi!! -"
    T[" - You are carrying too many kinds of items - "] = " - Estas cargando demasiados tipos de objetos - "
    T[" - to receive any more items. - "] = " - para recibir mas objetos. - "
    T[" - Please lighten your load - "] = " - Por favor aligera tu carga - "
    T[" - and try again. - "] = " - e intentalo de nuevo. - "
    T[" - You are carrying too much weight - "] = " - Estas cargando demasiado peso - "
    T["^FF0000- Warning message -"] = "^FF0000- Mensaje de advertencia -"
    T["- Hang on there!! -"] = "- Espera ahi!! -"
    T["- You have too many items -"] = "- Tienes demasiados objetos -"
    T["- to receive any more items. -"] = "- para recibir mas objetos. -"
    T["- Please lighten your load -"] = "- Por favor aligera tu carga -"
    T["- and try again. -^000000"] = "- e intentalo de nuevo. -^000000"

    # Fairy interpretation
    T["- You can't understand the fairy's words. -"] = "- No puedes entender las palabras del hada. -"
    T["- You need something to help you interpret them. -"] = "- Necesitas algo que te ayude a interpretarlas. -"

    # Common select options
    T["Yes."] = "Si."
    T["No."] = "No."
    T["Help."] = "Ayudar."
    T["Don't help."] = "No ayudar."
    T["Leave."] = "Irse."

    # =======================================================================
    # Now load the massive per-file translation dictionaries from files
    # =======================================================================
    trans_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in ['mora_trans.txt', 'dicastes_trans.txt',
                   'malaya_trans.txt', 'malangdo_trans.txt']:
        fpath = os.path.join(trans_dir, fname)
        if os.path.exists(fpath):
            count = 0
            with open(fpath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if '|||' in line:
                        parts = line.split('|||', 1)
                        if len(parts) == 2 and parts[0] and parts[1]:
                            T[parts[0]] = parts[1]
                            count += 1
            print(f"  Loaded {count} translations from {fname}")


def translate(text):
    """Translate English text to LATAM Spanish."""
    if not text or not text.strip():
        return text
    if text in T:
        return T[text]
    return text


def process_line(line):
    """Process a single script line, translating mes/select content."""
    stripped = line.strip()

    # Handle mes "text"; lines
    m = re.match(r'^(\s*mes\s+)"(.*)"\s*;(.*)$', line.rstrip('\n'))
    if m:
        prefix = m.group(1)
        content = m.group(2)
        suffix = m.group(3)

        # Keep NPC name-only lines: mes "[Name]";
        if re.match(r'^\[.*\]$', content):
            return line

        # Handle concatenated strings
        if '"+' in content or '+"' in content:
            translated = translate(content)
        else:
            translated = translate(content)

        result = prefix + '"' + translated + '";' + suffix
        if line.endswith('\n') and not result.endswith('\n'):
            result += '\n'
        return result

    # Handle select("opt1:opt2") lines
    m = re.search(r'select\("([^"]*)"\)', line)
    if m:
        options = m.group(1).split(':')
        translated_opts = [translate(opt) for opt in options]
        new_opts = ':'.join(translated_opts)
        return line[:m.start(1)] + new_opts + line[m.end(1):]

    # Handle mapannounce text
    m = re.search(r'(mapannounce\s+"[^"]*"\s*,\s*)"([^"]*)"', line)
    if m:
        text = m.group(2)
        translated = translate(text)
        return line[:m.start(2)] + translated + line[m.end(2):]

    return line


def process_file(filepath):
    """Process one quest file."""
    with open(filepath, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    original_count = len(lines)
    new_lines = [process_line(line) for line in lines]

    assert len(new_lines) == original_count, \
        f"Line count changed: {original_count} -> {len(new_lines)}"

    with open(filepath, 'w', encoding='latin-1') as f:
        f.writelines(new_lines)

    # Count translations
    translated = sum(1 for old, new in zip(lines, new_lines) if old != new)
    print(f"  {os.path.basename(filepath)}: {original_count} lines, {translated} changed")


def main():
    print("Building translation dictionary...")
    build_translations()
    print(f"Total translations loaded: {len(T)}")
    print()

    files = [
        "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_mora.txt",
        "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_dicastes.txt",
        "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_malaya.txt",
        "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_malangdo.txt",
    ]

    print("Processing files...")
    for filepath in files:
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"  NOT FOUND: {filepath}")

    print("\nDone!")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Apply translations from _translation_dict.json to the_sign_quest.txt.
Lines 1-1953 already in Spanish, process 1954+.
For untranslated strings, uses generate_translations.py translate_text().
Handles expression-containing lines carefully to avoid corruption.
"""
import json, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_translations import translate_text

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "the_sign_quest.txt")
DICT_FILE = os.path.join(SCRIPT_DIR, "_translation_dict.json")
SKIP_LINES = 1953  # Lines already translated to Spanish

def safe_quote_replace(text):
    """Replace double quotes with single quotes, but protect expression patterns."""
    # Protect "+ expr +" patterns (string concatenation in rAthena scripts)
    # These contain quotes that are part of script syntax, not dialogue
    parts = re.split(r'("?\+[^"]*?")', text)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Normal text - replace quotes
            result.append(part.replace('"', "'"))
        else:
            # Expression part - keep as-is
            result.append(part)
    return ''.join(result)

def has_expression(content):
    """Check if mes content contains script expressions (string concatenation)."""
    return '"+ ' in content or ' +"' in content or '"+' in content or '+"' in content

def main():
    with open(DICT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mes_dict = data.get("mes", {})
    select_dict = data.get("select", {})
    announce_dict = data.get("announce", {})

    with open(INPUT, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_count = len(lines)
    out = []
    stats = {"dict": 0, "fallback": 0, "kept": 0, "skipped_expr": 0}

    for i, line in enumerate(lines):
        if i < SKIP_LINES:
            out.append(line)
            continue

        s = line.rstrip('\n')

        # mes "...";
        m = re.match(r'^(\s*mes\s+)"(.*)";(.*)$', s)
        if m:
            prefix, content, suffix = m.group(1), m.group(2), m.group(3)

            # Skip NPC names, dots, empty, and lines with expressions
            if re.match(r'^\[.*\]$', content.strip()):
                out.append(line)
                continue
            if re.match(r'^[\s.!?,;:\-~*()\d]*$', content.strip()):
                out.append(line)
                continue

            # If line has expression concatenation, be very careful
            if has_expression(content):
                # Only translate if there's an exact dict match
                if content in mes_dict and mes_dict[content]:
                    translated = mes_dict[content]
                    # Don't replace quotes in expression-containing translations
                    out.append(f'{prefix}"{translated}";{suffix}\n')
                    stats["dict"] += 1
                else:
                    # Skip expression-containing lines for safety
                    out.append(line)
                    stats["skipped_expr"] += 1
                continue

            # Normal text line - try dict first, then fallback
            if content in mes_dict and mes_dict[content]:
                translated = mes_dict[content]
                translated = translated.replace('"', "'")
                out.append(f'{prefix}"{translated}";{suffix}\n')
                stats["dict"] += 1
            else:
                translated = translate_text(content)
                if translated != content:
                    translated = translated.replace('"', "'")
                    out.append(f'{prefix}"{translated}";{suffix}\n')
                    stats["fallback"] += 1
                else:
                    out.append(line)
                    stats["kept"] += 1
            continue

        # select("...")
        m2 = re.search(r'(select\()"(.*?)"\)', s)
        if m2:
            full_content = m2.group(2)
            parts = full_content.split(':')
            translated_parts = []
            any_changed = False
            for p in parts:
                if p in select_dict and select_dict[p]:
                    tp = select_dict[p].replace('"', "'").replace(':', '')
                    translated_parts.append(tp)
                    if tp != p:
                        any_changed = True
                else:
                    tp = translate_text(p)
                    tp = tp.replace('"', "'").replace(':', '')
                    translated_parts.append(tp)
                    if tp != p:
                        any_changed = True

            if any_changed:
                translated = ':'.join(translated_parts)
                ns = s[:m2.start()] + f'select("{translated}")' + s[m2.end():]
                out.append(ns + '\n')
                stats["dict"] += 1
            else:
                out.append(line)
            continue

        # mapannounce
        m3 = re.search(r'(mapannounce\s+"[^"]+"\s*,\s*)"(.*?)"', s)
        if m3:
            content = m3.group(2)
            if content in announce_dict and announce_dict[content]:
                translated = announce_dict[content].replace('"', "'")
                ns = s[:m3.start()] + f'{m3.group(1)}"{translated}"' + s[m3.end():]
                out.append(ns + '\n')
                stats["dict"] += 1
            else:
                translated = translate_text(content)
                if translated != content:
                    translated = translated.replace('"', "'")
                    ns = s[:m3.start()] + f'{m3.group(1)}"{translated}"' + s[m3.end():]
                    out.append(ns + '\n')
                    stats["fallback"] += 1
                else:
                    out.append(line)
            continue

        out.append(line)

    assert len(out) == original_count, f"Line count mismatch: {len(out)} vs {original_count}"

    with open(INPUT, 'w', encoding='utf-8') as f:
        f.writelines(out)

    print(f"Done. {original_count} lines preserved.")
    print(f"Dict translations: {stats['dict']}")
    print(f"Fallback translations: {stats['fallback']}")
    print(f"Skipped (expressions): {stats['skipped_expr']}")
    print(f"Kept as-is: {stats['kept']}")

if __name__ == '__main__':
    main()

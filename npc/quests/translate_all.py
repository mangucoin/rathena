#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive English to LATAM Spanish translator for rAthena quest scripts.
Uses deep_translator (Google Translate) for translation.
Translates mes "...", select("..."), and mapannounce dialogue text.
Preserves: code, variables, color codes ^RRGGBB, NPC names in [], line count.
Uses informal "tu" (LATAM Spanish). Keeps proper nouns.
No colons introduced inside select() text.
"""

import re
import sys
import json
import time
import os

sys.stdout.reconfigure(encoding='utf-8')

from deep_translator import GoogleTranslator

# =============================================================================
# CONFIG
# =============================================================================
CACHE_FILE = 'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/translation_cache.json'
BATCH_SIZE = 50  # Google Translate batch size
RATE_LIMIT_DELAY = 0.5  # seconds between batches

FILES = [
    'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_lighthalzen.txt',
    'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_nameless.txt',
    'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_rachel.txt',
    'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_veins.txt',
]

# =============================================================================
# STRING EXTRACTION
# =============================================================================

def is_npc_name(s):
    """Check if string is just NPC name in brackets [Name]"""
    return bool(re.match(r'^\[.*\]$', s.strip()))

def is_skip_string(s):
    """Check if string should NOT be translated."""
    t = s.strip()
    if not t:
        return True
    # NPC name brackets
    if is_npc_name(t):
        return True
    # Only dots, spaces, special chars (no letters)
    if not re.search(r'[a-zA-Z]', t):
        return True
    # Dynamic name expression like [" + strcharinfo(0) + "]
    if re.match(r'^\["\s*\+', t):
        return True
    return False

def strip_color_codes(s):
    """Remove color codes for translation, return (stripped, [(pos, code)]"""
    codes = []
    def replacer(m):
        codes.append(m.group(0))
        return f'%%CC{len(codes)-1}%%'
    stripped = re.sub(r'\^[0-9A-Fa-f]{6}', replacer, s)
    return stripped, codes

def restore_color_codes(s, codes):
    """Restore color codes after translation."""
    for i, code in enumerate(codes):
        s = s.replace(f'%%CC{i}%%', code)
    return s

def strip_variables(s):
    """Remove variable references like " + varname + " for translation."""
    vars_found = []
    def replacer(m):
        vars_found.append(m.group(0))
        return f'%%VV{len(vars_found)-1}%%'
    # Pattern: " + expression + "  (e.g., " + strcharinfo(0) + ")
    stripped = re.sub(r'"\s*\+\s*[^"]+\s*\+\s*"', replacer, s)
    return stripped, vars_found

def restore_variables(s, vars_found):
    """Restore variable references after translation."""
    for i, v in enumerate(vars_found):
        s = s.replace(f'%%VV{i}%%', v)
    return s

def extract_all_strings(files):
    """Extract all unique translatable strings from all files."""
    all_strings = set()
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('//'):
                    continue
                # mes "..." patterns
                for m in re.finditer(r'mes\s+"([^"]*)"', line):
                    s = m.group(1)
                    if not is_skip_string(s):
                        all_strings.add(s)
                # select("...") patterns
                for m in re.finditer(r'select\(\s*"([^"]*)"', line):
                    s = m.group(1)
                    # Split by : and add each option if translatable
                    for option in s.split(':'):
                        if not is_skip_string(option):
                            all_strings.add(option.strip())
                    all_strings.add(s)  # Also add full string for direct replacement
                # mapannounce patterns
                for m in re.finditer(r'mapannounce\s+"[^"]+"\s*,\s*"([^"]*)"', line):
                    s = m.group(1)
                    if not is_skip_string(s):
                        all_strings.add(s)
    return all_strings

# =============================================================================
# TRANSLATION
# =============================================================================

def prepare_for_translation(s):
    """Prepare a string for translation by protecting non-translatable parts."""
    # Protect color codes
    protected = s
    color_codes = []
    def protect_color(m):
        color_codes.append(m.group(0))
        return f'XCLR{len(color_codes)-1}X'
    protected = re.sub(r'\^[0-9A-Fa-f]{6}', protect_color, protected)

    # Protect ''quoted'' text (keep as-is, these are often item names)
    quoted = []
    def protect_quoted(m):
        quoted.append(m.group(0))
        return f'XQOT{len(quoted)-1}X'
    protected = re.sub(r"''[^']*''", protect_quoted, protected)

    return protected, color_codes, quoted

def restore_protected(s, color_codes, quoted):
    """Restore protected elements after translation."""
    for i, code in enumerate(color_codes):
        s = s.replace(f'XCLR{i}X', code)
        s = s.replace(f'Xclr{i}X', code)
        s = s.replace(f'xclr{i}x', code)
        # Google translate sometimes adds spaces
        s = s.replace(f'XCLR {i}X', code)
        s = s.replace(f'XCLR{i} X', code)
        s = s.replace(f'XCLR {i} X', code)
    for i, q in enumerate(quoted):
        s = s.replace(f'XQOT{i}X', q)
        s = s.replace(f'Xqot{i}X', q)
        s = s.replace(f'xqot{i}x', q)
        s = s.replace(f'XQOT {i}X', q)
        s = s.replace(f'XQOT{i} X', q)
        s = s.replace(f'XQOT {i} X', q)
    return s

def post_process_translation(translated):
    """Post-process translation to use informal 'tu' and fix common issues."""
    # Replace formal 'usted' forms with informal 'tu'
    t = translated
    # Common formal -> informal replacements
    replacements = [
        ('usted', 'tu'),
        ('Usted', 'Tu'),
        ('ustedes', 'ustedes'),  # keep plural
    ]
    for formal, informal in replacements:
        t = t.replace(formal, informal)

    # Fix double spaces
    t = re.sub(r'  +', ' ', t)

    return t

def translate_batch(strings, translator, cache):
    """Translate a list of strings, using cache when available."""
    results = {}
    to_translate = []

    for s in strings:
        if s in cache:
            results[s] = cache[s]
        else:
            to_translate.append(s)

    if to_translate:
        # Prepare strings for translation
        prepared = []
        metadata = []  # (original, color_codes, quoted) for each
        for s in to_translate:
            p, cc, qq = prepare_for_translation(s)
            prepared.append(p)
            metadata.append((s, cc, qq))

        # Batch translate
        try:
            if len(prepared) == 1:
                translated_list = [translator.translate(prepared[0])]
            else:
                translated_list = translator.translate_batch(prepared)
        except Exception as e:
            print(f"  Translation error: {e}")
            # Fall back to individual translations
            translated_list = []
            for p in prepared:
                try:
                    translated_list.append(translator.translate(p))
                except Exception as e2:
                    print(f"  Individual translation error for '{p[:50]}...': {e2}")
                    translated_list.append(p)  # Keep original on error

        # Restore protected elements and post-process
        for i, (orig, cc, qq) in enumerate(metadata):
            if i < len(translated_list) and translated_list[i]:
                t = restore_protected(translated_list[i], cc, qq)
                t = post_process_translation(t)
                results[orig] = t
                cache[orig] = t
            else:
                results[orig] = orig
                cache[orig] = orig

    return results

def translate_all_strings(strings, cache_file):
    """Translate all strings using batched API calls with caching."""
    # Load cache
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f"Loaded {len(cache)} cached translations")

    translator = GoogleTranslator(source='en', target='es')

    strings_list = sorted(strings)
    total = len(strings_list)
    translated_count = 0

    print(f"Total strings to translate: {total}")

    # Process in batches
    for i in range(0, total, BATCH_SIZE):
        batch = strings_list[i:i+BATCH_SIZE]
        # Filter out already cached
        uncached = [s for s in batch if s not in cache]

        if uncached:
            results = translate_batch(uncached, translator, cache)
            translated_count += len(uncached)

            # Save cache periodically
            if translated_count % 500 == 0 or i + BATCH_SIZE >= total:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, ensure_ascii=False, indent=1)

            # Rate limiting
            time.sleep(RATE_LIMIT_DELAY)

        progress = min(i + BATCH_SIZE, total)
        if progress % 500 == 0 or progress == total:
            print(f"  Progress: {progress}/{total} ({progress*100//total}%)")

    # Final cache save
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)

    print(f"Translation complete. {translated_count} new translations, {len(cache)} total cached.")
    return cache

# =============================================================================
# FILE PROCESSING
# =============================================================================

def apply_translations(filepath, cache):
    """Apply translations to a file, preserving all code structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_count = len(lines)
    translated_lines = []

    for line in lines:
        translated_lines.append(translate_file_line(line, cache))

    assert len(translated_lines) == original_count, \
        f"Line count mismatch in {filepath}: {original_count} -> {len(translated_lines)}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)

    print(f"Applied translations to: {filepath} ({original_count} lines)")

def translate_file_line(line, cache):
    """Translate a single line using the cache."""
    stripped = line.strip()

    # Skip comments
    if stripped.startswith('//'):
        return line

    # Skip empty lines
    if not stripped:
        return line

    result = line

    # Process mes "..." patterns
    def replace_mes(m):
        prefix = m.group(1)
        content = m.group(2)
        if is_skip_string(content):
            return m.group(0)
        translated = cache.get(content, content)
        return f'{prefix}"{translated}"'

    result = re.sub(r'(mes\s+)"([^"]*)"', replace_mes, result)

    # Process select("...") patterns - handle : separated options
    def replace_select(m):
        prefix = m.group(1)
        content = m.group(2)
        if is_skip_string(content):
            return m.group(0)
        # Try full string first
        if content in cache:
            translated = cache[content]
            # Remove any colons that might have been introduced
            # Actually, select options USE colons as separators, keep them
            return f'{prefix}"{translated}"'
        # Otherwise translate each option
        options = content.split(':')
        translated_options = []
        for opt in options:
            opt_stripped = opt.strip()
            if opt_stripped in cache:
                t = cache[opt_stripped]
                # Remove colons from individual option translations
                t = t.replace(':', ' -')
                translated_options.append(t)
            else:
                translated_options.append(opt)
        return f'{prefix}"{":" .join(translated_options)}"'

    # Only process if line has select
    if 'select(' in result:
        result = re.sub(r'(select\(\s*)"([^"]*)"', replace_select, result)

    # Process mapannounce patterns
    def replace_announce(m):
        prefix = m.group(1)
        content = m.group(2)
        if is_skip_string(content):
            return m.group(0)
        translated = cache.get(content, content)
        return f'{prefix}"{translated}"'

    if 'mapannounce' in result:
        result = re.sub(r'(mapannounce\s+"[^"]+"\s*,\s*)"([^"]*)"', replace_announce, result)

    return result

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("rAthena Quest Translation: English -> LATAM Spanish")
    print("=" * 60)

    # Step 1: Extract all unique strings
    print("\nStep 1: Extracting translatable strings...")
    all_strings = extract_all_strings(FILES)
    print(f"  Found {len(all_strings)} unique translatable strings")

    # Step 2: Translate all strings
    print("\nStep 2: Translating strings...")
    cache = translate_all_strings(all_strings, CACHE_FILE)

    # Step 3: Apply translations to all files
    print("\nStep 3: Applying translations to files...")
    for filepath in FILES:
        apply_translations(filepath, cache)

    print("\n" + "=" * 60)
    print("Translation complete!")
    print("=" * 60)

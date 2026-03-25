#!/usr/bin/env python3
"""
Translate rAthena quest NPC dialogue from English to LATAM Spanish.
Rules:
- Only translate text inside mes "..."; and select("...")
- Never change script logic, variables, functions, coordinates, NPC sprite IDs
- Never change NPC names in brackets [Name]
- Preserve color codes ^RRGGBB exactly
- Preserve variable references exactly
- Use informal "tu" (LATAM Spanish)
- Keep proper nouns (place names, character names, item names)
- Do not introduce colons inside select() text
- Keep exact same line count per file
"""

import re
import sys
import os

# We'll process line by line. For each line we check if it's a mes or select line
# and translate the English text portions.

def translate_text(text):
    """Translate a single English text string to LATAM Spanish.
    This handles the text INSIDE quotes, preserving color codes and variables."""

    # If it's just dots/ellipsis or empty, keep as is
    if re.match(r'^[\.\s\-~!?*]+$', text):
        return text

    # If it's just a NPC name in brackets like [Nile], keep as is
    if re.match(r'^\[.*\]$', text):
        return text

    # Split text by color codes and variable references to preserve them
    # We need to translate the English parts while keeping codes intact

    # First, let's use a comprehensive translation approach
    result = do_translate(text)
    return result

def do_translate(text):
    """Main translation function using pattern matching."""

    # Preserve segments that should not be translated
    # Color codes: ^RRGGBB
    # Variables: strcharinfo(0), .@var$, etc.
    # Item names in game context

    # We'll use a large dictionary of translations
    # For efficiency, try exact match first, then pattern-based

    t = text

    # Check if entire string is a known translation
    if t in TRANSLATIONS:
        return TRANSLATIONS[t]

    # Try to find and apply partial translations
    # Handle color-coded segments
    # Pattern: ^RRGGBB...text...^000000
    # We need to translate inside color codes too

    # For complex strings with color codes, split and translate parts
    if '^' in t:
        return translate_with_color_codes(t)

    # For strings with concatenation (+ signs), they stay as-is in the file
    # The mes line itself handles concatenation

    # Default: return translation from dictionary or original
    return TRANSLATIONS.get(t, t)

def translate_with_color_codes(text):
    """Handle text with ^RRGGBB color codes."""
    # Split by color code pattern
    parts = re.split(r'(\^[0-9a-fA-F]{6})', text)
    result = []
    for part in parts:
        if re.match(r'^\^[0-9a-fA-F]{6}$', part):
            result.append(part)
        else:
            # Translate this text segment
            result.append(TRANSLATIONS.get(part, part))
    return ''.join(result)

def process_mes_line(line):
    """Process a mes "..." line, translating the text content."""
    # Match: mes "text";
    # But also: mes "text" + var + "text";
    # And: mes "[NPC Name]";  (don't translate these)

    stripped = line.lstrip()
    if not stripped.startswith('mes "'):
        # Could be: mes "[" + .@npc_name$ + "]";
        # Or other non-standard mes lines
        return line

    indent = line[:len(line) - len(stripped)]

    # Check for NPC name line: mes "[Something]";
    m = re.match(r'^mes "\[.*\]";$', stripped)
    if m:
        return line  # Don't translate NPC names

    # Check for simple mes "text";
    m = re.match(r'^mes "(.*?)";$', stripped)
    if m:
        text = m.group(1)
        translated = translate_text(text)
        return indent + 'mes "' + translated + '";'

    # Check for mes "text" + variable + "text";
    # These have concatenation - translate string parts only
    # Pattern: mes "text1" + expr + "text2" + expr + "text3";
    m = re.match(r'^mes (.+);$', stripped)
    if m:
        content = m.group(1)
        # Split by + and translate only quoted string parts
        parts = split_concat(content)
        translated_parts = []
        for part in parts:
            pt = part.strip()
            if pt.startswith('"') and pt.endswith('"'):
                inner = pt[1:-1]
                # Don't translate NPC name brackets
                if re.match(r'^\[.*\]$', inner) or re.match(r'^\[$', inner) or re.match(r'^\]$', inner):
                    translated_parts.append(part)
                else:
                    translated = translate_text(inner)
                    translated_parts.append(part[:len(part)-len(pt)] + '"' + translated + '"')
            else:
                translated_parts.append(part)
        return indent + 'mes ' + ' + '.join(translated_parts) + ';'

    return line

def split_concat(s):
    """Split a string by + while respecting quotes."""
    parts = []
    current = ''
    in_quote = False
    i = 0
    while i < len(s):
        c = s[i]
        if c == '"' and (i == 0 or s[i-1] != '\\'):
            in_quote = not in_quote
            current += c
        elif c == '+' and not in_quote:
            parts.append(current)
            current = ''
        else:
            current += c
        i += 1
    if current:
        parts.append(current)
    return parts

def process_select_line(line):
    """Process a select("opt1","opt2",...) line."""
    stripped = line.lstrip()
    indent = line[:len(line) - len(stripped)]

    # Find select( ... ) in the line
    # It could be: select("text")
    # Or: if (select("a","b") == 2)
    # Or: switch( select( "a", "b", "c" ) )
    # Or: .@s = select( "a", "b" ) - 1;

    # Find the select(...) portion
    m = re.search(r'select\s*\((.*?)\)', stripped)
    if not m:
        return line

    select_content = m.group(1)

    # Parse the options - they're comma-separated quoted strings, possibly with variables
    options = parse_select_options(select_content)
    translated_options = []
    for opt in options:
        opt_stripped = opt.strip()
        if opt_stripped.startswith('"') and opt_stripped.endswith('"'):
            inner = opt_stripped[1:-1]
            translated = translate_text(inner)
            # Preserve leading/trailing spaces in the option
            leading = opt[:len(opt) - len(opt.lstrip())]
            trailing_spaces = ''
            if opt.endswith(' '):
                trailing_spaces = ' '
            translated_options.append(leading + '"' + translated + '"' + trailing_spaces)
        else:
            translated_options.append(opt)  # Variable reference, keep as-is

    new_select_content = ','.join(translated_options)

    # Reconstruct the line
    start = stripped[:m.start(1)]
    end = stripped[m.end(1):]
    new_stripped = start + new_select_content + end

    return indent + new_stripped

def process_npctalk_line(line):
    """Process npctalk "text" lines."""
    stripped = line.lstrip()
    indent = line[:len(line) - len(stripped)]

    m = re.match(r'^npctalk "(.*?)"(.*);$', stripped)
    if m:
        text = m.group(1)
        rest = m.group(2)
        translated = translate_text(text)
        return indent + 'npctalk "' + translated + '"' + rest + ';'
    return line

def process_line(line):
    """Process a single line of the script."""
    stripped = line.lstrip()

    # Check if it's a mes line
    if stripped.startswith('mes "') or stripped.startswith('mes "['):
        # Check if it's just a NPC name
        if re.match(r'^mes "\[.*\]";$', stripped):
            return line
        return process_mes_line(line)

    # Check if it contains select(
    if 'select(' in stripped or 'select (' in stripped:
        return process_select_line(line)

    # Check if it's an npctalk line
    if stripped.startswith('npctalk "'):
        return process_npctalk_line(line)

    return line

def process_file(input_path, output_path=None):
    """Process an entire file."""
    if output_path is None:
        output_path = input_path

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_count = len(lines)
    translated_lines = []

    for line in lines:
        # Remove newline for processing, add back after
        line_stripped = line.rstrip('\n').rstrip('\r')
        translated = process_line(line_stripped)
        translated_lines.append(translated)

    # Verify line count
    assert len(translated_lines) == original_count, f"Line count mismatch: {len(translated_lines)} vs {original_count}"

    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        for i, tl in enumerate(translated_lines):
            if i < len(translated_lines) - 1:
                f.write(tl + '\n')
            else:
                # Last line - check if original had newline
                if lines[-1].endswith('\n'):
                    f.write(tl + '\n')
                else:
                    f.write(tl)

    print(f"Processed {input_path}: {original_count} lines")

# =============================================================================
# TRANSLATION DICTIONARY
# =============================================================================
# This maps English text to LATAM Spanish translations.
# NPC names in brackets are never translated.
# Color codes are preserved.
# Variable references are preserved.
# =============================================================================

TRANSLATIONS = {}

def build_translations():
    """Build the translation dictionary from all quest files."""
    global TRANSLATIONS
    # We'll populate this with all dialogue translations
    pass

if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print("Usage: python translate_quests.py file1.txt file2.txt ...")
        sys.exit(1)
    for f in files:
        process_file(f)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate rAthena quest NPC dialogue from English to LATAM Spanish.

Strategy: Extract all translatable strings, dump them to a JSON file for
manual translation reference, then apply translations from the JSON mapping.
"""

import re
import json
import os

def is_npc_name_line(text):
    """Check if text is just an NPC name in brackets like [Guard]"""
    t = text.strip()
    if re.match(r'^\[.*\]$', t):
        return True
    return False

def extract_strings_from_file(filepath):
    """Extract all translatable strings with their line numbers and context."""
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//'):
            continue

        # mes "..." patterns
        for m in re.finditer(r'(mes\s+)"([^"]*)"', line):
            s = m.group(2)
            if s and not is_npc_name_line(s):
                results.append({
                    'line': i + 1,
                    'type': 'mes',
                    'original': s,
                    'full_match': m.group(0),
                    'start': m.start(),
                    'end': m.end()
                })

        # select("...") patterns - need to handle multi-option
        for m in re.finditer(r'select\(\s*"([^"]*)"', line):
            s = m.group(1)
            if s:
                results.append({
                    'line': i + 1,
                    'type': 'select',
                    'original': s,
                    'full_match': m.group(0),
                    'start': m.start(),
                    'end': m.end()
                })

        # mapannounce
        for m in re.finditer(r'(mapannounce\s+"[^"]+"\s*,\s*)"([^"]*)"', line):
            s = m.group(2)
            if s:
                results.append({
                    'line': i + 1,
                    'type': 'mapannounce',
                    'original': s,
                    'full_match': m.group(0),
                    'start': m.start(),
                    'end': m.end()
                })

    return results

def dump_strings(filepath, output_json):
    """Dump all unique translatable strings to a JSON file."""
    results = extract_strings_from_file(filepath)
    unique_strings = {}
    for r in results:
        s = r['original']
        if s not in unique_strings:
            unique_strings[s] = s  # eng -> eng (placeholder)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(unique_strings, f, ensure_ascii=False, indent=2)

    print(f"Dumped {len(unique_strings)} unique strings from {filepath} to {output_json}")
    return unique_strings

if __name__ == '__main__':
    files = {
        'lighthalzen': r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_lighthalzen.txt',
        'nameless': r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_nameless.txt',
        'rachel': r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_rachel.txt',
        'veins': r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/quests_veins.txt',
    }

    all_strings = {}
    for name, filepath in files.items():
        results = extract_strings_from_file(filepath)
        for r in results:
            s = r['original']
            if s not in all_strings:
                all_strings[s] = s

    # Dump all unique strings
    output = r'D:/Xponzy Network/Ragnarok-Server/rathena/npc/quests/all_strings.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(all_strings, f, ensure_ascii=False, indent=2)
    print(f"Total unique strings across all files: {len(all_strings)}")

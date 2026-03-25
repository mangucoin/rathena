#!/usr/bin/env python3
import re
import sys
import os

def extract(filepath):
    with open(filepath, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    strings = []
    seen = set()

    for line in lines:
        stripped = line.strip()

        # mes "text";
        m = re.match(r'\s*mes\s+"(.*)"\s*;', stripped)
        if m:
            content = m.group(1)
            if re.match(r'^\[.*\]$', content):
                continue
            if '"+' in content or '+"' in content:
                continue
            # Skip purely punctuation/empty
            clean = re.sub(r'[.!?*\-_ ~\t^0-9A-Fa-f]', '', content)
            if not clean:
                continue
            if content not in seen:
                seen.add(content)
                strings.append(('MES', content))

        # select("opt1:opt2")
        m = re.search(r'select\("([^"]*)"\)', stripped)
        if m:
            opts = m.group(1).split(':')
            for o in opts:
                clean = re.sub(r'[.!?*\-_ ~\t]', '', o)
                if not clean:
                    continue
                if o not in seen:
                    seen.add(o)
                    strings.append(('SEL', o))

        # mapannounce text
        m = re.search(r'mapannounce\s+"[^"]*"\s*,\s*"([^"]*)"', stripped)
        if m:
            text = m.group(1)
            if text not in seen:
                seen.add(text)
                strings.append(('ANN', text))

    basename = os.path.basename(filepath).replace('.txt', '')
    outdir = os.path.dirname(filepath)
    outpath = os.path.join(outdir, f'{basename}_strings.txt')
    with open(outpath, 'w', encoding='utf-8') as f:
        for typ, s in strings:
            f.write(f'{s}\n')

    print(f"{basename}: {len(strings)} unique translatable strings -> {outpath}")
    return len(strings)

files = [
    "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_mora.txt",
    "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_dicastes.txt",
    "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_malaya.txt",
    "D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_malangdo.txt",
]

total = 0
for f in files:
    total += extract(f)
print(f"\nTotal unique strings needing translation: {total}")

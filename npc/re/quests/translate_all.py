#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys, os

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    original_count = len(lines)
    translated = [process_line(line) for line in lines]
    assert len(translated) == original_count
    with open(filepath, 'w', encoding='utf-8', newline=chr(10)) as f:
        f.writelines(translated)
    print(f'  Done: {os.path.basename(filepath)} ({original_count} lines)')

def process_line(line):
    stripped = line.strip()
    if not stripped or stripped.startswith('//'):
        return line
    result = line
    if re.search(r'\bmes\s+' + chr(34), stripped):
        result = translate_mes(line)
    if 'select(' in result:
        result = translate_select(result)
    if re.search(r'\bnpctalk\s+' + chr(34), result):
        result = translate_npctalk(result)
    if re.search(r'\bunittalk\s+', result):
        result = translate_unittalk(result)
    return result

def translate_mes(line):
    m = re.match(r'^(.*?\bmes\s+)(.*?)(;\s*(?://.*)?)' + chr(10) + '?$', line)
    if not m:
        return line
    prefix, expr, suffix = m.group(1), m.group(2), m.group(3)
    nl = chr(10) if line.endswith(chr(10)) else ''
    new_expr = translate_quoted_strings(expr)
    return prefix + new_expr + suffix + nl

def translate_select(line):
    def repl_select(m):
        full = m.group(0)
        def repl_q(m2):
            content = m2.group(1)
            if ':' in content:
                parts = content.split(':')
                tp = [tr(p) if p else p for p in parts]
                return chr(34) + ':'.join(tp) + chr(34)
            return chr(34) + tr(content) + chr(34)
        return re.sub(chr(34) + '([^' + chr(34) + ']*)' + chr(34), repl_q, full)
    return re.sub(r'select\s*\([^)]*\)', repl_select, line)

def translate_npctalk(line):
    m = re.search(r'(\bnpctalk\s+' + chr(34) + ')([^' + chr(34) + ']*)(' + chr(34) + ')', line)
    if not m:
        return line
    content = m.group(2)
    cm = re.match(r'^([^:]+):\s*(.+)$', content)
    if cm:
        translated = cm.group(1) + ': ' + tr(cm.group(2))
    else:
        translated = tr(content)
    return line[:m.start(2)] + translated + line[m.end(2):]

def translate_unittalk(line):
    def repl_q(m):
        content = m.group(1)
        if not content.strip():
            return chr(34) + content + chr(34)
        cm = re.match(r'^(.*?\s*:\s*)(.+)$', content)
        if cm and cm.group(2).strip():
            return chr(34) + cm.group(1) + tr(cm.group(2)) + chr(34)
        return chr(34) + tr(content) + chr(34)
    return re.sub(chr(34) + '([^' + chr(34) + ']*)' + chr(34), repl_q, line)

def translate_quoted_strings(expr):
    def repl(m):
        content = m.group(1)
        if re.match(r'^\[.*\]$', content.strip()):
            return chr(34) + content + chr(34)
        if not content.strip():
            return chr(34) + content + chr(34)
        return chr(34) + tr(content) + chr(34)
    return re.sub(chr(34) + '([^' + chr(34) + ']*)' + chr(34), repl, expr)

def tr(text):
    if not text or not text.strip():
        return text
    t = text.strip()
    if all(c in '.!?*~-() \t' for c in t):
        return text
    color_parts = re.split(r'(\^[0-9a-fA-F]{6})', text)
    if len(color_parts) > 1:
        result_parts = []
        for part in color_parts:
            if re.match(r'^\^[0-9a-fA-F]{6}$', part):
                result_parts.append(part)
            else:
                result_parts.append(translate_plain(part))
        return ''.join(result_parts)
    return translate_plain(text)

def translate_plain(text):
    if not text or not text.strip():
        return text
    t = text.strip()
    if t in TR:
        ws_before = text[:len(text) - len(text.lstrip())]
        ws_after = text[len(text.rstrip()):]
        return ws_before + TR[t] + ws_after
    return text

TR = {}

def load_translations():
    global TR
    mapfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translation_map.txt')
    if not os.path.exists(mapfile):
        print(f'ERROR: {mapfile} not found!')
        sys.exit(1)
    with open(mapfile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip(chr(10)).rstrip(chr(13))
            if not line or line.startswith('#'):
                continue
            if '|||' in line:
                en, es = line.split('|||', 1)
                TR[en] = es
    print(f'  Loaded {len(TR)} translations')

if __name__ == '__main__':
    print('Loading translations...')
    load_translations()
    files = [
        'D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_15_1.txt',
        'D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_16_1.txt',
        'D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_16_2.txt',
        'D:/Xponzy Network/Ragnarok-Server/rathena/npc/re/quests/quests_eclage.txt',
    ]
    for f in files:
        print(f'Processing {os.path.basename(f)}...')
        translate_file(f)
    print('All files translated!')

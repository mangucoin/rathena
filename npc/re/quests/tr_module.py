#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys, os

def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    translated = [process_line(line) for line in lines]
    assert len(translated) == len(lines)
    with open(input_path, 'w', encoding='utf-8', newline='
') as f:
        f.writelines(translated)
    print(f'Done: {os.path.basename(input_path)} ({len(lines)} lines)')

def process_line(line):
    s = line.strip()
    if s.startswith('//') or not s:
        return line
    if s.startswith('mes ') and '"' in s:
        return translate_mes(line)
    if 'select(' in s:
        return translate_select(line)
    if 'npctalk ' in s:
        return translate_npctalk(line)
    if 'unittalk ' in s:
        return translate_unittalk(line)
    return line

def translate_mes(line):
    m = re.match(r'^(\s*mes\s+)(.+)(;.*)$', line.rstrip('
'))
    if not m:
        return line
    prefix, expr, suffix = m.group(1), m.group(2), m.group(3)
    newline_end = '
' if line.endswith('
') else ''
    new_expr = re.sub(r'"([^"]*)"', lambda mm: '"' + tr_content(mm.group(1)) + '"', expr)
    return prefix + new_expr + suffix + newline_end

def translate_select(line):
    def repl_select(m):
        full = m.group(0)
        def repl_q(m2):
            c = m2.group(1)
            if ':' in c:
                parts = c.split(':')
                tp = [tr_content(p) if p else p for p in parts]
                return '"' + ':'.join(tp) + '"'
            return '"' + tr_content(c) + '"'
        return re.sub(r'"([^"]*)"', repl_q, full)
    return re.sub(r'select\s*\([^)]*\)', repl_select, line)

def translate_npctalk(line):
    m = re.search(r'(npctalk\s+")([^"]*)(".*)', line)
    if not m:
        return line
    pre = line[:m.start()] + m.group(1)
    content = m.group(2)
    post = m.group(3)
    cm = re.match(r'^([^:]+):\s*(.+)$', content)
    if cm:
        translated = cm.group(1) + ': ' + tr_dialogue(cm.group(2))
    else:
        translated = tr_dialogue(content)
    return pre + translated + post

def translate_unittalk(line):
    def repl(m):
        c = m.group(1)
        if not c.strip():
            return '"' + c + '"'
        cm = re.match(r'^(.*?\s*:\s*)(.+)$', c)
        if cm:
            return '"' + cm.group(1) + tr_dialogue(cm.group(2)) + '"'
        return '"' + tr_dialogue(c) + '"'
    return re.sub(r'"([^"]*)"', repl, line)

def tr_content(text):
    if not text:
        return text
    if re.match(r'^\[.*\]$', text.strip()):
        return text
    return tr_dialogue(text)

def tr_dialogue(text):
    if not text or not text.strip():
        return text
    if all(c in '.!?*~- ()' for c in text.strip()):
        return text
    colors = []
    def save_cc(m):
        colors.append(m.group(0))
        return chr(167) + 'C' + str(len(colors)-1) + chr(167)
    processed = re.sub(r'\^[0-9a-fA-F]{6}', save_cc, text)
    translated = do_tr(processed)
    for i, cc in enumerate(colors):
        translated = translated.replace(chr(167) + 'C' + str(i) + chr(167), cc)
    return translated

print('Translation module loaded')

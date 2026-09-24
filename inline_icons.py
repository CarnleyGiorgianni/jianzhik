#!/usr/bin/env python3
"""Convert <img src="images/icons/X.svg"> references to inline SVG."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(ROOT, 'images', 'icons')

# read all svg files into a dict
svgs = {}
for name in os.listdir(ICONS_DIR):
    if name.endswith('.svg'):
        path = os.path.join(ICONS_DIR, name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # extract inner content (everything between <svg ...> and </svg>)
        m = re.search(r'<svg[^>]*>(.*)</svg>', content, re.DOTALL)
        if m:
            inner = m.group(1)
            # remove aria-label from inner if any (we'll add aria-hidden)
            svgs[name] = inner.strip()

# process HTML files
files = ['index.html', 'services.html', 'advantages.html', 'news.html', 'contact.html']
total = 0
for fname in files:
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    # match <img src="images/icons/xxx.svg" width="N" height="M" alt="...">
    pattern = re.compile(r'<img\s+src="images/icons/([a-z0-9_-]+\.svg)"\s+width="(\d+)"\s+height="(\d+)"\s*alt="[^"]*"\s*>')
    def replace(m):
        filename = m.group(1)
        w = m.group(2); h = m.group(3)
        if filename not in svgs:
            return m.group(0)
        inner = svgs[filename]
        # force currentColor for stroke if present, otherwise keep
        return f'<svg width="{w}" height="{h}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    html = pattern.sub(replace, html)
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        n = len(pattern.findall(original))
        total += n
        print(f"[ok] {fname}: replaced {n} icon references")
    else:
        print(f"[-] {fname}: no changes")
print(f"Total replacements: {total}")
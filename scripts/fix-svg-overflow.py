#!/usr/bin/env python3
"""
Fix My Buddy AAC symbol overflow on iOS Safari.

Cause: 3,100+ Mulberry SVGs declare overflow="visible" on the root <svg>.
When such an SVG is loaded via <img>, iOS/WebKit paints content outside the
element box; the tile's object-fit:contain + overflow:hidden then show only a
zoomed strip. Removing the spurious overflow="visible" lets the UA clip to the
viewBox so object-fit:contain fits the whole symbol.

This rewrites SVGs in-place: removes overflow="visible" on the root element and
guarantees preserveAspectRatio="xMidYMid meet". Idempotent.

Usage: python3 fix-svg-overflow.py public/symbols
"""
import re, sys, pathlib

OVERFLOW = re.compile(r'\s+overflow\s*=\s*"(?:visible)"', re.I)

def fix_file(p: pathlib.Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    # locate the opening <svg ...> tag
    m = re.search(r'<svg\b[^>]*>', txt, re.I)
    if not m:
        return False
    tag = m.group(0)
    new = OVERFLOW.sub('', tag)                       # drop overflow="visible"
    if 'preserveAspectRatio' not in new:             # make fit explicit
        new = new[:-1] + ' preserveAspectRatio="xMidYMid meet">'
    if new == tag:
        return False
    p.write_text(txt[:m.start()] + new + txt[m.end():], encoding='utf-8')
    return True

def main(root):
    root = pathlib.Path(root)
    changed = 0; total = 0
    for p in root.rglob('*.svg'):
        total += 1
        if fix_file(p):
            changed += 1
    print(f"Scanned {total} SVGs, fixed {changed}")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'public/symbols')

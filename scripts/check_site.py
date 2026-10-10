#!/usr/bin/env python3
"""Check static pages, local links and assets without external dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob('*.html'))
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        for key in ('href','src'):
            if a.get(key): self.links.append(a[key])

parsed={}
for page in PAGES:
    p=Links(); p.feed(page.read_text(encoding='utf-8')); parsed[page.resolve()]=p
errors=[]
for page, data in parsed.items():
    for link in data.links:
        uri=urlsplit(link)
        if uri.scheme or uri.netloc or link.startswith('//') or link.startswith('mailto:') or link.startswith('tel:'):
            continue
        path=unquote(uri.path)
        target=(page.parent / path).resolve() if path else page
        if target.is_dir(): target=target/'index.html'
        if not target.is_file():
            errors.append(f'{page.relative_to(ROOT)}: missing {link}')
        elif uri.fragment and target in parsed and uri.fragment not in parsed[target].ids:
            errors.append(f'{page.relative_to(ROOT)}: missing fragment {link}')
print(f'Checked {len(PAGES)} HTML files; {len(errors)} errors')
for error in errors: print(error, file=sys.stderr)
sys.exit(bool(errors))

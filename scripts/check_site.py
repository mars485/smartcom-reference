#!/usr/bin/env python3
"""Validate local references, metadata, and accessibility landmarks."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://mars485.github.io/smartcom-reference/'
PAGES = sorted(ROOT.rglob('*.html'))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = []
        self.tags = Counter()
        self.meta = {}
        self.lang = None
        self.canonical = None
        self.skip = False
        self.title = False
        self._in_title = False
        self.errors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] += 1
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'title': self._in_title = True
        if tag == 'meta': self.meta[a.get('name') or a.get('property')] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if tag == 'a' and a.get('class') == 'skip-link' and a.get('href') == '#main': self.skip = True
        if a.get('id'): self.ids.append(a['id'])
        for key in ('href', 'src'):
            if a.get(key): self.links.append(a[key])
        if tag == 'img' and 'alt' not in a: self.errors.append('image missing alt')

    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False

    def handle_data(self, data):
        if self._in_title and data.strip(): self.title = True


parsed = {}
errors = []
for page in PAGES:
    data = Page()
    data.feed(page.read_text(encoding='utf-8'))
    parsed[page.resolve()] = data
    name = page.relative_to(ROOT).as_posix()
    errors.extend(f'{name}: {error}' for error in data.errors)
    if data.lang != 'ru': errors.append(f'{name}: missing Russian language')
    if not data.title: errors.append(f'{name}: missing title')
    if data.tags['h1'] != 1: errors.append(f'{name}: expected one h1')
    for ident, count in Counter(data.ids).items():
        if count > 1: errors.append(f'{name}: duplicate id {ident}')
    if name != '404.html':
        expected = BASE if name == 'index.html' else BASE + name
        if data.canonical != expected: errors.append(f'{name}: wrong canonical URL')
        if not data.meta.get('description'): errors.append(f'{name}: missing description')
        if data.meta.get('og:url') != expected: errors.append(f'{name}: wrong Open Graph URL')
        if not data.skip or 'main' not in data.ids: errors.append(f'{name}: missing skip link or main target')
        if data.tags['nav'] != 1: errors.append(f'{name}: expected one navigation landmark')
        if data.tags['main'] != 1: errors.append(f'{name}: expected one main landmark')

for page, data in parsed.items():
    for link in data.links:
        uri = urlsplit(link)
        if uri.scheme or uri.netloc or link.startswith('//'): continue
        path = unquote(uri.path)
        target = (page.parent / path).resolve() if path else page
        if not target.is_relative_to(ROOT):
            errors.append(f'{page.relative_to(ROOT)}: link escapes site {link}')
            continue
        if target.is_dir(): target = target / 'index.html'
        if not target.is_file(): errors.append(f'{page.relative_to(ROOT)}: missing {link}')
        elif uri.fragment and target in parsed and uri.fragment not in parsed[target].ids:
            errors.append(f'{page.relative_to(ROOT)}: missing fragment {link}')

if 'данные не отправлены' not in (ROOT / 'assets/js/main.js').read_text(encoding='utf-8'):
    errors.append('demo form must explicitly state that data were not sent')
urls = {node.text for node in ET.parse(ROOT / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
expected_urls = {BASE if page.name == 'index.html' else BASE + page.relative_to(ROOT).as_posix()
                 for page in PAGES if page.name != '404.html'}
if urls != expected_urls: errors.append('sitemap.xml: URLs do not match public pages')

print(f'Checked {len(PAGES)} HTML files; {len(errors)} errors')
for error in errors: print(error, file=sys.stderr)
sys.exit(bool(errors))

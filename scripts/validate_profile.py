#!/usr/bin/env python3
"""Check README links, self-contained SVGs, and real contribution totals."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = '{http://www.w3.org/2000/svg}'


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))
        assert tag not in ('script','iframe','style','canvas','video'), f'Unsupported README element: {tag}'


def main():
    for path in [ROOT/'README.md', ROOT/'PROJECT_SHOWCASE.md']:
        source = path.read_text()
        parser = Images();parser.feed(source)
        for img in parser.images:
            assert 'alt' in img, f'Missing image alternative text in {path.name}'
            src = img['src'].split('#')[0].split('?')[0]
            if not src.startswith(('http:', 'https:')):
                assert (path.parent/src).is_file(), f'Missing image: {src}'
        for link in re.findall(r'\]\((\./[^)]+)\)', source):
            assert (path.parent/link.split('#')[0]).is_file(), f'Missing document: {link}'
    for path in (ROOT/'assets').glob('*.svg'):
        root=ET.fromstring(path.read_text())
        assert root.tag == SVG+'svg' and 'viewBox' in root.attrib
        assert root.find(SVG+'title') is not None and root.find(SVG+'desc') is not None
        for node in root.iter():
            tag=node.tag.split('}')[-1]
            assert tag not in ('script','foreignObject','image'), f'Non-self-contained SVG: {path.name}'
            assert not any(k.lower().startswith('on') for k in node.attrib), 'SVG event handler'
            for key,value in node.attrib.items():
                if key.endswith('href'):
                    assert value.startswith('#'), 'External SVG resource'
        assert 'prefers-reduced-motion' in path.read_text(), f'Missing reduced motion support: {path.name}'
    snapshot=json.loads((ROOT/'assets/contribution-snapshot.json').read_text())
    assert snapshot['username']=='Dinesh-757'
    days=snapshot['days'];total=sum(d['count'] for d in days)
    assert 365 <= len(days) <= 378 and len({d['date'] for d in days}) == len(days)
    current=(ROOT/'assets/contribution-current.svg').read_text()
    for d in days:
        assert f'{d["date"]}: {d["count"]} contributions' in current
    assert f'{total:,}' in current
    print(f'Validated README assets, SVG compatibility, and {len(days)} contribution days ({total} contributions).')


if __name__=='__main__':
    main()

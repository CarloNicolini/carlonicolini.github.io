"""Check generated navigation and local resource references without network access."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
site = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / '_site'
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.links.append(value)
errors = []
for page in site.rglob('*.html'):
    parser = Links(); parser.feed(page.read_text(errors='replace'))
    for link in parser.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = site / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else page.parent / unquote(parsed.path)
        if not target.exists() and not target.with_suffix('.html').exists():
            errors.append((str(page.relative_to(site)), link))
unique = sorted(set(errors))
for page, link in unique:
    print(f'{page}: missing {link}')
print(f'Checked {len(list(site.rglob("*.html")))} HTML pages; {len(unique)} missing local references.')
sys.exit(bool(unique))

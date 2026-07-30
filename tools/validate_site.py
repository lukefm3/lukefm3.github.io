from html.parser import HTMLParser
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a", "link", "script", "iframe"}:
            key = "href" if tag in {"a", "link"} else "src"
            if attrs.get(key):
                self.links.append(attrs[key])

errors = []
for page in DOCS.glob("*.html"):
    parser = LinkParser()
    parser.feed(page.read_text(encoding="utf-8"))
    for link in parser.links:
        if link.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        target = (page.parent / link.split("#", 1)[0].split("?", 1)[0]).resolve()
        if not target.exists():
            errors.append(f"{page.name}: missing {link}")

metadata = json.loads((DOCS / "data" / "metadata.json").read_text(encoding="utf-8"))
if metadata.get("record_count", 0) < 1:
    errors.append("metadata.json reports no records")

csv_lines = (DOCS / "data" / "earthquakes.csv").read_text(encoding="utf-8").splitlines()
if len(csv_lines) < 2:
    errors.append("earthquakes.csv has no data rows")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"Validated {len(list(DOCS.glob('*.html')))} pages, local links, downloads, and {len(csv_lines)-1} data rows.")

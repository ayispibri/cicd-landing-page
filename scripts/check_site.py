from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class DocumentCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.has_title = False
        self.has_main = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "title":
            self._in_title = True
        if tag == "main":
            self.has_main = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.has_title = True

html_file = ROOT / "index.html"
css_file = ROOT / "style.css"
js_file = ROOT / "script.js"
for file in (html_file, css_file, js_file):
    if not file.is_file():
        raise SystemExit(f"GAGAL: file tidak ditemukan: {file.name}")

parser = DocumentCheck()
parser.feed(html_file.read_text(encoding="utf-8-sig"))
if not parser.has_title:
    raise SystemExit("GAGAL: elemen <title> belum ada atau kosong")
if not parser.has_main:
    raise SystemExit("GAGAL: elemen <main> belum ada")
for required_id in ("beranda", "tentang", "program", "kontak"):
    if required_id not in parser.ids:
        raise SystemExit(f"GAGAL: bagian #{required_id} belum ada")
print("LULUS: file utama, judul, konten, dan bagian landing page tersedia.")

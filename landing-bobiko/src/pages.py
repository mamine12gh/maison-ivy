"""Trouve la page de chaque ancre (id="...") : on cherche le texte du titre qui suit l'ancre dans le PDF."""
import sys, re, json, html as H
from pypdf import PdfReader
pdf, src = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
texts = [re.sub(r'\s+', ' ', p.extract_text() or '') for p in PdfReader(pdf).pages]
out = {}
for m in re.finditer(r'id="([^"]+)"[^>]*>(.*?)</h[123]>', s, re.S):
    aid, inner = m.group(1), m.group(2)
    t = H.unescape(re.sub(r'<[^>]+>', ' ', inner)); t = re.sub(r'\s+', ' ', t).strip()
    key = t[:28]
    for i, pt in enumerate(texts):
        if i < 2: continue
        if key and key in pt:
            out[aid] = i + 1; break
mk = {}
for i, pt in enumerate(texts):
    for m in re.finditer(r'§([^§]+)§', pt):
        mk.setdefault(m.group(1), i + 1)
out.update(mk)
print(json.dumps(out))

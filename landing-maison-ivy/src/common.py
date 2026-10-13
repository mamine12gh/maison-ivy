# -*- coding: utf-8 -*-
"""Gabarit commun aux deux PDF (HTML imprimé par Chromium)."""
import html, os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CSS = open(os.path.join(HERE, "fonts-abs.css"), encoding="utf-8").read()

def e(s):
    return html.escape(s, quote=False)

CSS = FONT_CSS + r"""
:root{--coral:#FF5A36;--cta:#E8431F;--yellow:#FFC83D;--ink:#1E1B2E;--cream:#FFF6EC;--cream2:#FBEAD6;--sky:#2F5BEA;--green:#1E8A5E;--muted:#5F5870;--line:#EADFD2}
@page{size:A4;margin:18mm 16mm 18mm 16mm;
  @bottom-left{content:"Maison Ivy · " string(doctitle);font-family:Nunito,sans-serif;font-size:8pt;color:#8B8398}
  @bottom-right{content:counter(page) " / " counter(pages);font-family:Nunito,sans-serif;font-size:8pt;color:#8B8398}}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:Nunito,system-ui,sans-serif;font-size:10pt;line-height:1.5;color:var(--ink)}
.doctitle{string-set:doctitle content();display:none}
h1,h2,h3,h4{font-family:Fredoka,Nunito,sans-serif;line-height:1.15;margin:0;break-after:avoid}
h1{font-size:24pt;font-weight:700;margin:0 0 4mm}
h2{font-size:15pt;font-weight:700;margin:7mm 0 2.5mm}
h3{font-size:11.5pt;font-weight:600;margin:5mm 0 2mm}
h4{font-size:10pt;font-weight:600;margin:3mm 0 1mm}
p{margin:0 0 2.4mm}
ul,ol{margin:0 0 2.6mm;padding-left:5mm}
li{margin-bottom:1mm}
a{color:var(--sky);text-decoration:none}
.chapter{break-before:page}
.kicker{font-family:Nunito;font-weight:900;font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--cta);margin-bottom:1.5mm}
.lead{font-size:11pt;color:#3A3550}
.muted{color:var(--muted)}
.small{font-size:8.5pt}
.hand{font-family:Caveat,cursive;font-weight:700}
/* tables */
table{width:100%;border-collapse:collapse;margin:2mm 0 4mm;font-size:8.8pt;break-inside:auto}
th,td{padding:1.8mm 2.2mm;vertical-align:top;text-align:left;border-bottom:.3mm solid var(--line)}
thead th{background:var(--ink);color:#fff;font-weight:800;font-size:8.4pt}
tbody tr:nth-child(even) td{background:#FDF9F4}
tr{break-inside:avoid}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
/* callouts */
.box{border-radius:3mm;padding:3.5mm 4.5mm;margin:3mm 0 4mm;break-inside:avoid}
.box.cream{background:var(--cream)}
.box.yellow{background:#FFF3C9}
.box.ink{background:var(--ink);color:var(--cream)}
.box.ink b{color:var(--yellow)}
.box.blue{background:#E9EEFF;color:#1B2A6B}
.box h4{margin-top:0}
.box p:last-child,.box ul:last-child{margin-bottom:0}
.decision{display:grid;grid-template-columns:22mm 1fr;gap:3mm;align-items:start;background:var(--ink);color:#fff;border-radius:3mm;padding:3.5mm 4.5mm;margin:3mm 0 3mm;break-inside:avoid}
.decision .lab{font-family:Fredoka;font-weight:700;color:var(--yellow);font-size:10pt}
.test{font-size:8.8pt;background:#E9EEFF;color:#1B2A6B;border-radius:2mm;padding:2mm 3mm;margin:0 0 3mm;break-inside:avoid}
.pill{display:inline-block;border-radius:99px;padding:.3mm 2.4mm;font-size:7.8pt;font-weight:800;background:var(--cream);margin-right:1mm}
.pill.c{background:var(--coral);color:#fff}
.pill.y{background:var(--yellow)}
.pill.i{background:var(--ink);color:#fff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
figure{margin:3mm 0 5mm;break-inside:avoid}
figcaption{font-size:8.2pt;color:var(--muted);margin-top:1.5mm}
figcaption b{color:var(--ink)}
img.shot{width:100%;border-radius:3mm;border:.3mm solid var(--line);display:block}
/* cover */
.cover{page:cover;height:297mm;width:210mm;position:relative;overflow:hidden;background:var(--cream);padding:34mm 20mm 0}
.cover .band{position:absolute;top:0;left:0;right:0;height:7mm;background:var(--coral)}
.cover h1{font-size:34pt;line-height:1.05;max-width:160mm}
.cover .sub{font-family:Fredoka;font-size:15pt;color:var(--muted);font-weight:500;margin-top:2mm}
.cover .meta{position:absolute;left:20mm;bottom:22mm;font-size:9pt;color:var(--muted);max-width:110mm}
.cover .logo{margin-bottom:22mm}
.cover .art{position:absolute;right:-18mm;bottom:-10mm;width:120mm}
/* toc */
.toc{width:100%;font-size:10pt}
.toc td{border-bottom:.3mm dotted #D8CCBE;padding:1.15mm 1mm}
.toc td:last-child{text-align:right;width:14mm;color:var(--muted)}
.mk{font-size:1px;color:#fff;position:absolute}
.toc tr.part td{text-align:left!important;font-family:Fredoka;font-weight:600;font-size:11pt;padding-top:3.5mm;border-bottom:0}
.toc a{color:var(--ink)}
.toc a::after{content:target-counter(attr(href), page)}
.toc td.pg{text-align:right}
"""

LOGO_O = '''<svg viewBox="0 0 40 40" aria-hidden="true"><defs><mask id="lm{n}"><rect x="-5" y="-5" width="50" height="50" fill="#fff"/><path d="M15 1 L38 24 L50 24 L50 -10 L15 -10 Z" fill="#000"/></mask></defs><g mask="url(#lm{n})" fill="#FF5A36"><circle cx="20" cy="19" r="16"/><path d="M8.5 27 L4 38.5 L17.5 33.5 Z"/></g><path d="M17.24 3.24 Q16.88 22.12 35.76 21.76 Z" fill="#FFE1D6" stroke="#E8431F" stroke-width="1.2" stroke-linejoin="round"/></svg>'''
_n = [0]
def logo_o():
    _n[0] += 1
    return LOGO_O.replace("{n}", str(_n[0]))

def logo(size="30pt", color="#1E1B2E"):
    return (f'<span style="font-family:Fredoka;font-weight:700;font-size:{size};color:{color};letter-spacing:-.02em;white-space:pre;line-height:1">maison '
            f'<span style="position:relative;display:inline-block">\u0131<span style="position:absolute;width:.42em;height:.42em;left:50%;top:-.38em;transform:translateX(-42%)">{logo_o()}</span></span>vy</span>')

COVER_ART = '''<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"><circle cx="170" cy="160" r="130" fill="#FFC83D"/><circle cx="250" cy="250" r="55" fill="#FF5A36"/>
<g transform="rotate(-8 140 120)"><rect x="95" y="40" width="90" height="105" rx="4" fill="#fff" stroke="#E1D6C8" stroke-width="2"/>
<g fill="none" stroke="#1E1B2E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(100 48) scale(.8)"><circle cx="50" cy="44" r="30"/><circle cx="50" cy="48" r="15" fill="#fff"/><path d="M38 41 L36 29 L45 36 M62 41 L64 29 L55 36"/><path d="M48 53 Q50 55.5 52 53"/><path d="M36 52 L27 50 M36 55.5 L27 57.5 M64 52 L73 50 M64 55.5 L73 57.5"/><path d="M50 14 L50 7"/><path d="M33 73 Q50 67 67 73 L69 93 L31 93 Z" fill="#fff"/></g></g>
<rect x="80" y="140" width="130" height="120" rx="34" fill="#fff" stroke="#1E1B2E" stroke-width="4"/><rect x="100" y="136" width="90" height="10" rx="5" fill="#1E1B2E"/><circle cx="145" cy="205" r="24" fill="#FF5A36" stroke="#1E1B2E" stroke-width="4"/></svg>'''

def page(title, body):
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{e(title)}</title><style>{CSS}</style></head><body><span class="doctitle">{e(title)}</span>{body}</body></html>'

def cover(kicker, title, sub, meta):
    return f'''<section class="cover"><div class="band"></div><div class="logo">{logo("30pt")}</div>
<p class="kicker">{e(kicker)}</p><h1>{title}</h1><p class="sub">{sub}</p>
<div class="art">{COVER_ART}</div><div class="meta">{meta}</div></section>'''

def table(head, rows, cls="", widths=None, num_cols=()):
    cg = "".join(f'<col style="width:{w}">' for w in widths) if widths else ""
    th = "".join(f'<th class="{"num" if i in num_cols else ""}">{h}</th>' for i, h in enumerate(head))
    trs = "".join("<tr>" + "".join(f'<td class="{"num" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<table class="{cls}"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def hbars(items, maxv=100, w=170, unit="", highlight=None, color="#E8431F", label_w=46):
    """items: [(label, value)] -> SVG en mm (largeur w)."""
    rowh = 7
    h = rowh * len(items) + 2
    bar_w = w - label_w - 14
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm" xmlns="http://www.w3.org/2000/svg" font-family="Nunito" font-size="3.2">']
    for i, (lab, v) in enumerate(items):
        y = 1 + i * rowh
        c = color if (highlight is None or i == highlight) else "#CFC6D8"
        out.append(f'<text x="0" y="{y+4.4}" fill="#1E1B2E" font-weight="700">{e(lab)}</text>')
        out.append(f'<rect x="{label_w}" y="{y+0.8}" width="{bar_w}" height="4.6" rx="2.3" fill="#F3ECE3"/>')
        out.append(f'<rect x="{label_w}" y="{y+0.8}" width="{bar_w*v/maxv:.2f}" height="4.6" rx="2.3" fill="{c}"/>')
        out.append(f'<text x="{label_w+bar_w+2}" y="{y+4.4}" fill="#1E1B2E" font-weight="800">{v}{unit}</text>')
    out.append("</svg>")
    return "".join(out)

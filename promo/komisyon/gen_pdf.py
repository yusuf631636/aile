"""getirtrend Pazaryeri komisyon oranları PDF'i.
Kaynak tablo kategori listesi; her orana -3 puan uygulanır (en düşük %0)."""
import json, html
from collections import OrderedDict
INDIR = 3.0
rows = json.load(open('kaynak-satirlar.json', encoding='utf-8'))
fmt = lambda v: ('%' + f'{v:.2f}').replace('.', ',')
groups = OrderedDict()
for cat, std, ozel in rows:
    cat = cat.replace('Esnaf Çiçek', 'Çiçek').strip()
    genel = cat.endswith('(Ana Sayfa)')
    cat = cat.replace(' (Ana Sayfa)', '')
    parts = [p.strip() for p in cat.split('/')]
    top = parts[0]
    groups.setdefault(top, [])
    sub = ' › '.join(parts[1:]) if len(parts) > 1 else ('Tüm alt kategoriler (genel oran)' if genel else 'Ana kategori')
    groups[top].append((sub, len(parts) - 1, max(0.0, std - INDIR), max(0.0, ozel - INDIR), std, ozel))
summary = []
for top, rs in groups.items():
    s = [r[2] for r in rs]; o = [r[3] for r in rs]
    rng = lambda a: fmt(min(a)) if min(a) == max(a) else f'{fmt(min(a))} – {fmt(max(a))}'
    summary.append(f'<tr><td><b>{html.escape(top)}</b></td><td>{len(rs)}</td><td>{rng(s)}</td><td>{rng(o)}</td></tr>')
body = []
for top, rs in groups.items():
    body.append(f'<h2>{html.escape(top)}</h2><table class="t"><thead><tr><th>Kategori</th><th>Standart</th><th>Özel grup*</th></tr></thead><tbody>')
    for sub, d, s, o, _, _ in rs:
        body.append(f'<tr class="d{min(d,4)}"><td>{html.escape(sub)}</td><td class="r">{fmt(s)}</td><td class="r">{fmt(o)}</td></tr>')
    body.append('</tbody></table>')
logo = open('../assets/logo-mark.svg').read()
doc = f'''<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><title>getirtrend Pazaryeri Komisyon Oranları 2026</title>
<link rel="stylesheet" href="../assets/fonts.css">
<style>
 @page {{ size: A4; margin: 18mm 14mm 18mm 14mm; }}
 body {{ font-family: 'Plus Jakarta Sans', sans-serif; color: #221D19; font-size: 9pt; }}
 .cover {{ page-break-after: always; }}
 .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 26pt; letter-spacing: -1px; }}
 .brand svg {{ width: 44px; height: 44px; }} .brand b {{ color: #D7351F; }}
 h1 {{ font-size: 24pt; letter-spacing: -1px; margin: 26px 0 4px; }}
 .sub {{ font-size: 11pt; color: #6b625a; margin-bottom: 22px; }}
 .box {{ background: #FCEFED; border-left: 5px solid #D7351F; padding: 12px 16px; border-radius: 6px; margin: 14px 0; font-size: 10pt; line-height: 1.5; }}
 table {{ width: 100%; border-collapse: collapse; }}
 .s th, .s td {{ padding: 7px 8px; border-bottom: 1px solid #e7e1d8; text-align: left; font-size: 10pt; }}
 .s th {{ background: #221D19; color: #fff; }}
 h2 {{ font-size: 14pt; margin: 18px 0 6px; padding: 6px 10px; background: #D7351F; color: #fff; border-radius: 6px; page-break-after: avoid; }}
 .t th {{ background: #F5F1EB; text-align: left; padding: 5px 6px; font-size: 8.5pt; border-bottom: 2px solid #221D19; }}
 .t th:nth-child(n+2), .t td.r {{ text-align: right; width: 18mm; white-space: nowrap; }}
 .t td {{ padding: 3.2px 6px; border-bottom: 1px solid #eee7de; vertical-align: top; }}
 .t tr {{ page-break-inside: avoid; }}
 .t thead {{ display: table-header-group; }}
 tr.d1 td:first-child {{ font-weight: 700; }}
 tr.d0 td:first-child {{ font-weight: 800; }}
 tr:nth-child(even) td {{ background: #fbf9f6; }}
 .fn {{ font-size: 8.5pt; color: #6b625a; margin-top: 10px; line-height: 1.5; }}
</style></head><body>
<div class="cover">
  <div class="brand">{logo}<span>getir<b>trend</b></span></div>
  <h1>Pazaryeri Komisyon Oranları</h1>
  <div class="sub">2026 · Kategori bazlı satıcı komisyon listesi</div>
  <div class="box">Komisyon yalnızca <b>satış gerçekleştiğinde</b> uygulanır. Başvuru ve aylık mağaza ücreti yoktur. Teslim edilen her siparişin komisyonu ve net tutarı satıcı panelinde görünür; hakedişler IBAN'a ödenir.</div>
  <table class="s"><thead><tr><th>Ana kategori</th><th>Alt kategori sayısı</th><th>Standart oran</th><th>Özel grup oranı*</th></tr></thead><tbody>{''.join(summary)}</tbody></table>
  <div class="fn">* <b>Özel grup oranı:</b> Kadın girişimciler, genç girişimciler, kooperatifler, dernekler, çiftçiler ve üreticiler için başvurudan itibaren 12 ay geçerlidir.<br>
  Oranlar ürünün bulunduğu en alt kategoriye göre uygulanır. Bu liste bilgilendirme amaçlıdır; güncel oranlar satıcı panelinde yer alır.<br>
  Bilgi ve başvuru: getirtrend.com/satici-ol · WhatsApp 0537 618 63 16</div>
</div>
{''.join(body)}
<div class="fn">* Özel grup oranı: kadın ve genç girişimciler, kooperatifler, dernekler, çiftçiler ve üreticiler için 12 ay geçerlidir.</div>
</body></html>'''
open('komisyon.html', 'w', encoding='utf-8').write(doc)
print(len(rows), 'satır,', len(groups), 'ana kategori')

"""Builds the AI prompt pack (ai-senaryolar.md) and one cinematic page per story (sNN-*.html).
A page uses assets/ai/sNN/1.jpg..4.jpg; missing images fall back to a real photo so pages always render."""
import re
from pathlib import Path
from stories import STORIES, STYLE

HERE = Path(__file__).parent
FALLBACK = ["lahmacun2", "pide", "kebap", "durum", "adana", "baklava"]
CTA = {"restoran": ("Restoranını ücretsiz ekle", "İlk etapta komisyon yok · Kapıda ödeme", "getirtrend.com/restoran-ol"),
       "magaza": ("Mağazanı ücretsiz aç", "Aylık ücret yok · Yalnız satışta %10", "getirtrend.com/satici-ol")}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.replace("İ", "i").replace("I", "ı").lower().translate(str.maketrans("çğıöşüâ", "cgiosua"))).strip("-")

md = ["# getirtrend – 25 yapay zekâ reklam senaryosu\n",
      "Her senaryo için 4 görsel üretin (Gemini / Kling / Midjourney). Her komutun sonuna şu stil eklidir:\n",
      f"`{STYLE}`\n",
      "Görselleri **sıra numarasıyla** gönderin (ör. *s07 – 1, 2, 3, 4*). Videoya yazı, logo, müzik ve kapanışı ben eklerim.\n"]
for sid, title, kind, music, scenes in STORIES:
    md.append(f"\n## {sid.upper()} · {title} ({'Restoran' if kind == 'restoran' else 'Mağaza'})\n")
    for i, (p, a, b) in enumerate(scenes, 1):
        md.append(f"{i}. **Ekran yazısı:** {a} {b}\n   ```\n   {p}, {STYLE}\n   ```")
    head, sub, url = CTA[kind]
    head_html = f'{head.split(" ", 1)[0]}<br><em>{head.split(" ", 1)[1]}</em>'
    shots = []
    for i, (p, a, b) in enumerate(scenes, 1):
        img = f"assets/ai/{sid}/{i}.jpg"
        if not (HERE / img).exists():
            img = f"assets/{FALLBACK[(int(sid[1:]) + i) % len(FALLBACK)]}.jpg"
        shots.append((img, a, b))
    js = ",".join(f"['{img}',`{a}`,`{b}`]" for img, a, b in shots)
    html = f'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><title>getirtrend – {title}</title>
<link rel="stylesheet" href="engine.css"><link rel="stylesheet" href="assets/brand.css"><link rel="stylesheet" href="ad.css">
<style>
  #stage {{ background:#000; color:#fff; }} .scene {{ padding:0; }}
  .shot {{ position:absolute; inset:-2%; background-size:cover; background-position:center; }}
  .grade {{ position:absolute; inset:0; background:linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,0) 28%, rgba(0,0,0,0) 55%, rgba(0,0,0,.8)); }}
  .bars {{ position:absolute; left:0; right:0; height:90px; background:#000; z-index:4; }}
  .t {{ position:absolute; left:70px; right:70px; bottom:250px; text-align:left; z-index:5; }}
  .t .a {{ display:block; font:300 76px/1.04 'Inter'; letter-spacing:-2px; }}
  .t .b {{ display:block; font:800 104px/1 'Plus Jakarta Sans'; letter-spacing:-4px; color:#FFB21E; }}
  .tag {{ position:absolute; top:130px; left:70px; z-index:5; }}
  .idx {{ position:absolute; top:142px; right:70px; z-index:5; font:600 28px 'Inter'; letter-spacing:4px; opacity:.7; }}
  #end {{ background:#F5F1EB; color:#1d1a17; }}
</style></head>
<body data-music="{music}" data-dots="off">
<div id="stage">
  <div class="scene" id="m" data-static="1" data-dur="14.4" data-sfx="whoosh:0;whoosh:3.6;whoosh:7.2;whoosh:10.8">
    <div id="shots"></div><div class="grade"></div>
    <div class="bars" style="top:0"></div><div class="bars" style="bottom:0"></div>
    <div class="tag"><span class="gt inv" style="font-size:46px"><img src="assets/logo-mark.svg"><span>getir<b>trend</b></span></span></div>
    <div class="idx" id="idx"></div>
    <div class="t" id="t"></div>
  </div>
  <div class="scene" id="end" data-dur="5.0" data-sfx="success:0.4">
    <div data-in="0.1" data-anim="pop"><span class="gt" style="font-size:130px"><img src="assets/logo-mark.svg"><span>getir<b>trend</b></span></span></div>
    <div style="height:40px"></div>
    <div class="cap" data-in="0.4">{head_html}</div>
    <div style="height:24px"></div>
    <div data-in="0.8" style="font:600 40px 'Inter';opacity:.75">{sub}</div>
    <div style="height:70px"></div>
    <div class="btnr" data-in="1.2" data-anim="pop" id="cta">{url}</div>
  </div>
</div>
<script src="engine.js"></script>
<script>
  const $ = id => document.getElementById(id);
  const S = [{js}], L = 3.6;
  const eio = k => (k = clamp(k), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  $('shots').innerHTML = S.map((s, i) => `<div class="shot" id="s${{i}}" style="background-image:url(${{s[0]}})"></div>`).join('');
  window.DEFAULT_DURS = [14.4, 5.0];
  let cur = -1;
  HOOKS.m = (lt) => {{
    const i = Math.min(S.length - 1, Math.floor(lt / L)), k = lt - i * L;
    S.forEach((s, j) => {{
      const el = $('s' + j), kk = lt - j * L;
      const vis = kk > -0.01 && kk < L + 0.5;
      el.style.display = vis ? 'block' : 'none'; if (!vis) return;
      el.style.zIndex = j; el.style.opacity = j === 0 ? 1 : eio(kk / 0.5);
      const dir = j % 2 ? -1 : 1;
      el.style.transform = `scale(${{1.06 + 0.1 * clamp(kk / (L + 0.5))}}) translateX(${{dir * 24 * clamp(kk / L)}}px)`;
    }});
    if (i !== cur) {{ cur = i; $('t').innerHTML = `<span class="a">${{S[i][1]}}</span><span class="b">${{S[i][2]}}</span>`; $('idx').textContent = `0${{i + 1}} / 0${{S.length}}`; }}
    const e = eio((k - 0.25) / 0.6), o = i < S.length - 1 ? 1 - eio((k - L + 0.3) / 0.3) : 1;
    $('t').style.opacity = Math.min(e, o); $('t').style.transform = `translateY(${{(1 - e) * 40}}px)`; $('t').style.clipPath = `inset(0 0 ${{(1 - e) * 100}}% 0)`;
  }};
  HOOKS.end = (lt) => {{ if (lt > 2) $('cta').style.transform = `scale(${{1 + 0.04 * Math.sin((lt - 2) * 7)}})`; }};
</script>
</body></html>
'''
    (HERE / f"{sid}-{slug(title)}.html").write_text(html, encoding="utf-8")
(HERE / "ai-senaryolar.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("ok", len(STORIES))

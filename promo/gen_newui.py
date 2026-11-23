"""Videos built on the new dark getirtrend UI (assets/ui2, captured from getirtrend.com).
python3 gen_newui.py → v30..v33 pages; build with build2.py."""
from pathlib import Path
import json

HERE = Path(__file__).parent
K = 596 / 390  # css px of the 390-wide screenshots -> phone screen px

# scene kinds:
#  title: big type   {t:'title', a, b, dur, sfx}
#  phone: scrolling page in a phone {t:'phone', img, head, y0, y1, a, b, dur, tap:[x,y,at]?}
#  view:  static screenshot in phone {t:'view', img, a, b, dur, tap?, zoom?}
#  end:   CTA       {t:'end', a, b, url, sub}
VIDEOS = {
 "v30-bugun-ne-istersin": ("house", [
   dict(t='title', a='Bugün', b='ne istersin?', dur=2.4, sfx='whoosh:0;pop:0.3'),
   dict(t='view', img='home-view', a='Yemek mi,', b='alışveriş mi?', dur=3.4, tap=[195, 290, 2.3], sfx='tap:2.3'),
   dict(t='phone', img='yemek', head='yemek', y0=0, y1=1150, a='Mahallenin', b='restoranları', dur=4.2, sfx='whoosh:0'),
   dict(t='view', img='yemek-view', a='Yıldırım Fırsat:', b='%15 indirim', dur=3.4, zoom=1, sfx='ding:0.5'),
   dict(t='phone', img='restoran', head='yemek', y0=0, y1=1500, a='Menüye bak,', b='sepete ekle', dur=4.2, tap=[330, 1350, 3.4], sfx='whoosh:0;tap:3.4'),
   dict(t='phone', img='magazalar', head='alis', y0=0, y1=1100, a='Alışveriş de', b='burada', dur=3.6, sfx='whoosh:0'),
   dict(t='end', a='Yemek de, alışveriş de', b='getirtrend’de', url='getirtrend.com', sub='Kapıda nakit ya da kartla öde · Canlı sipariş takibi', dur=5.0, sfx='success:0.4'),
 ]),
 "v31-yildirim-firsat": ("pop", [
   dict(t='count', a='Şu an yayında', b='Yıldırım Fırsat', dur=3.6, sfx='whoosh:0;ding:0.6'),
   dict(t='view', img='yemek-view', a='Katılan restoranlarda', b='%15 indirim', dur=3.6, zoom=1, sfx='pop:0.4'),
   dict(t='phone', img='yemek', head='yemek', y0=1500, y1=3600, a='Gün boyu,', b='menünün tamamında', dur=4.4, sfx='whoosh:0'),
   dict(t='title', a='İndirim', b='sepete kendiliğinden', dur=2.8, sfx='cash:0.3'),
   dict(t='end', a='Fırsat bitmeden', b='sipariş ver', url='getirtrend.com', sub='Yıldırım Fırsat · Katılan restoranlarda geçerli', dur=5.0, sfx='success:0.4'),
 ]),
 "v32-alisveris": ("groove", [
   dict(t='title', a='getirtrend’de', b='alışveriş de var', dur=2.6, sfx='whoosh:0;pop:0.3'),
   dict(t='phone', img='magazalar', head='alis', y0=0, y1=700, a='Fırsat ve', b='yeni ürünler', dur=3.8, sfx='whoosh:0'),
   dict(t='phone', img='magazalar', head='alis', y0=600, y1=1500, a='Güvenilir', b='mağazalar', dur=4.4, sfx='whoosh:0'),
   dict(t='phone', img='magazalar', head='alis', y0=1600, y1=2350, a='Sen de', b='burada sat', dur=3.8, sfx='whoosh:0'),
   dict(t='end', a='Kapına kadar', b='alışveriş', url='getirtrend.com/magazalar', sub='Ödeme ve iade getirtrend güvencesinde', dur=5.0, sfx='success:0.4'),
 ]),
 "v33-satici-restoran-ol": ("corporate", [
   dict(t='title', a='İşini', b='getirtrend’e taşı', dur=2.6, sfx='whoosh:0;pop:0.3'),
   dict(t='phone', img='restoran-ol', head='yemek', y0=0, y1=1300, a='Restoranlar:', b='ilk etapta komisyon yok', dur=4.6, sfx='whoosh:0'),
   dict(t='phone', img='restoran', head='yemek', y0=0, y1=600, a='Menünü resimleriyle', b='biz yükleriz', dur=3.6, sfx='whoosh:0'),
   dict(t='phone', img='satici', head='alis', y0=0, y1=1400, a='Mağazalar:', b='yalnız satışta %10', dur=4.6, sfx='whoosh:0'),
   dict(t='end2', dur=5.6, sfx='success:0.4'),
 ]),
}

TPL = '''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><title>getirtrend – __TITLE__</title>
<link rel="stylesheet" href="engine.css"><link rel="stylesheet" href="assets/brand.css"><link rel="stylesheet" href="ad.css">
<style>
  #stage { background: #120D0B; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; }
  .scene { padding: 0; }
  .bgl { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 30%, rgba(215,53,31,.38), transparent 70%), radial-gradient(60% 40% at 80% 95%, rgba(255,178,30,.14), transparent 70%); }
  .ph { position: absolute; left: 222px; top: 500px; transform-origin: 50% 0; }
  .ph .scr { background: #120D0B; }
  .ph .head { position: absolute; left: 0; top: 0; width: 596px; z-index: 3; }
  .ph .nav { position: absolute; left: 0; bottom: 0; width: 596px; z-index: 3; }
  .ph .pg { position: absolute; left: 0; top: 0; width: 596px; will-change: transform; }
  .cap { position: absolute; left: 70px; right: 70px; top: 170px; text-align: left; }
  .cap .a { display: block; font: 300 70px/1.05 'Inter'; letter-spacing: -2px; color: rgba(255,255,255,.85); }
  .cap .b { display: block; font: 800 96px/1 'Plus Jakarta Sans'; letter-spacing: -4px; color: #FF6A4D; }
  .tg { position: absolute; top: 80px; left: 70px; }
  .big { text-align: center; }
  .big .a { display: block; font: 300 96px/1.05 'Inter'; letter-spacing: -3px; }
  .big .b { display: block; font: 800 136px/0.98 'Plus Jakarta Sans'; letter-spacing: -6px; color: #FF6A4D; }
  .cd { display: flex; gap: 22px; margin-top: 60px; justify-content: center; }
  .cd div { background: #fff; color: #120D0B; border-radius: 26px; width: 190px; padding: 22px 0; text-align: center; font: 800 110px/1 'Plus Jakarta Sans'; }
  .cd small { display: block; font: 600 28px 'Inter'; color: #6b625a; margin-top: 6px; }
  .pct { font: 800 300px/0.9 'Plus Jakarta Sans'; letter-spacing: -14px; color: #FFB21E; }
  .btnw { background: #D7351F; color: #fff; font: 800 58px 'Plus Jakarta Sans'; padding: 32px 66px; border-radius: 999px; box-shadow: 0 20px 60px rgba(215,53,31,.5); }
  .ctaw { border: 3px solid rgba(255,255,255,.85); border-radius: 999px; padding: 26px 46px; font: 700 42px 'Plus Jakarta Sans'; white-space: nowrap; }
</style></head>
<body data-music="__MUSIC__" data-dots="off">
<div id="stage">__SCENES__</div>
<script src="engine.js"></script>
<script>
  const $ = id => document.getElementById(id), K = __K__;
  const eio = k => (k = clamp(k), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  const spring = k => k <= 0 ? 0 : 1 - Math.exp(-6 * k) * Math.cos(10 * k);
  const SC = __CFG__;
  window.DEFAULT_DURS = SC.map(s => s.dur);
  SC.forEach((s, i) => {
    HOOKS['c' + i] = (lt) => {
      const cap = $('cap' + i);
      if (cap) { const e = eio((lt - 0.15) / 0.6), o = 1 - eio((lt - s.dur + 0.3) / 0.3);
        cap.style.opacity = Math.min(e, o); cap.style.clipPath = `inset(0 0 ${(1 - e) * 100}% 0)`; cap.style.transform = `translateY(${(1 - e) * 40}px)`; }
      const ph = $('ph' + i);
      if (ph) { const e = spring(clamp(lt / 0.8)); ph.style.transform = `translateY(${(1 - e) * 500}px) scale(${1.12 * (s.zoom ? 1 + 0.06 * clamp(lt / s.dur) : 1)})`; }
      const pg = $('pg' + i);
      if (pg && s.t === 'phone') pg.style.transform = `translateY(${-(s.y0 + (s.y1 - s.y0) * eio((lt - 0.7) / (s.dur - 1.2))) * K}px)`;
      const tp = $('tp' + i);
      if (tp && s.tap) { const at = s.tap[2], k = clamp((lt - at + 0.5) / 0.5), pr = clamp((lt - at) / 0.25);
        const scroll = s.t === 'phone' ? (s.y0 + (s.y1 - s.y0) * eio((lt - 0.7) / (s.dur - 1.2))) : 0;
        tp.style.left = (s.tap[0] * K) + 'px'; tp.style.top = ((s.tap[1] - scroll) * K) + 'px';
        tp.style.opacity = lt < at ? eio(k) : 1 - pr; tp.style.transform = `scale(${lt < at ? 1 : 1 - .3 * Math.sin(pr * Math.PI)})`; }
      const big = $('big' + i);
      if (big) { [...big.children].forEach((c, j) => { const e = spring(clamp((lt - 0.1 - j * 0.15) / 0.7)); c.style.opacity = clamp(e * 2); c.style.transform = `translateY(${(1 - e) * 80}px)`; }); }
      if (s.t === 'count') { const left = 3 * 3600 - 2 * 60 - 14 - Math.floor(lt * 1); const h = Math.floor(left / 3600), m = Math.floor(left % 3600 / 60), sec = left % 60;
        $('h' + i).textContent = String(h).padStart(2, '0'); $('m' + i).textContent = String(m).padStart(2, '0'); $('s' + i).textContent = String(sec).padStart(2, '0'); }
      const bt = $('bt' + i); if (bt && lt > 2) bt.style.transform = `scale(${1 + 0.04 * Math.sin((lt - 2) * 7)})`;
    };
  });
</script>
</body></html>
'''

def scene_html(i, s):
    tag = '<div class="tg"><span class="gt inv" style="font-size:46px"><img src="assets/logo-mark.svg"><span>getir<b>trend</b></span></span></div>'
    cap = f'<div class="cap" id="cap{i}"><span class="a">{s.get("a","")}</span><span class="b">{s.get("b","")}</span></div>'
    attrs = f'class="scene" id="c{i}" data-static="1" data-dur="{s["dur"]}" data-sfx="{s.get("sfx","")}"'
    t = s['t']
    if t in ('phone', 'view'):
        img = f'assets/ui2/{s["img"]}.jpg' if t == 'phone' else f'assets/ui2/{s["img"]}.jpg'
        if t == 'view': img = f'assets/ui2/{s["img"]}.jpg'
        inner = (f'<img class="pg" id="pg{i}" src="assets/ui2/{s["img"]}.jpg" style="top:{162 if t=="phone" else 0}px">'
                 if t == 'phone' else f'<img class="pg" src="assets/ui2/{s["img"]}.jpg">')
        head = f'<img class="head" src="assets/ui2/head-{s["head"]}.png">' if t == 'phone' else ''
        nav = '<img class="nav" src="assets/ui2/nav.png">' if t == 'phone' else ''
        tap = '<div class="tapc" id="tp%d"></div>' % i if s.get('tap') else ''
        return f'<div {attrs}><div class="bgl"></div>{tag}{cap}<div class="ph" id="ph{i}"><div class="isl"></div><div class="scr">{head}{inner}{nav}{tap}</div></div></div>'
    if t == 'title':
        return f'<div {attrs}><div class="bgl"></div>{tag}<div class="big" id="big{i}"><span class="a">{s["a"]}</span><span class="b">{s["b"]}</span></div></div>'
    if t == 'count':
        return (f'<div {attrs}><div class="bgl"></div>{tag}<div class="big" id="big{i}"><span class="a" style="font-size:60px">{s["a"]}</span>'
                f'<span class="b" style="color:#fff">{s["b"]}</span><span class="pct">%15</span>'
                f'<span class="cd"><div><span id="h{i}">02</span><small>saat</small></div><div><span id="m{i}">57</span><small>dk</small></div><div><span id="s{i}">46</span><small>sn</small></div></span></div></div>')
    if t == 'end':
        return (f'<div {attrs}><div class="bgl"></div><div class="big" id="big{i}"><span><span class="gt inv" style="font-size:120px"><img src="assets/logo-mark.svg"><span>getir<b>trend</b></span></span></span>'
                f'<span class="a" style="margin-top:50px;font-size:66px">{s["a"]}</span><span class="b" style="font-size:108px">{s["b"]}</span>'
                f'<span style="display:block;margin-top:40px;font:600 36px Inter;opacity:.75">{s["sub"]}</span>'
                f'<span style="display:inline-block;margin-top:70px" class="btnw" id="bt{i}">{s["url"]}</span></div></div>')
    if t == 'end2':
        return (f'<div {attrs}><div class="bgl"></div><div class="big" id="big{i}"><span><span class="gt inv" style="font-size:120px"><img src="assets/logo-mark.svg"><span>getir<b>trend</b></span></span></span>'
                f'<span class="a" style="margin-top:50px;font-size:66px">Başvuru ücretsiz,</span><span class="b" style="font-size:108px">aylık ücret yok</span>'
                f'<span style="display:flex;flex-direction:column;align-items:center;gap:26px;margin-top:70px"><span class="btnw" id="bt{i}" style="font-size:44px">Restoran → getirtrend.com/restoran-ol</span>'
                f'<span class="ctaw">Mağaza → getirtrend.com/satici-ol</span></span></div></div>')

for name, (music, scenes) in VIDEOS.items():
    cfg = [{k: v for k, v in s.items() if k in ('t', 'dur', 'y0', 'y1', 'tap', 'zoom')} for s in scenes]
    html = (TPL.replace('__TITLE__', name).replace('__MUSIC__', music).replace('__K__', str(K))
            .replace('__CFG__', json.dumps(cfg)).replace('__SCENES__', '\n'.join(scene_html(i, s) for i, s in enumerate(scenes))))
    (HERE / f'{name}.html').write_text(html, encoding='utf-8')
    print(name, round(sum(s['dur'] for s in scenes), 1), 'sn')

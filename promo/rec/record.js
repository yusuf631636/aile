// Records a real session on getirtrend.com as a phone (no order is placed).
const { chromium, devices } = require('playwright');
const flow = process.argv[2], out = process.argv[3];
(async () => {
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const b = await chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const ctx = await b.newContext({ ...devices['iPhone 13'], viewport: { width: 390, height: 844 }, ignoreHTTPSErrors: true, locale: 'tr-TR' });
  // visible finger: red ring wherever a tap happens
  await ctx.addInitScript(() => { addEventListener('pointerdown', e => { const d = document.createElement('div');
    Object.assign(d.style, { position: 'fixed', left: e.clientX - 28 + 'px', top: e.clientY - 28 + 'px', width: '56px', height: '56px', borderRadius: '50%',
      background: 'rgba(255,255,255,.35)', border: '3px solid #fff', boxShadow: '0 0 0 3px rgba(215,53,31,.8)', zIndex: 2147483647, pointerEvents: 'none', transition: 'transform .35s, opacity .35s' });
    document.documentElement.appendChild(d); requestAnimationFrame(() => { d.style.transform = 'scale(1.6)'; d.style.opacity = '0'; }); setTimeout(() => d.remove(), 500); }, true); });
  const p = await ctx.newPage();
  // high-res capture via CDP screencast (device pixels), frames saved with timestamps
  require('fs').mkdirSync(out + '/frames', { recursive: true });
  const cdp = await ctx.newCDPSession(p); const meta = [];
  cdp.on('Page.screencastFrame', async f => { const n = String(meta.length).padStart(5, '0');
    require('fs').writeFileSync(`${out}/frames/${n}.jpg`, Buffer.from(f.data, 'base64')); meta.push([n, f.metadata.timestamp]);
    await cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 88, maxWidth: 1170, maxHeight: 2532, everyNthFrame: 1 });
  const W = ms => p.waitForTimeout(ms);
  const scroll = async (px, ms = 1400) => { const n = Math.round(ms / 16); for (let i = 0; i < n; i++) { const k = (1 - Math.cos(Math.PI * (i + 1) / n)) / 2 - (1 - Math.cos(Math.PI * i / n)) / 2; await p.evaluate(d => scrollBy(0, d), px * k); await W(16); } };
  const tap = async (loc) => { await loc.scrollIntoViewIfNeeded({ timeout: 8000 }); const bb = await loc.boundingBox(); await W(250); await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down(); await W(90); await p.mouse.up(); };
  const t0 = Date.now(); const mark = (l) => console.log('MARK', ((Date.now() - t0) / 1000).toFixed(2), l);
  if (flow === 'yemek') {
    await p.goto('https://getirtrend.com/', { waitUntil: 'networkidle' }); mark('home'); await W(2400);
    await tap(p.locator('a:has-text("Restoranlar, Yıldırım")').first()); await p.waitForLoadState('networkidle'); mark('yemek'); await W(3000);
    const k = p.getByRole('button', { name: /Küçült/ }).first(); if (await k.count()) { await tap(k).catch(() => {}); await W(900); }
    await scroll(700); await W(500); await scroll(800); await W(800); mark('list');
    await tap(p.locator('a[href$="/yemek/misss-lahmacun"]:visible').first()); await p.waitForLoadState('networkidle'); mark('rest'); await W(2200);
    await scroll(600); await W(700); await scroll(700); await W(700); await scroll(600); await W(1200); mark('menu');
  } else {
    await p.goto('https://getirtrend.com/', { waitUntil: 'networkidle' }); mark('home'); await W(2000);
    await tap(p.locator('a:has-text("Giyim, elektronik")').first()); await p.waitForLoadState('networkidle'); mark('magaza'); await W(2000);
    await scroll(500); await W(600); await scroll(500); await W(600);
    const prod = p.locator('main a[href*="/urun/"]:visible, main a[href*="/magaza/"]:visible').first();
    console.log('prodcount', await prod.count(), await prod.getAttribute('href').catch(() => ''));
    await tap(prod); await p.waitForLoadState('networkidle'); mark('urun'); await W(2200);
    await scroll(500); await W(700); await scroll(600); await W(1500); mark('end');
  }
  await W(400); await cdp.send('Page.stopScreencast').catch(() => {});
  require('fs').writeFileSync(out + '/frames.json', JSON.stringify(meta));
  console.log('url', p.url(), 'frames', meta.length);
  await ctx.close(); await b.close();
})();

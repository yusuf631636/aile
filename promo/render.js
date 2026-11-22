// Captures a promo page frame by frame. Usage: node render.js <page.html> <framesDir> <dursJSON> [fps]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const http = require('http');
// tiny static server: ES modules (three.js pages) cannot load over file://
function serve(root) {
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.woff2': 'font/woff2' };
  return new Promise(res => { const srv = http.createServer((q, r) => {
    const f = path.join(root, decodeURIComponent(q.url.split('?')[0]));
    fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
  }).listen(0, '127.0.0.1', () => res(srv)); });
}

(async () => {
  const [html, out, dursJson, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const srv = await serve(path.dirname(path.resolve(html)));
  await page.goto(`http://127.0.0.1:${srv.address().port}/${path.basename(html)}?capture`);
  await page.waitForFunction(() => window.setTimeline && (window.READY === undefined || window.READY === true), null, { timeout: 60000 });
  // load every declared font face up front so text never renders in a fallback font mid-video
  await page.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
  await page.evaluate(async () => { await Promise.all([...document.fonts].map(f => f.load().catch(() => {}))); await document.fonts.ready; });
  const total = await page.evaluate(d => window.setTimeline(d), JSON.parse(dursJson));
  const n = Math.round((total + 0.8) * fps); // hold the last scene a little after the voice ends
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    await page.screenshot({ path: path.join(out, `f${String(i).padStart(5, '0')}.png`) });
  }
  await browser.close(); srv.close();
  console.log(`${html}: ${n} frames`);
})();

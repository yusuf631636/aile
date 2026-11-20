// Captures a promo page frame by frame. Usage: node render.js <page.html> <framesDir> <dursJSON> [fps]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [html, out, dursJson, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html) + '?capture');
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(d => window.setTimeline(d), JSON.parse(dursJson));
  const n = Math.round((total + 0.8) * fps); // hold the last scene a little after the voice ends
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    await page.screenshot({ path: path.join(out, `f${String(i).padStart(5, '0')}.png`) });
  }
  await browser.close();
  console.log(`${html}: ${n} frames`);
})();

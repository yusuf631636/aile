// Prints the scene list (length + sound cues) of a promo page after its scripts have run.
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(process.argv[2]) + '?capture');
  console.log(JSON.stringify(await p.evaluate(() => ({ music: document.body.dataset.music, sw: document.body.dataset.switch || '0',
    scenes: [...document.querySelectorAll('.scene')].map(s => ({ dur: +s.dataset.dur, sfx: s.dataset.sfx || '' })) }))));
  await b.close(); })();

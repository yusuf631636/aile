"""Puts a real screen recording of getirtrend.com (record.js) into a phone with captions, music and an end card.
Usage: python3 compose.py <recording.webm> <out.mp4> <config.json> <workdir>"""
import json, subprocess, sys, urllib.parse
from pathlib import Path
HERE = Path(__file__).resolve().parent; PROMO = HERE.parent
rec, out, cfgp, wd = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4]); wd.mkdir(parents=True, exist_ok=True)
cfg = json.load(open(cfgp, encoding='utf-8'))
trim, clip = cfg['trim'], cfg['clip']           # seconds cut from the start / length kept
caps, end, END = cfg['caps'], cfg['end'], 5.0
total = clip + END
shots = [('bg', {}, False), ('mask', {}, False), ('bezel', {}, True)] + [(f'cap{i}', dict(k='cap', a=c[2], b=c[3]), True) for i, c in enumerate(caps)] + [('end', dict(k='end', **end), False)]
js = """const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [name, q, transp] of JSON.parse(process.argv[2])) {
    await p.goto('file://' + path.join(process.argv[3], 'layers.html') + '?' + new URLSearchParams({ k: name, ...q }));
    await p.evaluate(async () => { await Promise.all([...document.fonts].map(f => f.load().catch(() => {}))); await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => i.onload = r))); });
    await p.waitForTimeout(150); await p.screenshot({ path: path.join(process.argv[4], name + '.png'), omitBackground: transp }); }
  await b.close(); })();"""
(wd / 'shots.js').write_text(js)
subprocess.run(['node', str(wd / 'shots.js'), json.dumps([[n, dict(k=n, **q) if 'k' not in q else q, t] for n, q, t in shots]), str(HERE), str(wd)], check=True)
subprocess.run([sys.executable, str(PROMO / 'music2.py'), cfg.get('music', 'house'), f'{total:.2f}', str(wd / 'music.wav')], check=True, capture_output=True)
subprocess.run([sys.executable, str(PROMO / 'sfx.py'), str(wd / 'sfx')], check=True, capture_output=True)
# inputs: 0 bg, 1 rec, 2 mask, 3 bezel, 4.. caps, then end, music, tap sfx
cut = wd / 'cut.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', rec, '-ss', str(trim), '-t', str(clip), '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', str(cut)], check=True)
# round the screen corners in a separate pass (keeps the recording perfectly in sync)
rnd = wd / 'round.mov'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(cut), '-i', str(wd / 'mask.png'), '-filter_complex',
                f'[0:v]fps=30,scale=640:1382,setsar=1,tpad=stop_mode=clone:stop_duration={END},format=rgba[v];[1:v]format=gray,crop=640:1382:220:442,loop=-1:1:0,fps=30[m];[v][m]alphamerge,trim=duration={total}[o]',
                '-map', '[o]', '-c:v', 'png', str(rnd)], check=True)
ins = ['-loop', '1', '-t', f'{total}', '-i', str(wd / 'bg.png'), '-i', str(rnd),
       '-loop', '1', '-t', f'{total}', '-i', str(wd / 'mask.png'), '-loop', '1', '-t', f'{total}', '-i', str(wd / 'bezel.png')]
for i in range(len(caps)): ins += ['-loop', '1', '-t', f'{total}', '-i', str(wd / f'cap{i}.png')]
ins += ['-loop', '1', '-t', f'{total}', '-i', str(wd / 'end.png'), '-i', str(wd / 'music.wav'), '-i', str(wd / 'sfx' / 'tap.wav'), '-i', str(wd / 'sfx' / 'whoosh.wav')]
ne = 4 + len(caps); nm, nt, nw = ne + 1, ne + 2, ne + 3
f = ['[0:v]fps=30[bg]', '[bg][1:v]overlay=220:442:eof_action=repeat[a0]', '[a0][3:v]overlay=0:0[a1]']
last = 'a1'
for i, (s, e, *_ ) in enumerate(caps):
    f.append(f'[{4+i}:v]format=rgba,fade=in:st={s}:d=0.4:alpha=1,fade=out:st={e-0.35}:d=0.35:alpha=1[c{i}]')
    f.append(f'[{last}][c{i}]overlay=0:0:enable=\'between(t,{s},{e})\'[o{i}]'); last = f'o{i}'
f.append(f'[{ne}:v]format=rgba,fade=in:st={clip}:d=0.5:alpha=1[ec]'); f.append(f'[{last}][ec]overlay=0:0:enable=\'gte(t,{clip})\',format=yuv420p[v]')
taps = cfg.get('taps', [])
amix = ['[%d:a]volume=0.9[mu]' % nm]
for j, t in enumerate(taps): amix.append(f'[{nt}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.6[t{j}]')
amix.append(f'[{nw}:a]adelay={int(clip*1000)}|{int(clip*1000)},volume=0.5[w]')
amix.append(''.join(['[mu]'] + [f'[t{j}]' for j in range(len(taps))] + ['[w]']) + f'amix=inputs={len(taps)+2}:normalize=0,loudnorm=I=-15:TP=-1.5[a]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(f + amix), '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.2f}', '-movflags', '+faststart', out], check=True)
print('wrote', out)

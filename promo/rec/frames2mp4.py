"""Turns CDP screencast frames (variable timing) into a constant 30 fps mp4.
Usage: python3 frames2mp4.py <recording dir> <out.mp4>"""
import json, subprocess, sys
from pathlib import Path

d = Path(sys.argv[1]); out = sys.argv[2]
meta = json.load(open(d / 'frames.json'))
lines = ['ffconcat version 1.0']
for i, (n, ts) in enumerate(meta):
    dur = (meta[i + 1][1] - ts) if i + 1 < len(meta) else 0.5
    lines += [f"file 'frames/{n}.jpg'", f'duration {max(dur, 0.001):.4f}']
lines.append(f"file 'frames/{meta[-1][0]}.jpg'")
(d / 'list.txt').write_text('\n'.join(lines))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(d / 'list.txt'),
                '-vf', 'fps=30,scale=1170:2532:force_original_aspect_ratio=decrease,pad=1170:2532,format=yuv420p',
                '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', out], check=True)
print('wrote', out, round(meta[-1][1] - meta[0][1], 2), 's')

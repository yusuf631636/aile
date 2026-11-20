"""Generates a simple, royalty-free upbeat background track (WAV) with numpy.
Usage: python3 music.py out.wav [seconds] [bpm] [seed]
"""
import sys, wave
import numpy as np

SR = 44100
out = sys.argv[1]
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 112
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
beat = 60 / bpm
t = np.arange(int(SR * dur)) / SR
mix = np.zeros_like(t)

def note(f, start, length, vol, kind="saw"):
    i0, i1 = int(start * SR), min(int((start + length) * SR), len(t))
    if i0 >= len(t):
        return
    tt = np.arange(i1 - i0) / SR
    if kind == "sine":
        w = np.sin(2 * np.pi * f * tt)
    else:  # soft saw (few harmonics)
        w = sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 6))
    env = np.minimum(1, tt / 0.01) * np.exp(-tt * 3.0)
    mix[i0:i1] += vol * w * env

# I - V - vi - IV in C major
progs = [
    [[261.63, 329.63, 392.0], [196.0, 246.94, 293.66], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63]],  # I V vi IV
    [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]],  # vi IV I V
    [[174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66], [220.0, 261.63, 329.63]],  # IV I V vi
    [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]],  # I vi IV V
]
chords = progs[seed % len(progs)]
bars = int(dur / (4 * beat)) + 1
for b in range(bars):
    ch = chords[b % 4]
    for s in range(8):  # eighth-note plucks
        start = b * 4 * beat + s * beat / 2
        note(ch[s % 3] * 2, start, beat / 2, 0.06)
    note(ch[0] / 2, b * 4 * beat, 4 * beat, 0.18, "sine")  # bass
    for f in ch:  # warm pad
        i0 = int(b * 4 * beat * SR); i1 = min(int((b + 1) * 4 * beat * SR), len(t))
        if i0 < len(t):
            tt = np.arange(i1 - i0) / SR
            mix[i0:i1] += 0.025 * np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / 0.3) * np.minimum(1, (tt[-1] - tt) / 0.3 + 1e-9)
    for k in range(4):  # kick
        st = b * 4 * beat + k * beat
        i0 = int(st * SR)
        if i0 < len(t):
            n = min(int(0.18 * SR), len(t) - i0)
            tt = np.arange(n) / SR
            mix[i0:i0 + n] += 0.5 * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18)
    for k in (1, 3):  # clap-ish noise
        i0 = int((b * 4 * beat + k * beat) * SR)
        if i0 < len(t):
            n = min(int(0.12 * SR), len(t) - i0)
            mix[i0:i0 + n] += 0.12 * np.random.default_rng(b * 10 + k).standard_normal(n) * np.exp(-np.arange(n) / SR * 30)

fade = np.ones_like(t)
fl = int(1.5 * SR)
fade[-fl:] = np.linspace(1, 0, fl)
fade[: int(0.3 * SR)] = np.linspace(0, 1, int(0.3 * SR))
mix = mix * fade
mix = mix / np.max(np.abs(mix)) * 0.8
data = (mix * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out)

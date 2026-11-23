"""Synthesises small sound effects (royalty-free) used by build.py.
Usage: python3 sfx.py <outDir>
"""
import sys, wave
from pathlib import Path
import numpy as np

SR = 44100
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)


def save(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    with wave.open(str(out / f"{name}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def tt(sec):
    return np.arange(int(SR * sec)) / SR


def bell(f, sec, decay):
    t = tt(sec)
    return sum(a * np.sin(2 * np.pi * f * m * t) for m, a in ((1, 1), (2.76, .35), (5.4, .12))) * np.exp(-t * decay)


# notification "ding-ding"
d = np.zeros(int(SR * 0.9)); a = bell(1318.5, .6, 7); b = bell(1760, .6, 6)
d[:len(a)] += a; s = int(SR * .13); d[s:s + len(b)] += b
save("ding", d)

# whoosh (filtered noise sweep)
t = tt(.45); n = rng.standard_normal(len(t))
env = np.sin(np.pi * t / t[-1]) ** 2
k = np.cumsum(n); k -= np.convolve(k, np.ones(40) / 40, "same")  # crude band-pass
save("whoosh", k * env * 0.6)

# pop / tap
t = tt(.12)
save("tap", np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 45))
t = tt(.25)
save("pop", np.sin(2 * np.pi * (500 + 900 * np.exp(-t * 25)) * t) * np.exp(-t * 18))

# cash register "ka-ching"
c = np.zeros(int(SR * 1.2)); t = tt(.08)
c[:len(t)] += rng.standard_normal(len(t)) * np.exp(-t * 60) * .6
for i, f in enumerate((2637, 3136, 3951)):
    x = bell(f, 1.0, 4.5); s = int(SR * (.06 + i * .02)); c[s:s + len(x)] += x[: len(c) - s] * .6
save("cash", c)

# success chime (rising arpeggio)
c = np.zeros(int(SR * 1.0))
for i, f in enumerate((1046.5, 1318.5, 1568, 2093)):
    x = bell(f, .6, 6); s = int(SR * i * .08); c[s:s + len(x)] += x
save("success", c)
# thermal printer line (short buzzy stepper burst)
t = tt(.22)
buzz = np.sign(np.sin(2 * np.pi * 1900 * t)) * 0.25 + rng.standard_normal(len(t)) * 0.35
gate = (np.sin(2 * np.pi * 38 * t) > -0.2).astype(float)
save("print", buzz * gate * np.minimum(1, t / .01) * np.minimum(1, (t[-1] - t) / .03))

# paper tear
t = tt(.5)
save("tear", rng.standard_normal(len(t)) * np.exp(-t * 6) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t)))
# chiptune coin + level-up (square waves)
def sq(f, sec, vol=1.0):
    t = tt(sec); return np.sign(np.sin(2 * np.pi * f * t)) * vol * np.exp(-t * 4)
c = np.zeros(int(SR * .4)); a = sq(988, .08); b = sq(1319, .27)
c[:len(a)] += a; c[int(SR * .08):int(SR * .08) + len(b)] += b
save("coin", c * .5)
c = np.zeros(int(SR * 1.0))
for i, f in enumerate((523, 659, 784, 1047, 1319)):
    x = sq(f, .18); s0 = int(SR * i * .1); c[s0:s0 + len(x)] += x
save("levelup", c * .5)
# split-flap board: burst of tiny clicks
c = np.zeros(int(SR * .6))
for i in range(14):
    t = tt(.012); s0 = int(SR * (i * .035 + rng.random() * .01))
    c[s0:s0 + len(t)] += rng.standard_normal(len(t)) * np.exp(-t * 400) * (0.6 + 0.4 * rng.random())
save("flap", c * .8)
print("sfx ok")

"""Composes a background track per style as MIDI and renders it with real instrument
samples (FluidR3 General MIDI soundfont via fluidsynth). Royalty-free: everything is
generated here.

Usage: python3 music2.py <style> <seconds> <out.wav> [switchSeconds]
styles: pop (energetic, 124 bpm), chill (lo-fi, 86 bpm),
        drama (sad piano that turns into an upbeat groove at switchSeconds), acoustic (warm, 100 bpm)
"""
import subprocess, sys, tempfile
from pathlib import Path
import mido

STYLE, DUR, OUT = sys.argv[1], float(sys.argv[2]), sys.argv[3]
SWITCH = float(sys.argv[4]) if len(sys.argv) > 4 else 0
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
TPB = 480

# note helpers
NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def n(s):  # "C4", "F#3", "Bb2"
    p = NAMES[s[0]]; i = 1
    if s[i] == "#": p += 1; i += 1
    elif s[i] == "b": p -= 1; i += 1
    return 12 * (int(s[i:]) + 1) + p

def chord(root, kind="maj"):
    r = n(root); iv = {"maj": (0, 4, 7), "min": (0, 3, 7), "maj7": (0, 4, 7, 11), "min7": (0, 3, 7, 10), "sus": (0, 5, 7)}[kind]
    return [r + i for i in iv]

events = []  # (beat, channel, kind, a, b)
def note(beat, ch, pitch, length, vel=90):
    events.append((beat, ch, "on", pitch, vel)); events.append((beat + length, ch, "off", pitch, 0))
def prog(ch, prg):
    events.append((0, ch, "prog", prg, 0))
DR = 9
KICK, SNARE, CLAP, HAT, OHAT, RIDE, CRASH, TAMB, SHAKER, RIM = 36, 38, 39, 42, 46, 51, 49, 54, 70, 37

if STYLE == "pop":
    bpm = 124
    prog(0, 81); prog(1, 38); prog(2, 89); prog(3, 5)
    P = [("A3", "min"), ("F3", "maj"), ("C4", "maj"), ("G3", "maj")]
    bars = int(DUR * bpm / 240) + 2
    for b in range(bars):
        root, kind = P[b % 4]; c = chord(root, kind); t0 = b * 4
        for i in range(4):
            note(t0 + i, DR, KICK, .25, 115)
            note(t0 + i + .5, DR, OHAT if i % 2 else HAT, .25, 70)
        note(t0 + 1, DR, CLAP, .25, 100); note(t0 + 3, DR, CLAP, .25, 100)
        for i in range(8): note(t0 + i * .5 + .25, DR, HAT, .1, 45)
        if b % 4 == 0: note(t0, DR, CRASH, 1, 80)
        for i in range(8):  # driving octave bass
            note(t0 + i * .5, 1, c[0] - 24 + (12 if i % 2 else 0), .45, 100)
        for p in c: note(t0, 2, p, 4, 55)
        if b >= 2:  # lead hook
            mel = [c[2] + 12, c[1] + 12, c[0] + 12, c[1] + 12, c[2] + 12, c[2] + 14, c[2] + 12, c[1] + 12]
            for i, p in enumerate(mel): note(t0 + i * .5, 0, p, .4, 70 if i % 2 else 85)
        for i in (0, 1.5, 3): [note(t0 + i, 3, p + 12, .4, 60) for p in c]
elif STYLE == "chill":
    bpm = 86
    prog(0, 4); prog(1, 33); prog(2, 11)
    P = [("D3", "min7"), ("G3", "maj"), ("C3", "maj7"), ("A3", "min7")]
    bars = int(DUR * bpm / 240) + 2
    for b in range(bars):
        root, kind = P[b % 4]; c = chord(root, kind); t0 = b * 4
        note(t0, DR, KICK, .3, 85); note(t0 + 2.5, DR, KICK, .3, 70)
        note(t0 + 1, DR, RIM, .2, 70); note(t0 + 3, DR, SNARE, .2, 60)
        for i in range(8): note(t0 + i * .5 + (0.06 if i % 2 else 0), DR, HAT, .1, 40 + (i % 2) * 10)
        for i, d in ((0, 1.5), (1.5, 1), (2.5, 1.5)): note(t0 + i, 1, c[0] - 12, d * .9, 85)
        for j, p in enumerate(c): note(t0 + j * .04, 0, p + 12, 1.8, 60); note(t0 + 2 + j * .04, 0, p + 12, 1.8, 50)
        if b % 2: [note(t0 + 3 + k * .25, 2, c[k % len(c)] + 24, .3, 45) for k in range(4)]
elif STYLE == "drama":
    bpm = 120
    sw = SWITCH * bpm / 60  # switch beat
    sw = 4 * round(sw / 4)
    prog(0, 0); prog(1, 48); prog(2, 38); prog(3, 81); prog(4, 89)
    sad = [("A3", "min"), ("F3", "maj"), ("D3", "min"), ("E3", "maj")]
    for b in range(int(sw // 4)):
        root, kind = sad[b % 4]; c = chord(root, kind); t0 = b * 4
        for i, p in enumerate([c[0], c[1], c[2], c[1]] * 2): note(t0 + i * .5, 0, p, .5, 55)
        note(t0, 0, c[0] - 12, 4, 60)
        for p in c: note(t0, 1, p, 4, 45)
    note(sw - 1, DR, SNARE, .1, 60); note(sw - .75, DR, SNARE, .1, 70); note(sw - .5, DR, SNARE, .1, 85); note(sw - .25, DR, SNARE, .1, 100)
    happy = [("C4", "maj"), ("G3", "maj"), ("A3", "min"), ("F3", "maj")]
    bars = int((DUR * bpm / 60 - sw) / 4) + 2
    for b in range(bars):
        root, kind = happy[b % 4]; c = chord(root, kind); t0 = sw + b * 4
        if b % 4 == 0: note(t0, DR, CRASH, 1, 90)
        for i in range(4): note(t0 + i, DR, KICK, .25, 115); note(t0 + i + .5, DR, OHAT, .25, 65)
        note(t0 + 1, DR, SNARE, .25, 105); note(t0 + 3, DR, SNARE, .25, 105)
        for i in range(8): note(t0 + i * .5, 2, c[0] - 24, .4, 100)
        for p in c: note(t0, 4, p, 4, 55)
        mel = [c[0] + 12, c[1] + 12, c[2] + 12, c[2] + 14, c[2] + 12, c[1] + 12, c[0] + 12, c[1] + 12]
        for i, p in enumerate(mel): note(t0 + i * .5, 3, p, .4, 80)
        for i in range(8): note(t0 + i * .5, 0, c[i % 3] + 12, .3, 50)
elif STYLE == "acoustic":
    bpm = 100
    prog(0, 25); prog(1, 32); prog(2, 45); prog(3, 73)
    P = [("G3", "maj"), ("D3", "maj"), ("E3", "min"), ("C3", "maj")]
    bars = int(DUR * bpm / 240) + 2
    for b in range(bars):
        root, kind = P[b % 4]; c = chord(root, kind); t0 = b * 4
        strum = [0, 1, 1.5, 2.5, 3, 3.5]
        for s in strum:  # guitar strums
            for j, p in enumerate(c + [c[0] + 12]): note(t0 + s + j * .015, 0, p, .45, 80 if s in (0, 2.5) else 60)
        note(t0, 1, c[0] - 12, 1.5, 90); note(t0 + 2, 1, c[2] - 12, 1.5, 85)
        note(t0, DR, KICK, .2, 80); note(t0 + 2, DR, KICK, .2, 70)
        note(t0 + 1, DR, CLAP, .2, 60); note(t0 + 3, DR, CLAP, .2, 60)
        for i in range(8): note(t0 + i * .5, DR, SHAKER, .1, 40 + 15 * (i % 2))
        if b >= 2 and b % 2 == 0:  # flute melody
            mel = [c[2] + 12, c[1] + 12, c[0] + 12, c[1] + 12, c[2] + 12, c[2] + 12]
            for i, p in enumerate(mel): note(t0 + i * .5 + .5, 3, p, .45, 70)
        for i in (0, 1, 2, 3): note(t0 + i, 2, c[i % 3] + 12, .3, 45)  # pizzicato
elif STYLE == "chip":
    bpm = 140
    prog(0, 80); prog(1, 38); prog(2, 81)
    P = [("C4", "maj"), ("A3", "min"), ("F3", "maj"), ("G3", "maj")]
    bars = int(DUR * bpm / 240) + 2
    for b in range(bars):
        root, kind = P[b % 4]; c = chord(root, kind); t0 = b * 4
        for i in range(4): note(t0 + i, DR, KICK, .2, 110); note(t0 + i + .5, DR, HAT, .1, 60)
        note(t0 + 1, DR, SNARE, .2, 95); note(t0 + 3, DR, SNARE, .2, 95)
        for i in range(8): note(t0 + i * .5, 1, c[0] - 24 + (7 if i % 4 == 2 else 0), .4, 95)
        arp = [c[0], c[1], c[2], c[1] + 12, c[2], c[1], c[0] + 12, c[2]]
        for i, p in enumerate(arp): note(t0 + i * .5, 2, p + 12, .25, 55)
        if b >= 1:
            mel = [c[2] + 12, c[2] + 12, c[1] + 12, c[2] + 12, c[0] + 24, c[2] + 12, c[1] + 12, c[0] + 12]
            for i, p in enumerate(mel): note(t0 + i * .5, 0, p, .4, 80)
else:
    raise SystemExit("unknown style " + STYLE)

mid = mido.MidiFile(ticks_per_beat=TPB)
tr = mido.MidiTrack(); mid.tracks.append(tr)
tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm)))
for ch in range(16):
    tr.append(mido.Message("control_change", channel=ch, control=91, value=50))  # reverb
end_beat = DUR * bpm / 60 + 1
order = {"prog": 0, "off": 1, "on": 2}
last = 0
for beat, ch, kind, a, b in sorted(events, key=lambda e: (e[0], order[e[2]])):
    if beat > end_beat: continue
    tick = int(round(beat * TPB)); dt = max(0, tick - last); last = max(last, tick)
    if kind == "prog": tr.append(mido.Message("program_change", channel=ch, program=a, time=dt))
    elif kind == "on": tr.append(mido.Message("note_on", channel=ch, note=a, velocity=b, time=dt))
    else: tr.append(mido.Message("note_off", channel=ch, note=a, velocity=0, time=dt))

with tempfile.TemporaryDirectory() as td:
    mp = Path(td) / "m.mid"; raw = Path(td) / "raw.wav"
    mid.save(mp)
    subprocess.run(["fluidsynth", "-ni", "-g", "0.8", "-r", "44100", "-F", str(raw), SF2, str(mp)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    f"atrim=0:{DUR},afade=t=in:d=0.05,afade=t=out:st={max(0, DUR - 1.5)}:d=1.5,"
                    "acompressor=threshold=-16dB:ratio=2.5:attack=10:release=200,loudnorm=I=-16:TP=-1.5",
                    "-ar", "44100", "-ac", "2", OUT], check=True)
print("music", STYLE, OUT)

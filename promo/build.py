"""Builds the GetirTrend promo videos: Turkish voiceover (Piper TTS) -> scene timings ->
frame capture (Playwright) -> music + voice + sound effects mix -> MP4.

Usage: python3 build.py <voice.onnx> <workDir> [page.html ...]
  REUSE_FRAMES=1  keep already-captured frames (only re-mix audio)
Voice used: Piper tr_TR "fahrettin" (CC0). Music and SFX are synthesised (music.py, sfx.py).

Each <div class="scene"> in a page may carry:
  data-voice="..."   narration line for the scene (scene length follows it)
  data-min="4.2"     minimum scene length in seconds
  data-sfx="ding:0.4;cash:1.2"   sound effects at scene-relative times
"""
import json, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LEAD, TAIL = 0.45, 0.55          # seconds of silence before / after each voice line
SR = 44100
VOICES = sys.argv[1]
WORK = Path(sys.argv[2]); WORK.mkdir(parents=True, exist_ok=True)
PAGES = [Path(p) for p in sys.argv[3:]] or sorted(HERE.glob("v*.html"))
MUSIC = {"v1": (104, 1), "v2": (118, 2), "v3": (112, 3), "v4": (100, 0), "v5": (124, 2)}  # bpm, seed
SFX_GAIN = {"ding": .55, "cash": .6, "success": .45, "tap": .5, "pop": .45, "whoosh": .35}


def run(*cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def read_wav(p):
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x, w.getframerate()


def write_wav(p, x):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


sfx_dir = WORK / "sfx"
run(sys.executable, str(HERE / "sfx.py"), str(sfx_dir), capture_output=True)
SFX = {k: read_wav(sfx_dir / f"{k}.wav")[0] for k in SFX_GAIN}

for page in PAGES:
    name, key = page.stem, page.stem[:2]
    html = page.read_text(encoding="utf-8")
    scenes = [dict(re.findall(r'(data-[\w-]+)="([^"]*)"', tag)) for tag in re.findall(r'<div class="scene"[^>]*>', html)]
    wd = WORK / name; wd.mkdir(exist_ok=True)
    clips, durs = [], []
    for i, sc in enumerate(scenes):
        clip = wd / f"vo{i}.wav"
        if not clip.exists():  # cache: Piper output varies run to run, keep timings stable
            run(sys.executable, "-m", "piper", "-m", VOICES, "-f", str(clip), "--length-scale", "1.08",
                "--sentence-silence", "0.25", input=sc["data-voice"].encode(), capture_output=True)
        x, sr = read_wav(clip)
        clips.append(clip)
        durs.append(round(max(3.0, float(sc.get("data-min", 0)), LEAD + len(x) / sr + TAIL), 3))
    durs[-1] += 0.6
    total = sum(durs) + 0.8
    print(name, "scene durations:", durs, "total:", round(total, 2), flush=True)

    frames = wd / "frames"
    if not (os.environ.get("REUSE_FRAMES") and frames.exists()):
        run("rm", "-rf", str(frames))
        run("node", str(HERE / "render.js"), str(page), str(frames), json.dumps(durs))

    # sound-effects track: per-scene cues + a soft whoosh on every scene change
    fx = np.zeros(int(SR * (total + 2)), np.float32)
    start = 0.0
    for i, sc in enumerate(scenes):
        cues = [c.split(":") for c in sc.get("data-sfx", "").split(";") if c]
        if i > 0 and not any(c[0] == "whoosh" for c in cues):
            cues.append(["whoosh", "-0.15"])
        for kind, at in cues:
            s = int(SR * max(0, start + float(at))); snd = SFX[kind] * SFX_GAIN[kind]
            fx[s:s + len(snd)] += snd[: len(fx) - s]
        start += durs[i]
    write_wav(wd / "sfx.wav", fx * 0.8)

    bpm, seed = MUSIC.get(key, (110, 0))
    music = wd / "music.wav"
    run(sys.executable, str(HERE / "music.py"), str(music), str(total), str(bpm), str(seed), capture_output=True)

    # voice lines placed at each scene start (+LEAD); music ducked under the voice
    inputs, filters, starts = [], [], 0.0
    for i, (c, d) in enumerate(zip(clips, durs)):
        inputs += ["-i", str(c)]
        ms = int((starts + LEAD) * 1000)
        filters.append(f"[{i + 1}:a]aresample=44100,adelay={ms}|{ms}[v{i}]")
        starts += d
    n = len(clips)
    filters.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,volume=1.6,"
                   "highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,apad[vo]")
    filters.append("[vo]asplit=2[vo1][vo2]")
    filters.append(f"[{n + 1}:a]aresample=44100,volume=0.55[mu]")
    filters.append("[mu][vo1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck]")
    filters.append(f"[{n + 2}:a]aresample=44100,volume=0.7[fx]")
    filters.append("[duck][vo2][fx]amix=inputs=3:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[aout]")
    out = HERE / f"getirtrend-{name}.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(frames / "f%05d.png"),
        *inputs, "-i", str(music), "-i", str(wd / "sfx.wav"), "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-t", f"{total:.3f}", "-movflags", "+faststart", str(out))
    print("wrote", out, flush=True)

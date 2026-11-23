"""Builds the music-driven GetirTrend videos (v6+): scene lengths come from data-dur,
music from music2.py (real-instrument General MIDI rendering), plus sound effects.

Usage: python3 build2.py <workDir> page.html [page.html ...]
  REUSE_FRAMES=1        keep captured frames, only re-mix audio
  VOICE_DIR=<dir>       optional narration: <dir>/<page-name>/vo<i>.wav is placed at the start
                        of scene i (+0.4 s) and the music is ducked under it
Page attributes: <body data-music="pop|chill|drama|acoustic" data-switch="6.2">
Scene attributes: data-dur="4.5" data-sfx="ding:0.4;cash:1.2"
"""
import json, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SR = 44100
WORK = Path(sys.argv[1]); WORK.mkdir(parents=True, exist_ok=True)
PAGES = [Path(p) for p in sys.argv[2:]]
SFX_GAIN = {"ding": .5, "cash": .55, "success": .45, "tap": .45, "pop": .4, "whoosh": .3, "print": .35, "tear": .5, "coin": .3, "levelup": .35, "flap": .45}
VOICE_DIR = os.environ.get("VOICE_DIR")


def run(*cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def read_wav(p):
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
        return x


def write_wav(p, x):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


run(sys.executable, str(HERE / "sfx.py"), str(WORK / "sfx"), capture_output=True)
SFX = {k: read_wav(WORK / "sfx" / f"{k}.wav") for k in SFX_GAIN}

for page in PAGES:
    name = page.stem
    meta = json.loads(subprocess.run(["node", str(HERE / "render_meta.js"), str(page)], check=True, capture_output=True, text=True).stdout)
    body = {"data-music": meta["music"], "data-switch": meta["sw"]}
    scenes = [{"data-dur": s["dur"], "data-sfx": s["sfx"]} for s in meta["scenes"]]
    durs = [float(s["data-dur"]) for s in scenes]
    total = sum(durs) + 0.5
    wd = WORK / name; wd.mkdir(exist_ok=True)
    print(name, durs, "total", total, flush=True)

    frames = wd / "frames"
    if not (os.environ.get("REUSE_FRAMES") and frames.exists()):
        run("rm", "-rf", str(frames))
        run("node", str(HERE / "render.js"), str(page), str(frames), json.dumps(durs))
    nframes = len(list(frames.glob("f*.png")))
    total = nframes / 30

    fx = np.zeros(int(SR * (total + 2)), np.float32)
    vo = np.zeros_like(fx)
    start = 0.0
    for i, sc in enumerate(scenes):
        for cue in filter(None, sc.get("data-sfx", "").split(";")):
            kind, at = cue.split(":")
            s = int(SR * max(0, start + float(at))); snd = SFX[kind] * SFX_GAIN[kind]
            fx[s:s + len(snd)] += snd[: len(fx) - s]
        vp = Path(VOICE_DIR) / name / f"vo{i}.wav" if VOICE_DIR else None
        if vp and vp.exists():
            x = read_wav(vp); s = int(SR * (start + 0.4)); vo[s:s + len(x)] += x[: len(vo) - s]
        start += durs[i]
    write_wav(wd / "sfx.wav", fx)
    write_wav(wd / "vo.wav", vo)
    music = wd / "music.wav"
    run(sys.executable, str(HERE / "music2.py"), body.get("data-music", "pop"), f"{total:.3f}", str(music),
        body.get("data-switch", "0"), capture_output=True)

    has_vo = bool(vo.any())
    # with narration: music sits far below the voice and ducks hard while someone speaks
    duck = "[mu][vo1]sidechaincompress=threshold=0.01:ratio=20:attack=10:release=600:makeup=1[md]" if has_vo else "[mu]anull[md]"
    filt = ";".join([
        f"[1:a]aresample=44100,volume={0.32 if has_vo else 0.9}[mu]",
        ("[3:a]aresample=44100,highpass=f=100,equalizer=f=2500:t=q:w=1.2:g=4,volume=2.4,asplit=2[vo1][vo2]") if has_vo else "[3:a]aresample=44100[vo2]",
        duck,
        f"[2:a]aresample=44100,volume={0.5 if has_vo else 0.9}[fx]",
        "[md][fx][vo2]amix=inputs=3:normalize=0,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.2:LRA=10[aout]",
    ])
    out = HERE / f"getirtrend-{name}.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(frames / "f%05d.png"),
        "-i", str(music), "-i", str(wd / "sfx.wav"), "-i", str(wd / "vo.wav"), "-filter_complex", filt,
        "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart", str(out))
    print("wrote", out, flush=True)

"""Builds the GetirTrend promo videos: Turkish voiceover (Piper TTS) -> scene timings ->
frame capture (Playwright) -> music + voice mix -> MP4.

Usage: python3 build.py <voice.onnx> <workDir> [page.html ...]
Voice used: Piper tr_TR "fahrettin" (CC0).
"""
import json, os, re, subprocess, sys, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD, TAIL = 0.45, 0.55          # seconds of silence before / after each voice line
VOICES = sys.argv[1]
WORK = Path(sys.argv[2]); WORK.mkdir(parents=True, exist_ok=True)
PAGES = [Path(p) for p in sys.argv[3:]] or sorted(HERE.glob("v*.html"))
MUSIC = {"v1": (104, 1), "v2": (118, 2), "v3": (112, 3)}  # bpm, seed per video


def run(*cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def wav_dur(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


for page in PAGES:
    name = page.stem
    key = name[:2]
    lines = re.findall(r'class="scene"[^>]*data-voice="([^"]+)"', page.read_text(encoding="utf-8"))
    wd = WORK / name; wd.mkdir(exist_ok=True)
    clips, durs = [], []
    for i, text in enumerate(lines):
        clip = wd / f"vo{i}.wav"
        if not clip.exists():  # cache: Piper output varies run to run, keep timings stable
          run(sys.executable, "-m", "piper", "-m", VOICES, "-f", str(clip), "--length-scale", "1.08",
            "--sentence-silence", "0.25", input=text.encode(), capture_output=True)
        d = wav_dur(clip)
        clips.append(clip)
        durs.append(round(max(3.0, LEAD + d + TAIL), 3))
    durs[-1] += 0.6
    total = sum(durs) + 0.8
    print(name, "scene durations:", durs, "total:", round(total, 2))

    frames = wd / "frames"
    if not (os.environ.get("REUSE_FRAMES") and frames.exists()):
        run("rm", "-rf", str(frames))
        run("node", str(HERE / "render.js"), str(page), str(frames), json.dumps(durs))

    bpm, seed = MUSIC.get(key, (110, 0))
    music = wd / "music.wav"
    run(sys.executable, str(HERE / "music.py"), str(music), str(total), str(bpm), str(seed))

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
    filters.append("[duck][vo2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[aout]")
    out = HERE / f"getirtrend-{name}.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(frames / "f%05d.png"),
        *inputs, "-i", str(music), "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-t", f"{total:.3f}", "-movflags", "+faststart", str(out))
    print("wrote", out)

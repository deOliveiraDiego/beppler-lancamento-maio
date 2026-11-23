#!/usr/bin/env python3
"""Renderiza render/index.html quadro a quadro (render(t)) no Chrome e codifica com ffmpeg.

Uso:
  uv run --with playwright python -I render.py --snap 3,12,40      # quadros soltos em build/snap_*.jpg
  uv run --with playwright python -I render.py --video build/sem-audio.mp4 [--fps 30] [--workers 4]
"""
import asyncio, json, os, re, subprocess, sys
from playwright.async_api import async_playwright

# Pasta do filme (roteiro.json, cenas/, render/, build/). O conteúdo fica fora do git
# (docs/conta/video, porque tem números do cliente); aqui só o código.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.environ.get("VIDEO_DIR", os.path.join(RAIZ, "docs", "conta", "video"))
PAGE = "file://" + os.path.join(AQUI, "render", "index.html")

def total():
    s = open(os.path.join(AQUI, "render", "timeline.js")).read()
    return json.loads(re.search(r"=\s*(\{.*\});", s, re.S).group(1))["total"]

async def abrir(pw):
    b = await pw.chromium.launch(channel="chrome", args=["--disable-gpu", "--force-color-profile=srgb"])
    p = await b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    await p.goto(PAGE); await p.evaluate("document.fonts.ready"); await p.wait_for_timeout(300)
    return b, p

async def snaps(ts):
    async with async_playwright() as pw:
        b, p = await abrir(pw)
        for t in ts:
            await p.evaluate(f"render({t})")
            await p.screenshot(path=os.path.join(AQUI, "build", f"snap_{t:06.1f}.jpg"), type="jpeg", quality=85)
        await b.close()

async def faixa(pw, i0, i1, fps, out):
    b, p = await abrir(pw)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(i0, i1):
        await p.evaluate(f"render({i / fps})")
        ff.stdin.write(await p.screenshot(type="jpeg", quality=93))
        if (i - i0) % 300 == 0: print(f"  {out}: {i - i0}/{i1 - i0}", flush=True)
    ff.stdin.close(); ff.wait(); await b.close()

async def video(out, fps, workers):
    n = int(total() * fps); step = -(-n // workers)
    parts = [os.path.join(AQUI, "build", f"parte_{k}.mp4") for k in range(workers)]
    async with async_playwright() as pw:
        await asyncio.gather(*[faixa(pw, k * step, min(n, (k + 1) * step), fps, parts[k]) for k in range(workers)])
    lst = os.path.join(AQUI, "build", "partes.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    print("vídeo:", out)

if __name__ == "__main__":
    a = sys.argv
    os.makedirs(os.path.join(AQUI, "build"), exist_ok=True)
    if "--snap" in a:
        asyncio.run(snaps([float(x) for x in a[a.index("--snap") + 1].split(",")]))
    else:
        fps = int(a[a.index("--fps") + 1]) if "--fps" in a else 30
        w = int(a[a.index("--workers") + 1]) if "--workers" in a else 4
        asyncio.run(video(os.path.join(AQUI, a[a.index("--video") + 1]), fps, w))

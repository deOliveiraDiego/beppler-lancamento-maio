#!/usr/bin/env python3
"""Monta a linha do tempo a partir das falas, a pista de voz e a mixagem com a trilha.

Uso: uv run --with numpy python -I ferramentas/video/montagem.py [--estimar]   (VIDEO_DIR muda a pasta do filme)
Gera: render/timeline.js, build/voz.wav, build/mix.wav
--estimar: falas que ainda não existem entram com duração estimada (para testar o render).
"""
import json, os, subprocess, sys, wave
import numpy as np

# Pasta do filme (roteiro.json, cenas/, render/, build/). O conteúdo fica fora do git
# (docs/conta/video, porque tem números do cliente); aqui só o código.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.environ.get("VIDEO_DIR", os.path.join(RAIZ, "docs", "conta", "video"))
SR = 44100
INTRO, GAP, GAP_MESMO, GAP_CENA, OUTRO = 1.2, .38, .22, 1.1, 4.5

def ler_wav(p):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def main():
    estimar = "--estimar" in sys.argv
    r = json.load(open(os.path.join(AQUI, "roteiro.json")))
    os.makedirs(os.path.join(AQUI, "build"), exist_ok=True)
    t = INTRO; cenas = {}; clips = []
    for ci, c in enumerate(r["cenas"]):
        if ci: t += GAP_CENA
        f = os.path.join(AQUI, "cenas", f"{c['id']}.wav")
        a = ler_wav(f)
        nz = np.where(np.abs(a) > 0.01)[0]
        a = a[max(0, nz[0] - 800): nz[-1] + 2400]
        d = len(a) / SR
        # pausas: trechos de 160 ms ou mais abaixo do limiar
        hop = int(.01 * SR); e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        quiet = e < .012; gaps = []; i = 0
        while i < len(quiet):
            if quiet[i]:
                j = i
                while j < len(quiet) and quiet[j]: j += 1
                if (j - i) * .01 >= .16: gaps.append(((i + j) / 2 * .01, (j - i) * .01))
                i = j
            else: i += 1
        # fronteiras esperadas pelo tamanho do texto; casa cada uma com a pausa mais próxima
        n = len(c["falas"]); tam = np.cumsum([len(x[1]) for x in c["falas"]]); tam = tam / tam[-1]
        bounds = []; usados = set()
        for k in range(n - 1):
            alvo = tam[k] * d
            cand = [(abs(g[0] - alvo) - .4 * g[1], gi) for gi, g in enumerate(gaps) if gi not in usados and (not bounds or g[0] > bounds[-1] + .5)]
            if cand:
                _, gi = min(cand); usados.add(gi); bounds.append(gaps[gi][0])
            else:
                bounds.append(alvo)
        cortes = [0.0] + bounds + [d]
        linhas = [[round(t + cortes[k], 3), round(t + cortes[k + 1], 3)] for k in range(n)]
        clips.append((t, a))
        cenas[c["id"]] = {"start": round(t, 3), "end": round(t + d, 3), "lines": linhas}
        t += d
    total = t + OUTRO
    tl = {"total": round(total, 3), "scenes": cenas}
    open(os.path.join(AQUI, "render", "timeline.js"), "w").write("window.TL = " + json.dumps(tl) + ";\n")
    print(f"duração total: {total:.1f}s")
    for k, v in cenas.items(): print(f"  {k}: {v['start']:6.1f} → {v['end']:6.1f}")
    # pista de voz
    N = int((total + 1) * SR); voz = np.zeros(N, np.float32)
    for t0, a in clips:
        i = int(t0 * SR); voz[i:i + len(a)] += a[:N - i]
    # trilha composta na medida certa
    trilha = os.path.join(AQUI, "build", "trilha.wav")
    subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trilha.py"), f"{total:.2f}", trilha,
                    "--pad-em", f"{cenas['s1']['start']:.2f}", "--abre-em", f"{cenas['s4']['start']:.2f}"], check=True)
    mus = ler_wav(trilha); mus = np.pad(mus, (0, max(0, N - len(mus))))[:N]
    # ducking: a trilha abaixa ~12 dB sob a voz, sobe nos respiros
    env = np.abs(voz); k = int(.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = np.where(env > .004, 1.0, 0.0)
    duck = np.convolve(duck, np.ones(int(.6 * SR)) / int(.6 * SR), mode="same")
    gain = 10 ** ((-12 * duck) / 20)
    mix = voz * 1.0 + mus * 0.22 * gain
    mix /= max(1e-9, np.max(np.abs(mix))) / 0.9
    for nome, sig in (("voz.wav", voz), ("mix.wav", mix)):
        pcm = (np.clip(sig, -1, 1) * 32767).astype(np.int16)
        with wave.open(os.path.join(AQUI, "build", nome), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print("build/voz.wav e build/mix.wav prontos")

if __name__ == "__main__":
    main()

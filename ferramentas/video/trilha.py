#!/usr/bin/env python3
"""Trilha original do vídeo (composta em código, sem licença de terceiros).

Piano em arpejo, pad quente e baixo, 70 bpm, ré maior. Entra só o piano, o pad chega
depois do gancho, abre um pouco na solução e fecha num acorde longo.
Uso: python3 -I trilha.py <duracao_s> <saida.wav> [--pad-em 12] [--abre-em 130]
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 70.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# compassos de 2 barras cada: Dmaj9, Bm9, Gmaj7, A6sus4 (MIDI)
CHORDS = [
    [50, 57, 61, 64, 66, 69],   # D  A  C# E  F# A
    [47, 54, 57, 61, 62, 66],   # B  F# A  C# D  F#
    [43, 50, 54, 57, 59, 62],   # G  D  F# A  B  D
    [45, 52, 54, 57, 59, 64],   # A  E  F# A  B  E
]

def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na) ** 2
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

def piano_note(f, dur, vel):
    n = int(dur * SR); t = np.arange(n) / SR
    tone = (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 2.5)
            + .12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 4) + .05 * np.sin(2 * np.pi * 4.01 * f * t) * np.exp(-t * 6))
    e = np.exp(-t * 1.6) * (1 - np.exp(-t * 400))
    return vel * tone * e

def pad_chord(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            s += np.sin(2 * np.pi * ff * t + np.random.rand() * 6.28) + .25 * np.sin(2 * np.pi * 2 * ff * t)
    s /= (len(freqs) * 3)
    # vibrato de volume lento
    s *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t)
    return s * env_adsr(n, 1.8, 1.8)

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    # filtro de um polo, duas passadas
    for _ in range(2):
        acc = 0.0
        for i in range(len(x)):
            acc = (1 - a) * x[i] + a * acc
            y[i] = acc
        x = y.copy()
    return y

def reverb(x, secs=2.8, mix=.32):
    n = int(secs * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    ir = rng.standard_normal(n) * np.exp(-t * 3.2)
    ir[:int(.02 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n - 1; N = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]
    return (1 - mix) * x + mix * wet * 3

def main():
    dur = float(sys.argv[1]); out = sys.argv[2]
    pad_em = float(sys.argv[sys.argv.index("--pad-em") + 1]) if "--pad-em" in sys.argv else 12.0
    abre_em = float(sys.argv[sys.argv.index("--abre-em") + 1]) if "--abre-em" in sys.argv else dur * 0.6
    total = dur + 4.0
    N = int(total * SR)
    piano = np.zeros(N); pad = np.zeros(N); bass = np.zeros(N)
    np.random.seed(3)
    nbars = int(np.ceil(dur / BAR)) + 1
    pattern = [0, 2, 4, 3, 5, 2, 4, 1]          # arpejo em colcheias (índices do acorde)
    for b in range(nbars):
        t0 = b * BAR
        if t0 > dur - BAR * 0.5: break
        ch = CHORDS[(b // 2) % 4]
        # piano: arpejo em colcheias, mais esparso no começo
        for k, idx in enumerate(pattern):
            ts = t0 + k * BEAT / 2
            if ts >= dur: break
            if t0 < pad_em and k % 2: continue
            vel = 0.22 * (1.0 if k % 2 == 0 else 0.7) * (0.9 + 0.2 * np.random.rand())
            note = piano_note(hz(ch[idx] + 12), 2.4, vel)
            i = int(ts * SR); piano[i:i + len(note)] += note[:max(0, N - i)]
        # pad a partir do gancho, mais aberto depois de abre_em
        if t0 >= pad_em - BAR:
            p = pad_chord([hz(m) for m in ch[1:]], BAR + 1.8) * (0.16 if t0 < abre_em else 0.22)
            i = int(t0 * SR); pad[i:i + len(p)] += p[:max(0, N - i)]
            # baixo
            if t0 >= pad_em:
                n = int(BAR * SR); tt = np.arange(n) / SR
                bs = 0.18 * np.sin(2 * np.pi * hz(ch[0] - 12) * tt) * env_adsr(n, .05, .8)
                bass[i:i + n] += bs[:max(0, N - i)]
    # acorde final longo
    i = int(dur * SR)
    fin = pad_chord([hz(m) for m in CHORDS[0][1:]], 4.0) * 0.22
    pad[i - int(.5 * SR): i - int(.5 * SR) + len(fin)] += fin[:N - i + int(.5 * SR)]
    for m in CHORDS[0][2:5]:
        nt = piano_note(hz(m + 12), 4.0, .18); piano[i:i + len(nt)] += nt[:N - i]
    pad = np.convolve(pad, np.ones(24) / 24, mode="same")   # amacia agudos do pad
    mix = piano * 0.9 + pad + bass
    mix = reverb(mix)
    fade = env_adsr(N, 2.5, 3.5); mix *= fade
    mix /= np.max(np.abs(mix)) + 1e-9; mix *= 0.85
    st = np.stack([mix, np.roll(mix, int(.011 * SR)) * 0.97], axis=1)   # leve abertura estéreo
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"trilha: {total:.1f}s -> {out}")

if __name__ == "__main__":
    main()

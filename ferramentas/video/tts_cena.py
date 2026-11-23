#!/usr/bin/env python3
"""Uma cena por pedido, duas vozes em diálogo (Gemini TTS multi-falante).

Uso: python3 -I tts_cena.py roteiro.json cenas/
Cota gratuita: 10 pedidos por dia por modelo; o filme usa 7.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, wave

K = os.environ["GEMINI_API_KEY"]
MODELO = os.environ.get("TTS_MODEL", "gemini-3.1-flash-tts-preview")
NOMES = {"A": "Ana", "B": "Beto"}

r = json.load(open(sys.argv[1])); out = sys.argv[2]
os.makedirs(out, exist_ok=True)
for c in r["cenas"]:
    f = os.path.join(out, f"{c['id']}.wav")
    if os.path.exists(f):
        continue
    texto = "\n".join(f"{NOMES[q]}: {t}" for q, t in c["falas"])
    body = {"contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
                {"speaker": NOMES[q], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": r["vozes"][q]}}} for q in ("A", "B")]}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": K})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            d = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{c['id']}: erro {e.code} {e.read()[:300]}")
    pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    with wave.open(f, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print(f"{c['id']}: {len(pcm) / 48000:.1f}s", flush=True)
    time.sleep(8)

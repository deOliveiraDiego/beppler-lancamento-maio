# Vídeo explicativo com duas vozes

Pipeline usado no vídeo "Sofia na Black" (nov/2026). O código fica aqui; o conteúdo do filme
(roteiro com números do cliente, cenas em HTML/JS, áudios e renders) fica em `docs/conta/video/`,
fora do git, porque o repo é público. Outra pasta: `VIDEO_DIR=/caminho`.

| Script | O que faz |
|---|---|
| `tts_cena.py roteiro.json cenas/` | Uma cena por pedido no Gemini TTS, duas vozes em diálogo. Cota gratuita: 10 pedidos/dia por modelo. Mande só o texto: instrução de estilo no prompt é lida em voz alta. |
| `trilha.py <segundos> <saida.wav>` | Trilha original (piano, pad e baixo, 70 bpm), sem licença de terceiros. |
| `montagem.py` | Corta as falas pelas pausas, gera `render/timeline.js`, a pista de voz e a mixagem com ducking. |
| `render.py --snap 3,40` / `--video build/x.mp4` | Captura `render/index.html` quadro a quadro (`render(t)`) no Chrome e codifica com ffmpeg. |

Requisitos: `uv`, `ffmpeg`, Google Chrome, `GEMINI_API_KEY` no ambiente.

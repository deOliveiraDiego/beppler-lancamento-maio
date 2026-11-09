"""Envia mensagem avulsa como a Sofia (número do Unnichat) e grava na memória dela.

Uso:
    python3 -I enviar-avulsa.py <telefone> "<mensagem>"

- telefone: só dígitos, com DDI, igual ao sessionId da Sofia (ex.: 5511999999999).
- Parágrafos separados por linha em branco viram mensagens separadas (como a Sofia faz).
- Depois do envio, grava a mensagem inteira como `ai` em n8n_chat_histories_tpoc_setembro,
  pelo workflow "Sofia Black — Memória de Mensagem Avulsa" (OI3j2L5BhVEKwQvZ).
- Teste primeiro no número do Diego.
"""
import json
import sys
import time
import urllib.request

UNNICHAT = "https://unnichat.com.br/a/start/APhog6fll206OfS47maU"
MEMORIA = "https://connect.fernandabeppler.com.br/webhook/sofia-black-memoria-avulsa-k8r3v9"


def post(url, data):
    req = urllib.request.Request(url, json.dumps(data).encode(), {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    phone, texto = sys.argv[1], sys.argv[2].replace("\\n", "\n")
    partes = [p for p in texto.split("\n\n") if p.strip()]
    for i, parte in enumerate(partes):
        r = post(UNNICHAT, {"phone": phone, "response": parte})
        print(f"envio {i + 1}/{len(partes)}: {r}", flush=True)
        if i < len(partes) - 1:
            time.sleep(4)
    m = post(MEMORIA, {"phone": phone, "mensagem": texto})
    print(f"memória: id {m[0]['id']}", flush=True)


if __name__ == "__main__":
    main()

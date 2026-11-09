#!/usr/bin/env python3
"""Roda conversas multi-turno contra a Sofia (prod ou teste) e imprime a transcrição.
Uso: python3 -I personas.py <prod|teste> <rodada> [persona ...]
"""
import json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

URLS = {
    "prod": "https://connect.fernandabeppler.com.br/webhook/7b75b4cd-032c-4167-a9f1-d2f3e41cace2",
    "teste": "https://connect.fernandabeppler.com.br/webhook/3550ea5b-86f4-4f8d-aff9-13db4d251cf4/chat",
}

# Personas de VENDA (seguras em prod: não devem encaminhar).
VENDA = {
    "curiosa": ["Oi, vi o story da Fê. O que é essa Black Vitalícia?", "E quanto custa?", "Tem bônus pra quem entrar agora?"],
    "aluna": ["Oi Sofia! Já sou aluna do TPOC. Quero a Vitalícia, me manda o link", "Qual o valor pra aluna?"],
    "grupovip": ["Quero participar da black vitalícia das bruxas ✨", "Mas quando abre? Que horas é a live?"],
    "boleto": ["Oi, dá pra pagar no boleto?", "Não sou aluna ainda", "Quantas parcelas?"],
    "urgencia": ["Até quando fica aberto?", "Posso pensar e comprar semana que vem?"],
}
# Personas que podem ENCAMINHAR (rodar só em teste).
HANDOFF = {
    "golden": ["Sou Golden, tenho a vitalícia antiga. Tenho preço especial?"],
    "acesso": ["Comprei ontem e não consigo acessar o curso, aparece bloqueado"],
    "senhavip": ["Não recebi a senha do grupo VIP, o que faço?"],
}

def send(env, session, msg):
    body = {"sessionId": session, "chatInput": msg}
    if env == "teste":
        body["action"] = "sendMessage"
    req = urllib.request.Request(URLS[env], data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=150) as r:
            data = json.loads(r.read().decode() or "{}")
    except Exception as e:  # noqa: BLE001
        return f"[ERRO] {e}"
    return data.get("output") or data.get("text") or json.dumps(data, ensure_ascii=False)

def run(env, rodada, nome, falas):
    session = f"claude-{rodada}-{nome}-{int(time.time())}"
    out = [f"### {env} · {rodada} · {nome}  (session {session})"]
    for f in falas:
        out.append(f"👤 {f}")
        out.append(f"🔮 {send(env, session, f)}")
    return "\n".join(out)

if __name__ == "__main__":
    env, rodada, *nomes = sys.argv[1:]
    todas = {**VENDA, **HANDOFF}
    if env == "prod":
        todas = VENDA
    escolhidas = {n: todas[n] for n in (nomes or todas)}
    with ThreadPoolExecutor(max_workers=5) as ex:
        res = list(ex.map(lambda kv: run(env, rodada, *kv), escolhidas.items()))
    print("\n\n".join(res))

#!/usr/bin/env python3
"""Classifica e resume as conversas capturadas do Unnichat.

Uso:
  set -a; . ~/.claude/secrets/deoliveiratech.env; set +a
  python3 -I analise.py --entrada docs/conta/unnichat --desde 2026-09-21 --ate 2026-11-23

Quem mandou cada mensagem (a API só diz contact / user / platform):
  aluna     senderBy=contact
  sofia     senderBy=user e o texto bate com uma resposta da Sofia no banco
  automacao senderBy=platform, tipos de fluxo (template, button, cta-url...)
            ou texto idêntico enviado a 5+ contatos (disparo/fluxo)
  equipe    o resto do lado da escola: texto escrito por uma atendente

Imprime só agregados (sem nome, telefone ou texto) e grava classificadas.jsonl na entrada.
"""
import argparse, json, os, re, subprocess, statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

BRT = timezone(timedelta(hours=-3))
TIPOS_AUTOMACAO = {"template", "button", "cta-url", "list", "interactive", "info"}
TEMAS = [
    ("Acesso, login e plataforma", r"acess|login|logar|senha|plataforma|cademi|entrar|n[aã]o consigo|bloquead|liberad"),
    ("Aulas, grupos e links", r"\baula|grupo|link|live|ao vivo|grava[cç]|replay|v[ií]deo|comunidade|circle"),
    ("Pagamento, boleto e parcelas", r"boleto|pix|parcel|pagamento|pagar|paguei|cart[aã]o|cobran|fatura|vencimento"),
    ("Cancelamento e reembolso", r"cancel|reembols|estorn|devolu|desist"),
    ("Certificado e cadastro", r"certificad|cadastr|e-?mail|nome completo|cpf|dados"),
    ("Compra e oferta", r"compr|valor|pre[cç]o|desconto|black|vital[ií]c|oferta|lote|golden"),
]

def norm(s):
    return re.sub(r"\W+", "", (s or "").lower())

# A memória da Sofia da Black só tem horário a partir de 23/09 16:34 UTC, e as respostas
# de 21 a 23/09 se perderam no restore de 08/11. Antes disso, "user" sem par no banco
# pode ser Sofia ou equipe: fica "indefinido" e sai das métricas da equipe.
SEM_MEMORIA_ATE = datetime(2026, 9, 23, 16, 34, tzinfo=timezone.utc)

def chave_massa(s):
    """Texto sem o vocativo inicial ("Carla, que bom…" → "que bom…"), para achar disparos personalizados."""
    s = re.sub(r"^\s*(ol[aá]|oi|bom dia|boa tarde|boa noite)?[\s,!]*[^,!?.\n]{1,25}[,!]\s*", "", s or "", flags=re.I)
    return norm(s)[:80]

def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(BRT)

def comercial(d):
    return d.weekday() < 5 and 9 <= d.hour < 18

def sofia_textos():
    url = os.environ.get("BEPPLER_DATABASE_URL")
    if not url:
        return set()
    out = set()
    for t in ("n8n_chat_histories_tpoc_setembro", "n8n_chat_histories_sofia", "n8n_chat_histories_wtp", "n8n_chat_histories_sofia_wtp"):
        r = subprocess.run(["psql", url, "-At", "-c", f"SELECT message->>'content' FROM {t} WHERE message->>'type'='ai'"],
                           capture_output=True, text=True)
        for linha in r.stdout.split("\n"):
            k = norm(linha)
            if len(k) >= 20:
                out.add(k)
    return out

def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p * (len(xs) - 1))))] if xs else None

def fmt_min(m):
    if m is None: return "—"
    return f"{m:.0f} min" if m < 120 else f"{m/60:.1f} h"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--desde", default="2026-09-21")
    ap.add_argument("--ate", default="2026-11-23")
    a = ap.parse_args()
    ini = datetime.fromisoformat(a.desde).replace(tzinfo=BRT)
    fim = datetime.fromisoformat(a.ate).replace(tzinfo=BRT) + timedelta(days=1)

    msgs = [json.loads(l) for l in open(os.path.join(a.entrada, "mensagens.jsonl"))]
    contatos = [json.loads(l) for l in open(os.path.join(a.entrada, "contatos.jsonl"))]
    vistos = set()
    msgs = [m for m in msgs if not (m["id"] in vistos or vistos.add(m["id"]))]

    sofia = sofia_textos()
    sofia_blob = "|".join(sofia)
    sofia = {s[:80] for s in sofia}
    # textos idênticos do lado da escola enviados a muitos contatos = fluxo/disparo
    por_texto = defaultdict(set)
    for m in msgs:
        if m.get("senderBy") == "user" and m.get("message"):
            por_texto[norm(m["message"])[:80]].add(m["contactId"])
            por_texto[chave_massa(m["message"])].add(m["contactId"])
    massivo = {k for k, cs in por_texto.items() if len(cs) >= 5 and len(k) >= 10}

    def quem(m):
        s = m.get("senderBy")
        if s == "contact": return "aluna"
        if s == "platform": return "automacao"
        k = norm(m.get("message"))[:80]
        if m.get("type") in TIPOS_AUTOMACAO: return "automacao"
        if not k: return "automacao" if m.get("type") in ("video", "audio", "image", "document") else "equipe"
        # a Sofia manda a resposta em balões; cada balão é um trecho de uma resposta gravada no banco
        if k in sofia or (len(k) >= 20 and k[:60] in sofia_blob): return "sofia"
        if k in massivo or chave_massa(m.get("message")) in massivo: return "automacao"
        if dt(m["date"]) < SEM_MEMORIA_ATE: return "indefinido"
        return "equipe"

    for m in msgs:
        m["quem"] = quem(m)
        m["_dt"] = dt(m["date"])
    with open(os.path.join(a.entrada, "classificadas.jsonl"), "w") as f:
        for m in msgs:
            f.write(json.dumps({k: v for k, v in m.items() if k != "_dt"}, ensure_ascii=False) + "\n")

    per = [m for m in msgs if ini <= m["_dt"] < fim]
    achados = sum(1 for c in contatos if c.get("achado"))
    print(f"Telefones consultados: {len(contatos)} · achados no Unnichat: {achados}")
    print(f"Mensagens capturadas: {len(msgs)} (histórico todo) · no período {a.desde} a {a.ate}: {len(per)}")
    print("Por remetente no período:", dict(Counter(m["quem"] for m in per)))

    eq = [m for m in per if m["quem"] == "equipe"]
    contatos_eq = {m["contactId"] for m in eq}
    print(f"\nEquipe: {len(eq)} mensagens escritas, para {len(contatos_eq)} contatos")
    print("Equipe por mês:", dict(sorted(Counter(m["_dt"].strftime("%Y-%m") for m in eq).items())))
    print("Contatos atendidos pela equipe por mês:", {k: len(v) for k, v in sorted(
        {mes: {m["contactId"] for m in eq if m["_dt"].strftime("%Y-%m") == mes} for mes in {m["_dt"].strftime("%Y-%m") for m in eq}}.items())})
    print(f"Equipe em horário comercial (seg-sex 9h-18h): {sum(comercial(m['_dt']) for m in eq)}/{len(eq)}")

    # tempo de resposta: primeira mensagem da aluna sem resposta → primeira resposta (equipe ou sofia)
    por_contato = defaultdict(list)
    for m in sorted(msgs, key=lambda x: x["_dt"]):
        por_contato[m["contactId"]].append(m)
    t_eq, t_sofia, sem_resp = [], [], 0
    for cid, ms in por_contato.items():
        aberta = None
        for m in ms:
            if m["quem"] == "aluna":
                if aberta is None: aberta = m["_dt"]
            elif m["quem"] in ("equipe", "sofia") and aberta is not None:
                if ini <= aberta < fim:
                    (t_eq if m["quem"] == "equipe" else t_sofia).append((m["_dt"] - aberta).total_seconds() / 60)
                aberta = None
        if aberta is not None and ini <= aberta < fim:
            sem_resp += 1
    for nome, xs in (("equipe", t_eq), ("Sofia", t_sofia)):
        if xs:
            print(f"Tempo até a resposta da {nome}: n={len(xs)} mediana {fmt_min(statistics.median(xs))} · p75 {fmt_min(pct(xs,.75))} · p90 {fmt_min(pct(xs,.9))}"
                  f" · ≤1h {sum(x<=60 for x in xs)/len(xs):.0%} · >24h {sum(x>1440 for x in xs)/len(xs):.0%}")
    print(f"Conversas cuja última mensagem da aluna ficou sem resposta (no período): {sem_resp}")

    # temas das mensagens das alunas que receberam resposta da equipe
    al = [m for m in per if m["quem"] == "aluna" and m["contactId"] in contatos_eq and len(norm(m.get("message"))) >= 15]
    tema = Counter()
    for m in al:
        t = next((n for n, rx in TEMAS if re.search(rx, m["message"].lower())), "Outros")
        tema[t] += 1
    print("\nTemas das mensagens das alunas atendidas pela equipe:", dict(tema.most_common()))

    # repetição nas respostas da equipe
    chaves = Counter(norm(m.get("message"))[:50] for m in eq if m.get("message"))
    rep = sum(c for k, c in chaves.items() if c >= 3 and len(k) >= 15)
    print(f"Respostas da equipe repetidas 3+ vezes (mesmo começo): {rep}/{len(eq)}")

    at = Counter((c.get("atendente") or {}).get("id") for c in contatos if c.get("achado"))
    print("Contatos por atendente responsável (ids anonimizados):", {f"atendente {i+1}" if k else "sem atendente": v for i, (k, v) in enumerate(at.most_common())})

if __name__ == "__main__":
    main()

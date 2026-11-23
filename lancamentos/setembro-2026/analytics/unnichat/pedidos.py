#!/usr/bin/env python3
"""Agrupa as conversas em pedidos (episódios) e classifica o assunto.

Pedido = sequência de mensagens da aluna num contato, até 12h sem nova mensagem dela.
Assunto = primeira regra que bate no texto da aluna no episódio (ordem importa).
Quem respondeu = quem do lado da escola escreveu depois, dentro do episódio.
Uso: python3 -I pedidos.py docs/conta/unnichat/classificadas.jsonl [--amostra TEMA]
"""
import json, re, sys, random
from collections import Counter, defaultdict
from datetime import datetime, timedelta

ASSUNTOS = [
    ("golpe", r"fake|fingindo|se passando|golpe|clonad|https?://\S+\.(buzz|ru|top|xyz)|testa a[ií]|recebi r\$ ?300|amigo, seu apoio|resgata|presente de anivers"),
    ("corrente_spam", r"instagram\.com/(reel|p)/|threads\.com|tiktok\.com|facebook\.com/share|temu\.com|youtu\.?be|bolsonar|\blula\b|tarc[ií]sio|elei[cç]|\bvot(e|ar|o)\b|miliciano|golpista|debate|assine"),
    ("entrada_grupo_vip", r"quero participar|quero entrar no grupo|grupo vip|lista vip|quero o presente|participar da black"),
    ("cancelamento_reembolso", r"cancel|reembols|estorn|devolu[cç]|desist|arrependi"),
    ("acesso_plataforma", r"c[oó]digo|google|verifica[cç][aã]o|acess|login|logar|senha|plataforma|cademi|n[aã]o consigo (entrar|abrir|ver|assistir)|bloquead|n[aã]o (liberou|liberad)|libera[rç]|meu curso|meus cursos|[aá]rea de membros|app\b|aplicativo"),
    ("aula_live_grupo", r"\baula|magna|\blive\b|ao vivo|grava[cç]|replay|link d[ao] (grupo|aula|live|zoom|mentoria)|grupo|comunidade|circle|canal|zoom|mentoria|encontro|treinamento|sala"),
    ("pagamento", r"boleto|pix|parcel|pagamento|pagar|paguei|pago\b|cart[aã]o|cobran|fatura|vencimento|comprovante|entrada de|segunda via|2[ªa] via"),
    ("certificado_cadastro", r"certificad|cadastr|trocar (o )?e-?mail|mudar (o )?e-?mail|nome completo|\bcpf\b|titular|presente(ada|ar)|meus dados"),
    ("golden_beneficios", r"golden|vital[ií]cia (antiga|anterior)|j[aá] sou vital|brinde|\bkit\b|deck|baralho|retiro|buscador"),
    ("compra_oferta", r"compr|valor|pre[cç]o|quanto (custa|fica|é)|desconto|black|vital[ií]c|oferta|lote|como (fa[cç]o|funciona)|link|inscri|vaga|quero"),
    ("espiritual_pessoal", r"tarot|tar[oô]|leitura|consulta|ritual|signo|mapa|astrolog|feiti|magia|energia|sonh|orix|santo|vela|lua"),
    ("falar_com_fe", r"falar com|carlos|fernanda|\bf[eê]\b|falar com (ela|a f)"),
]
NOME = re.compile(r"^\s*[A-ZÀ-Ú][\wÀ-ú'.]{1,20}(\s+[A-ZÀ-Úa-zà-ú][\wÀ-ú'.]{1,20}){0,3}\s*$")
CURTO = re.compile(r"^\W*(sim|n[aã]o|ok|okay|oi+|ol[aá]|bom dia|boa (tarde|noite)|obrigad[ao]|gratid[aã]o|am[eé]m|top|blz|beleza|[👍❤🙏✨😊🥰]+)\W*$", re.I)

def dt(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))

def main():
    arq = sys.argv[1]
    amostra = sys.argv[sys.argv.index("--amostra") + 1] if "--amostra" in sys.argv else None
    ms = [json.loads(l) for l in open(arq)]
    ms.sort(key=lambda m: m["date"])
    por = defaultdict(list)
    for m in ms: por[m["contactId"]].append(m)
    pedidos = []
    for cid, l in por.items():
        ep = None
        for m in l:
            if m["date"] < "2026-09-21" or m["date"] >= "2026-11-24": continue
            if m["quem"] == "aluna":
                if ep is None or dt(m["date"]) - ep["ultima"] > timedelta(hours=12):
                    ep = {"cid": cid, "inicio": m["date"], "ultima": dt(m["date"]), "texto": [], "resp": Counter(), "t1": {}}
                    pedidos.append(ep)
                ep["ultima"] = dt(m["date"])
                if m.get("message"): ep["texto"].append(m["message"])
            elif ep is not None and m["quem"] in ("sofia", "equipe", "automacao", "indefinido") and m["type"] != "info":
                ep["resp"][m["quem"]] += 1
                ep["t1"].setdefault(m["quem"], (dt(m["date"]) - dt(ep["inicio"])).total_seconds() / 60)
    # texto idêntico mandado por 10+ contatos = clique em botão de fluxo (ex.: "Acessar informações")
    por_txt = defaultdict(set)
    for p in pedidos:
        for t in p["texto"]: por_txt[t.strip().lower()].add(p["cid"])
    botoes = {t for t, cs in por_txt.items() if len(cs) >= 10}
    tot = Counter(); quem = defaultdict(Counter); ex = defaultdict(list)
    for p in pedidos:
        livres = [t for t in p["texto"] if t.strip().lower() not in botoes and not CURTO.match(t) and not NOME.match(t)]
        txt = " ".join(livres).lower()
        if not txt.strip():
            a = "so_botao_ou_cumprimento"
        else:
            a = next((n for n, rx in ASSUNTOS if re.search(rx, txt)), "outros")
        p["assunto"] = a
        tot[a] += 1
        r = "equipe" if p["resp"]["equipe"] else "sofia" if p["resp"]["sofia"] else "indefinido" if p["resp"]["indefinido"] else "automacao" if p["resp"]["automacao"] else "ninguem"
        quem[a][r] += 1
        ex[a].append(" ‖ ".join(livres or p["texto"])[:160].replace("\n", " "))
    print("Textos de botão detectados:", sorted(botoes)[:15])
    print(f"Pedidos (episódios) entre 21/09 e 23/11: {len(pedidos)} em {len({p['cid'] for p in pedidos})} contatos\n")
    print(f"{'assunto':26} {'n':>5}  respondido por (equipe / sofia / automação / indefinido / ninguém)")
    for a, n in tot.most_common():
        q = quem[a]
        print(f"{a:26} {n:5}  {q['equipe']:4} / {q['sofia']:4} / {q['automacao']:4} / {q['indefinido']:4} / {q['ninguem']:4}")
    if "--dump" in sys.argv:
        sel=[p for p in pedidos if p["assunto"] not in ("so_botao_ou_cumprimento","corrente_spam") and (p["resp"]["equipe"] or not any(p["resp"][k] for k in ("sofia","indefinido")))]
        out=sys.argv[sys.argv.index("--dump")+1]
        with open(out,"w") as f:
            for i,p in enumerate(sel):
                f.write(json.dumps({"i":i,"cid":p["cid"],"inicio":p["inicio"],"auto":p["assunto"],"resp":dict(p["resp"]),"t1":p["t1"],"texto":" ‖ ".join(p["texto"])[:400]},ensure_ascii=False)+"\n")
        print("dump:",len(sel),"pedidos em",out)
    if amostra:
        random.seed(7)
        print(f"\nAMOSTRA {amostra}:")
        for t in random.sample(ex[amostra], min(25, len(ex[amostra]))): print("  -", t)

if __name__ == "__main__":
    main()

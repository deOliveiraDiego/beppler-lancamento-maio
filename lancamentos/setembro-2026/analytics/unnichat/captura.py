#!/usr/bin/env python3
"""Captura o histórico de conversas do Unnichat (EAM) para uma lista de telefones.

Uso:
  set -a; . ~/.claude/secrets/deoliveiratech.env; set +a
  python3 -I captura.py --telefones telefones.txt --saida docs/conta/unnichat

Lê BEPPLER_UNNICHAT_TOKEN e BEPPLER_UNNICHAT_BASE_URL do ambiente.
Grava contatos.jsonl e mensagens.jsonl (com PII). A saída nunca entra no git.
Retoma de onde parou: telefones já em contatos.jsonl são pulados.
Respeita o limite da API (~150 chamadas/min).
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

B = os.environ["BEPPLER_UNNICHAT_BASE_URL"].rstrip("/")
T = os.environ["BEPPLER_UNNICHAT_TOKEN"]
PAUSA = 0.45  # ~133 chamadas/min
_ult = 0.0

def call(method, path, body=None, tentativas=4):
    global _ult
    for i in range(tentativas):
        espera = PAUSA - (time.time() - _ult)
        if espera > 0: time.sleep(espera)
        _ult = time.time()
        req = urllib.request.Request(B + path, method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {T}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code == 429 or e.code >= 500:
                time.sleep(20 * (i + 1)); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            time.sleep(10 * (i + 1))
    raise RuntimeError(f"falhou: {method} {path}")

def variantes(fone):
    d = re.sub(r"\D", "", fone)
    if not d.startswith("55") and len(d) in (10, 11): d = "55" + d
    vs = [d]
    if d.startswith("55") and len(d) == 13 and d[4] == "9": vs.append(d[:4] + d[5:])   # sem o nono dígito
    if d.startswith("55") and len(d) == 12: vs.append(d[:4] + "9" + d[4:])            # com o nono dígito
    return vs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--telefones", required=True, type=Path)
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--atribuicao", action="store_true", help="também busca a atendente responsável")
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=True)
    fc, fm = a.saida / "contatos.jsonl", a.saida / "mensagens.jsonl"
    feitos = set()
    if fc.exists():
        feitos = {json.loads(l)["telefone_origem"] for l in fc.open()}
    fones = [l.strip() for l in a.telefones.open() if l.strip()]
    pend = [f for f in dict.fromkeys(fones) if f not in feitos]
    print(f"{len(fones)} telefones, {len(feitos)} já feitos, {len(pend)} pendentes", flush=True)
    achados = msgs_total = 0
    with fc.open("a") as oc, fm.open("a") as om:
        for n, fone in enumerate(pend, 1):
            contato = None
            for v in variantes(fone):
                r = call("POST", "/contact/search", {"phone": v})
                if r and r.get("data"):
                    contato = r["data"][0]; break
            reg = {"telefone_origem": fone, "achado": bool(contato)}
            if contato:
                achados += 1
                msgs = (call("GET", f"/contact/{contato['id']}/messages") or {}).get("data") or []
                reg.update(contato=contato, n_mensagens=len(msgs))
                if a.atribuicao:
                    reg["atendente"] = (call("GET", f"/contact/{contato['id']}/assign") or {}).get("data")
                for m in msgs:
                    m["telefone_origem"] = fone
                    om.write(json.dumps(m, ensure_ascii=False) + "\n")
                msgs_total += len(msgs)
            oc.write(json.dumps(reg, ensure_ascii=False) + "\n"); oc.flush(); om.flush()
            if n % 25 == 0 or n == len(pend):
                print(f"{n}/{len(pend)} · achados {achados} · mensagens {msgs_total}", flush=True)

if __name__ == "__main__":
    main()

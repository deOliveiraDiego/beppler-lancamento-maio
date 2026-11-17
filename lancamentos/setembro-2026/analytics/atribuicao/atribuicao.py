#!/usr/bin/env python3
"""Atribuição de vendas à Sofia.

Cruza exports de venda (Guru, TMB, qualquer CSV) com as conversas da Sofia
(tabela de memória n8n no Postgres, ou um CSV exportado dela) e classifica
cada venda aprovada em:

  utm        — a venda chegou com a UTM da Sofia (utm_medium=ia / ia-vendas)
  link       — a pessoa recebeu link da Sofia antes de comprar (dentro da janela)
  conversa   — a pessoa conversou com a Sofia antes de comprar, sem link
  pos_compra — a primeira conversa foi depois da compra (suporte, não venda)
  sem_contato

Uso:
  python3 atribuicao.py --vendas guru.csv tmb.csv --conversas conversas.csv
  DATABASE_URL=postgres://... python3 atribuicao.py --vendas guru.csv --tabela n8n_chat_histories_tpoc_setembro

Saída (detalhe com telefone e e-mail) vai para --saida, que por padrão é
docs/conta/atribuicao/ (fora do git). Nunca versione a saída.

Só usa a biblioteca padrão do Python. Para ler do Postgres, precisa do psql.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

LINK_MARKERS = ("sndflw.com", "sendflow.pro", "clkdmg.site", "pay.tmb.com.br", "fernandabeppler.com.br/combo-black")
STATUS_OK = ("aprovad", "approved", "paid", "pago", "complet", "conclu", "finaliz")
STATUS_BAD = ("reemb", "refund", "cancel", "chargeback", "estorn", "expir", "recus", "abandon", "pendente", "aguardando", "waiting")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Cabeçalhos aceitos por campo, em ordem de preferência (sem acento, minúsculo).
COLUMNS = {
    "id": ["id da transacao", "transacao", "transaction id", "transaction", "codigo da venda", "codigo", "id venda", "id"],
    "telefone": ["telefone do comprador", "telefone", "celular", "whatsapp", "contact phone", "phone"],
    "email": ["email do comprador", "e-mail do comprador", "email", "e-mail", "contact email"],
    "status": ["status da venda", "status do pagamento", "status", "situacao"],
    "data": ["data de aprovacao", "data aprovacao", "approved at", "data do pagamento", "paid at", "data da venda", "data de criacao", "created at", "data"],
    "valor": ["valor liquido", "valor total", "valor da venda", "valor", "total", "amount", "price", "preco"],
    "produto": ["nome do produto", "produto", "product name", "product", "oferta", "offer"],
    "utm_medium": ["utm medium", "utm_medium"],
    "utm_campaign": ["utm campaign", "utm_campaign"],
    "utm_source": ["utm source", "utm_source"],
    "src": ["src", "sck", "origem"],
}


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    return re.sub(r"[\s_]+", " ", text.strip().lower())


def phone_key(raw: str | None) -> str | None:
    """DDD + últimos 8 dígitos. Tolera DDI 55 e o nono dígito faltando."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) >= 12 and digits.startswith("55"):
        digits = digits[2:]
    if len(digits) < 10:
        return None
    return digits[:2] + digits[-8:]


def parse_money(raw: str | None) -> float:
    s = re.sub(r"[^\d,.\-]", "", raw or "")
    if not s:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


DATE_FORMATS = ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d")


BRT = timedelta(hours=-3)


def parse_date(raw: str | None) -> datetime | None:
    """Data sem fuso fica como está (exports vêm em horário de Brasília).
    Data com fuso (Postgres manda +00) é convertida para Brasília."""
    s = (raw or "").strip()
    if not s:
        return None
    m = re.search(r"([+-])(\d{2}):?(\d{2})?$|Z$", s)
    offset = None
    if m and re.search(r"\d{2}:\d{2}", s):
        if m.group(0) == "Z":
            offset = timedelta(0)
        else:
            sign = 1 if m.group(1) == "+" else -1
            offset = sign * timedelta(hours=int(m.group(2)), minutes=int(m.group(3) or 0))
        s = s[: m.start()]
    s = re.sub(r"\.\d+$", "", s)
    for fmt in DATE_FORMATS:
        try:
            d = datetime.strptime(s, fmt)
            return d - offset + BRT if offset is not None else d
        except ValueError:
            continue
    return None


def read_csv(path: Path) -> list[dict[str, str]]:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    sample = text[:4096]
    delim = ";" if sample.count(";") > sample.count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def map_columns(headers: list[str], overrides: dict[str, str]) -> dict[str, str | None]:
    by_norm = {norm(h): h for h in headers}
    found: dict[str, str | None] = {}
    for field_name, candidates in COLUMNS.items():
        if overrides.get(field_name):
            found[field_name] = overrides[field_name]
            continue
        found[field_name] = None
        for cand in candidates:
            if cand in by_norm:
                found[field_name] = by_norm[cand]
                break
        if found[field_name] is None:  # casamento parcial: "utm_medium (venda)"
            for n, original in by_norm.items():
                if any(n.startswith(c) for c in candidates):
                    found[field_name] = original
                    break
    return found


@dataclass
class Sale:
    origem: str
    id: str
    telefone: str
    email: str
    status: str
    data: datetime | None
    valor: float
    produto: str
    utm: str
    classe: str = "sem_contato"
    sessao: str = ""


def status_ok(status: str) -> bool | None:
    s = norm(status)
    if not s:
        return None
    if any(b in s for b in STATUS_BAD):
        return False
    return any(o in s for o in STATUS_OK)


def load_sales(paths: list[Path], overrides: dict[str, str], warn) -> list[Sale]:
    sales: dict[str, Sale] = {}
    for path in paths:
        rows = read_csv(path)
        if not rows:
            warn(f"{path.name}: arquivo vazio")
            continue
        cols = map_columns(list(rows[0].keys()), overrides)
        missing = [k for k in ("telefone", "email", "status", "data", "valor") if not cols[k]]
        if missing:
            warn(f"{path.name}: não achei as colunas {', '.join(missing)}. Use --col-<campo> para indicar.")
        get = lambda r, k: (r.get(cols[k]) or "").strip() if cols[k] else ""
        for i, r in enumerate(rows):
            st = get(r, "status")
            ok = status_ok(st)
            if ok is False or (ok is None and cols["status"]):
                continue
            utm = " ".join(filter(None, (get(r, "utm_medium"), get(r, "utm_campaign"), get(r, "utm_source"), get(r, "src"))))
            sale = Sale(
                origem=path.name, id=get(r, "id") or f"{path.name}:{i}", telefone=get(r, "telefone"),
                email=get(r, "email").lower(), status=st, data=parse_date(get(r, "data")),
                valor=parse_money(get(r, "valor")), produto=get(r, "produto"), utm=utm,
            )
            key = sale.id if get(r, "id") else f"{sale.email}|{sale.produto}|{sale.valor}|{sale.data}"
            sales.setdefault(key, sale)
    return list(sales.values())


@dataclass
class Contact:
    sessao: str
    primeira: datetime | None = None
    link_em: datetime | None = None
    recebeu_link: bool = False
    emails: set[str] = field(default_factory=set)
    mensagens: int = 0


def load_conversations_rows(args) -> list[dict[str, str]]:
    if args.conversas:
        return read_csv(Path(args.conversas))
    url = os.environ.get("DATABASE_URL") or os.environ.get("BEPPLER_DATABASE_URL")
    if not url:
        sys.exit("Sem conversas: passe --conversas <csv> ou defina BEPPLER_DATABASE_URL "
                 "(set -a; . ~/.claude/secrets/deoliveiratech.env; set +a).")
    table = args.tabela
    if not re.fullmatch(r"[A-Za-z0-9_]+", table):
        sys.exit("Nome de tabela inválido.")
    has_ts = subprocess.run(
        ["psql", url, "-At", "-c", f"select 1 from information_schema.columns where table_name='{table}' and column_name='created_at'"],
        capture_output=True, text=True, check=True,
    ).stdout.strip() == "1"
    ts = "created_at" if has_ts else "null"
    sql = (f"\\copy (select id, session_id, message->>'type' as type, message->>'content' as content, {ts} as created_at "
           f"from {table} order by id) to stdout with csv header")
    out = subprocess.run(["psql", url, "-c", sql], capture_output=True, text=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(out)))


def build_contacts(rows: list[dict[str, str]]) -> dict[str, Contact]:
    contacts: dict[str, Contact] = {}
    for r in rows:
        sess = (r.get("session_id") or "").strip()
        key = phone_key(sess)
        if not key or not re.fullmatch(r"\+?\d+", sess):
            continue  # sessões de teste (claude-…) ou sem telefone
        c = contacts.setdefault(key, Contact(sessao=sess))
        ts = parse_date(r.get("created_at"))
        content = r.get("content") or ""
        kind = (r.get("type") or "").lower()
        c.mensagens += 1
        if ts and (c.primeira is None or ts < c.primeira):
            c.primeira = ts
        if kind == "human":
            c.emails.update(e.lower() for e in EMAIL_RE.findall(content))
        if kind == "ai" and any(m in content for m in LINK_MARKERS):
            c.recebeu_link = True
            if ts and (c.link_em is None or ts < c.link_em):
                c.link_em = ts
    return contacts


def classify(sales: list[Sale], contacts: dict[str, Contact], janela: timedelta) -> None:
    by_email = {e: c for c in contacts.values() for e in c.emails}
    for s in sales:
        u = norm(s.utm)
        if re.search(r"(^|\W)ia($|\W)", u) or "ia-vendas" in s.utm.lower() or "sofia" in u:
            s.classe = "utm"
            continue
        c = contacts.get(phone_key(s.telefone) or "") or by_email.get(s.email)
        if not c:
            continue
        s.sessao = c.sessao
        if s.data and c.primeira and c.primeira > s.data:
            s.classe = "pos_compra"
        elif c.recebeu_link and (not s.data or not c.link_em or c.link_em <= s.data <= c.link_em + janela):
            s.classe = "link"
        else:
            s.classe = "conversa"


LABELS = {
    "utm": "Chegou pela UTM da Sofia",
    "link": "Recebeu link da Sofia antes de comprar",
    "conversa": "Conversou com a Sofia antes, sem link",
    "pos_compra": "Só falou com a Sofia depois da compra",
    "sem_contato": "Sem contato com a Sofia",
}


def brl(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def report(sales: list[Sale], desde, ate) -> dict:
    tot = defaultdict(lambda: [0, 0.0])
    prod = defaultdict(lambda: defaultdict(lambda: [0, 0.0]))
    for s in sales:
        tot[s.classe][0] += 1
        tot[s.classe][1] += s.valor
        prod[s.produto or "(sem produto)"][s.classe][0] += 1
        prod[s.produto or "(sem produto)"][s.classe][1] += s.valor
    atrib = [k for k in ("utm", "link")]
    return {
        "periodo": [desde.isoformat() if desde else None, ate.isoformat() if ate else None],
        "vendas_aprovadas": len(sales),
        "receita_total": round(sum(s.valor for s in sales), 2),
        "por_classe": {k: {"vendas": tot[k][0], "receita": round(tot[k][1], 2)} for k in LABELS},
        "atribuidas_sofia": {"vendas": sum(tot[k][0] for k in atrib), "receita": round(sum(tot[k][1] for k in atrib), 2)},
        "influenciadas_sofia": {"vendas": sum(tot[k][0] for k in ("utm", "link", "conversa")),
                                "receita": round(sum(tot[k][1] for k in ("utm", "link", "conversa")), 2)},
        "por_produto": {p: {k: {"vendas": v[0], "receita": round(v[1], 2)} for k, v in d.items()} for p, d in prod.items()},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vendas", nargs="+", required=True, type=Path)
    ap.add_argument("--conversas", help="CSV com session_id, type, content e (opcional) created_at")
    ap.add_argument("--tabela", default="n8n_chat_histories_tpoc_setembro")
    ap.add_argument("--desde", help="AAAA-MM-DD, filtra vendas a partir desta data")
    ap.add_argument("--ate", help="AAAA-MM-DD, filtra vendas até esta data (inclusive)")
    ap.add_argument("--janela-dias", type=int, default=30, help="dias entre o link e a compra (padrão 30)")
    ap.add_argument("--saida", type=Path, default=Path(__file__).resolve().parents[4] / "docs" / "conta" / "atribuicao")
    for k in COLUMNS:
        ap.add_argument(f"--col-{k.replace('_', '-')}", dest=f"col_{k}", help=f"nome exato da coluna de {k}")
    args = ap.parse_args(argv)

    warnings: list[str] = []
    overrides = {k: getattr(args, f"col_{k}") for k in COLUMNS if getattr(args, f"col_{k}")}
    sales = load_sales(args.vendas, overrides, warnings.append)
    desde = datetime.fromisoformat(args.desde) if args.desde else None
    ate = datetime.fromisoformat(args.ate) + timedelta(days=1) if args.ate else None
    if desde or ate:
        sem_data = sum(1 for s in sales if not s.data)
        if sem_data:
            warnings.append(f"{sem_data} vendas sem data ficaram fora do filtro de período")
        sales = [s for s in sales if s.data and (not desde or s.data >= desde) and (not ate or s.data < ate)]

    contacts = build_contacts(load_conversations_rows(args))
    if not any(c.primeira for c in contacts.values()):
        warnings.append("as conversas não têm data: a ordem conversa → compra não foi checada")
    classify(sales, contacts, timedelta(days=args.janela_dias))
    summary = report(sales, desde, ate)
    summary["contatos_sofia"] = len(contacts)
    summary["avisos"] = warnings

    args.saida.mkdir(parents=True, exist_ok=True)
    (args.saida / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.saida / "vendas-classificadas.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["classe", "origem", "id", "data", "valor", "produto", "telefone", "email", "utm", "sessao_sofia"])
        for s in sorted(sales, key=lambda s: (s.classe, s.data or datetime.min)):
            w.writerow([s.classe, s.origem, s.id, s.data.isoformat() if s.data else "", f"{s.valor:.2f}",
                        s.produto, s.telefone, s.email, s.utm, s.sessao])

    print(f"Vendas aprovadas no período: {summary['vendas_aprovadas']} · {brl(summary['receita_total'])}")
    print(f"Contatos da Sofia com telefone: {len(contacts)}\n")
    for k, label in LABELS.items():
        d = summary["por_classe"][k]
        print(f"  {label:<42} {d['vendas']:>5}  {brl(d['receita']):>16}")
    a, i = summary["atribuidas_sofia"], summary["influenciadas_sofia"]
    print(f"\nAtribuídas à Sofia (UTM + link):   {a['vendas']} vendas · {brl(a['receita'])}")
    print(f"Influenciadas (+ conversa sem link): {i['vendas']} vendas · {brl(i['receita'])}")
    for w_ in warnings:
        print(f"\nAviso: {w_}")
    print(f"\nDetalhe em {args.saida}/ (fora do git; tem telefone e e-mail)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

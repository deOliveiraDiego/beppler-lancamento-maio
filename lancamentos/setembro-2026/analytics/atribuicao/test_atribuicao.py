"""Testes com dados fictícios. Rodar: python3 -I -m unittest discover -s lancamentos/setembro-2026/analytics/atribuicao"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import atribuicao as a  # noqa: E402

GURU = """Id da transação;Nome do produto;Status da venda;Data de aprovação;Valor total;Telefone do comprador;Email do comprador;utm_medium;utm_campaign
T1;Combo Black;Aprovada;22/09/2026 10:15:00;R$ 3.997,00;(11) 90000-0001;a@exemplo.com;ia;ia-vendas
T2;Combo Black;Aprovada;23/09/2026 11:00:00;R$ 4.997,00;+55 21 90000-0002;b@exemplo.com;;
T3;Combo Black;Aprovada;24/09/2026 12:00:00;R$ 3.997,00;31900000003;c@exemplo.com;;
T4;Combo Black;Reembolsada;24/09/2026 12:00:00;R$ 3.997,00;41900000004;d@exemplo.com;;
T5;Combo Black;Aprovada;25/09/2026 09:00:00;R$ 3.997,00;51900000005;e@exemplo.com;;
T6;Combo Black;Aprovada;26/09/2026 09:00:00;R$ 3.997,00;;f@exemplo.com;;
T7;Combo Black;Aprovada;27/09/2026 09:00:00;R$ 3.997,00;61900000007;g@exemplo.com;;
"""

TMB = """transaction,product,status,paid at,amount,phone,email
X1,Combo Black Boleto,paid,2026-09-28 10:00:00,4997.00,7190000008,h@exemplo.com
"""

# T2: recebeu link antes → link. T3: conversou sem link → conversa. T5: primeira conversa depois da compra → pos_compra.
# T6: sem telefone, mas mandou o e-mail na conversa → link. T7: sem conversa → sem_contato.
# X1: telefone sem o nono dígito na venda, com nono na sessão → link.
CONVERSAS = """id,session_id,type,content,created_at
1,5521900000002,human,oi quero saber da black,2026-09-22 08:00:00
2,5521900000002,ai,segue o link https://sndflw.com/l/black-sofia,2026-09-22 08:01:00
3,5531900000003,human,quanto custa?,2026-09-23 08:00:00
4,5531900000003,ai,custa R$ 3.997,2026-09-23 08:01:00
5,5551900000005,human,não consigo acessar,2026-09-26 08:00:00
6,5591900000009,human,meu email é f@exemplo.com,2026-09-25 08:00:00
7,5591900000009,ai,aqui está: https://sndflw.com/l/black-sofia,2026-09-25 08:01:00
8,claude-teste-1,human,teste,2026-09-25 08:00:00
9,5571990000008,ai,link do boleto https://pay.tmb.com.br/EscoladeArte/X,2026-09-27 08:00:00
"""


class AtribuicaoTest(unittest.TestCase):
    def run_case(self, extra=()):
        d = Path(tempfile.mkdtemp())
        (d / "guru.csv").write_text(GURU, encoding="utf-8")
        (d / "tmb.csv").write_text(TMB, encoding="utf-8")
        (d / "conv.csv").write_text(CONVERSAS, encoding="utf-8")
        a.main(["--vendas", str(d / "guru.csv"), str(d / "tmb.csv"), "--conversas", str(d / "conv.csv"),
                "--saida", str(d / "out"), *extra])
        return json.loads((d / "out" / "resumo.json").read_text(encoding="utf-8"))

    def test_classes(self):
        r = self.run_case()
        c = {k: v["vendas"] for k, v in r["por_classe"].items()}
        self.assertEqual(c, {"utm": 1, "link": 3, "conversa": 1, "pos_compra": 1, "sem_contato": 1})
        self.assertEqual(r["vendas_aprovadas"], 7)  # reembolso fora
        self.assertEqual(r["atribuidas_sofia"], {"vendas": 4, "receita": 3997 + 4997 + 3997 + 4997})
        self.assertEqual(r["contatos_sofia"], 5)  # sessão de teste fora

    def test_periodo(self):
        r = self.run_case(["--desde", "2026-09-25", "--ate", "2026-09-27"])
        self.assertEqual(r["vendas_aprovadas"], 3)

    def test_helpers(self):
        self.assertEqual(a.parse_money("R$ 3.997,00"), 3997.0)
        self.assertEqual(a.parse_money("4,997.50"), 4997.5)
        self.assertEqual(a.phone_key("+55 (51) 98178-6460"), a.phone_key("51 8178-6460"))
        from datetime import datetime
        self.assertEqual(a.parse_date("2026-09-23 16:34:31.13872+00"), datetime(2026, 9, 23, 13, 34, 31))
        self.assertEqual(a.parse_date("2026-09-23T16:34:31Z"), datetime(2026, 9, 23, 13, 34, 31))
        self.assertEqual(a.parse_date("22/09/2026 10:15:00"), datetime(2026, 9, 22, 10, 15))
        self.assertEqual(a.parse_date("2026-09-22"), datetime(2026, 9, 22))


if __name__ == "__main__":
    unittest.main()

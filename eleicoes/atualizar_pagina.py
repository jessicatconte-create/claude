"""Grava os dados de dados_2026.csv e dados_estados_2026.json dentro de apuracao_2022_2026.html
(entre os marcadores /*DADOS*/ e /*FIM*/)."""
import csv, json, re

PAGINA = "apuracao_2022_2026.html"

with open("dados_2026.csv") as f:
    d26 = [[float(r["pct_secoes"]), r["hora"], float(r["lula"]), float(r["bolsonaro"])] for r in csv.DictReader(f)]
with open("dados_estados_2026.json") as f:
    uf = json.load(f)

campos = ("pct", "hora", "st", "ts", "vv", "lula", "flavio", "lv", "fv")
estados = {k: {c: v[c] for c in campos} for k, v in uf["estados"].items()}
br = {c: uf["br"][c] for c in campos}

js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
bloco = f"/*DADOS*/\nconst D26 = {js(d26)};\nconst ESTADOS = {js(estados)};\nconst BR = {js(br)};\n/*FIM*/"

s = open(PAGINA).read()
s = re.sub(r"/\*DADOS\*/.*?/\*FIM\*/", lambda _: bloco, s, count=1, flags=re.S)
open(PAGINA, "w").write(s)
print(f"página atualizada: {d26[-1][0]:.2f}% apurado, {len(estados)} estados")

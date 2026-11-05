"""Efeito da ordem de chegada das urnas no 2º turno de 2022, por UF, a partir de dados_2022_2t_secoes.json.
Para cada UF e cada p = 0..100 (% das seções da UF já recebidas pelo TSE), guarda quanto a parte de Lula entre
os dois no resultado final diferia da parte dele nas seções já recebidas: vies[p] = final − parcial (pontos).
Usado pela projeção da noite do 2º turno de 2026. Grava dados_2022_2t_vies.json."""
import json

d = json.load(open("dados_2022_2t_secoes.json"))
out = {}
for uf, secs in d.items():
    secs = sorted((s for s in secs if len(s) >= 5), key=lambda s: s[4])
    n = len(secs); L = sum(s[1] for s in secs); B = sum(s[2] for s in secs)
    final = 100 * L / (L + B)
    curva, l, b, k = [], 0, 0, 0
    for p in range(101):
        alvo = max(1, round(n * p / 100))
        while k < alvo:
            l += secs[k][1]; b += secs[k][2]; k += 1
        curva.append(round(final - 100 * l / (l + b), 2) if l + b else 0.0)
    out[uf] = curva
json.dump(out, open("dados_2022_2t_vies.json", "w"), separators=(",", ":"))
for uf in ("SP", "MG", "BA", "RJ"):
    c = out[uf]; print(uf, "10%:", c[10], "30%:", c[30], "50%:", c[50], "80%:", c[80])

"""Andamento do 2º turno de 2022 (presidente) a partir de dados_2022_2t_secoes.json (boletins de urna):
todas as seções do país ordenadas pelo horário em que o TSE recebeu o boletim; a cada ~1% de seções,
o % de Lula e de Bolsonaro nos válidos acumulados. Sem o exterior. Grava dados_2022_2t_serie.json
como [[% seções, "hhhmm", Lula, Bolsonaro], ...]."""
import json

d = json.load(open("dados_2022_2t_secoes.json"))
secs = sorted((s for v in d.values() for s in v if len(s) >= 5), key=lambda s: s[4])
n, L, B, V, out, prox = len(secs), 0, 0, 0, [], 0.0
for k, s in enumerate(secs, 1):
    L += s[1]; B += s[2]; V += s[3]
    p = 100 * k / n
    if (p >= prox or k == n) and V:
        m = s[4]
        out.append([round(p, 2), f"{m // 60 % 24:02d}h{m % 60:02d}", round(100 * L / V, 2), round(100 * B / V, 2)])
        prox = p + (0.25 if p < 5 else 1)
json.dump(out, open("dados_2022_2t_serie.json", "w"), separators=(",", ":"))
print(len(d), "UFs,", n, "seções; final Lula", out[-1][2], "Bolsonaro", out[-1][3])

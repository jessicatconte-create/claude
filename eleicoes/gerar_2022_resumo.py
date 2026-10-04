"""Resumo de 2022 por UF a partir de dados_2022_secoes.json (boletins de urna):
resultado final (Lula, Bolsonaro, válidos) e curva do % de seções com boletim emitido a cada minuto,
das 17h00 às 24h00 (horário de Brasília). Grava dados_2022_resumo.json."""
import json

d = json.load(open("dados_2022_secoes.json"))
INI, FIM = 17 * 60, 24 * 60
out = {}
for uf, secs in d.items():
    n = len(secs)
    # curva pelo horário em que o TSE recebeu o boletim (5º campo); sem ele, não há curva confiável
    if not all(len(s) >= 5 for s in secs):
        L = sum(s[1] for s in secs); B = sum(s[2] for s in secs); V = sum(s[3] for s in secs)
        out[uf] = {"lula": round(100 * L / V, 2), "bolsonaro": round(100 * B / V, 2), "vv": V, "secoes": n}
        continue
    mins = sorted(s[4] for s in secs)
    curva, k = [], 0
    for t in range(INI, FIM + 1):
        while k < n and mins[k] <= t:
            k += 1
        curva.append(round(100 * k / n, 2))
    L = sum(s[1] for s in secs); B = sum(s[2] for s in secs); V = sum(s[3] for s in secs)
    out[uf] = {"lula": round(100 * L / V, 2), "bolsonaro": round(100 * B / V, 2), "vv": V, "secoes": n, "curva": curva}
json.dump(out, open("dados_2022_resumo.json", "w"), separators=(",", ":"))
print(len(out), "UFs")

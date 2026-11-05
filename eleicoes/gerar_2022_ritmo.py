"""Ritmo da apuração do 2º turno de 2022 por estado, a partir de dados_2022_2t_secoes.json (boletins de urna com o
minuto em que o TSE recebeu cada um, horário de Brasília): % das seções de cada UF já recebidas a cada 2 minutos,
das 17h00 às 02h00, e a parte de Lula entre os dois nessas seções. Grava dados_2022_2t_ritmo.json como
{"t0": 1020, "passo": 2, "uf": {UF: [%...]}, "br": [%...], "lula_uf": {UF: [%...]}, "lula_br": [%...]}."""
import json

T0, PASSO, FIM = 17 * 60, 2, 26 * 60
d = json.load(open("dados_2022_2t_secoes.json"))
tempos = range(T0, FIM + 1, PASSO)


def curva(secs):
    """% das seções recebidas e % de Lula entre Lula e Bolsonaro nessas seções, em cada instante."""
    ts = sorted((s for s in secs if len(s) >= 5), key=lambda s: s[4])
    n, pct, lula, k, L, B = len(secs), [], [], 0, 0, 0
    for t in tempos:
        while k < len(ts) and ts[k][4] <= t:
            L += ts[k][1]; B += ts[k][2]; k += 1
        pct.append(round(100 * k / n, 1))
        lula.append(round(100 * L / (L + B), 1) if L + B else None)
    return pct, lula


por_uf = {uf: curva(v) for uf, v in d.items()}
br = curva([s for v in d.values() for s in v])
saida = {"t0": T0, "passo": PASSO, "uf": {uf: c[0] for uf, c in por_uf.items()}, "br": br[0],
         "lula_uf": {uf: c[1] for uf, c in por_uf.items()}, "lula_br": br[1]}
json.dump(saida, open("dados_2022_2t_ritmo.json", "w"), separators=(",", ":"))
print(len(saida["uf"]), "UFs; Brasil às 17h30:", saida["br"][15], "% e às 18h00:", saida["br"][30], "%")

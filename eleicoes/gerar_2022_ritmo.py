"""Ritmo da apuração do 2º turno de 2022 por estado, a partir de dados_2022_2t_secoes.json (boletins de urna com o
minuto em que o TSE recebeu cada um, horário de Brasília): % das seções de cada UF já recebidas a cada 2 minutos,
das 17h00 às 02h00. Grava dados_2022_2t_ritmo.json como {"t0": 1020, "passo": 2, "uf": {UF: [%...]}, "br": [%...]}."""
import json

T0, PASSO, FIM = 17 * 60, 2, 26 * 60
d = json.load(open("dados_2022_2t_secoes.json"))
tempos = range(T0, FIM + 1, PASSO)


def curva(secs):
    ts = sorted(s[4] for s in secs if len(s) >= 5)
    n, out, k = len(secs), [], 0
    for t in tempos:
        while k < len(ts) and ts[k] <= t:
            k += 1
        out.append(round(100 * k / n, 1))
    return out


saida = {"t0": T0, "passo": PASSO, "uf": {uf: curva(v) for uf, v in d.items()}, "br": curva([s for v in d.values() for s in v])}
json.dump(saida, open("dados_2022_2t_ritmo.json", "w"), separators=(",", ":"))
print(len(saida["uf"]), "UFs; Brasil às 17h30:", saida["br"][15], "% e às 18h00:", saida["br"][30], "%")

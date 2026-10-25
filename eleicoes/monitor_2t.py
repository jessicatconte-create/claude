"""Acompanha o 2º turno presidencial de 2026 (eleição 6258 do TSE) e grava dados_2t_2026.json,
usado pelo atualizar_pagina.py: Brasil (soma das UFs e exterior quando estiver mais adiantada),
cada UF e a série do andamento.

Uso:  python monitor_2t.py            # fica rodando; pare com Ctrl+C
      python monitor_2t.py --uma-vez  # uma leitura e sai
"""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
import monitor_tse as m

m.URL = "https://resultados.tse.jus.br/oficial/ele2026/6258/dados/{uf}/{uf}-c0001-e006258-u.json"
SAIDA = "dados_2t_2026.json"
INTERVALO = 30


def ler(j):
    """Como monitor_tse.ler, mas aceita o arquivo zerado de antes da apuração (sem horário)."""
    if not j.get("ht"):
        j = dict(j, ht="00:00:00", dt="25/10/2026")
    return m.ler(j)


def rodada():
    try:
        with open(SAIDA) as f:
            ant = json.load(f)
    except (OSError, ValueError):
        ant = {"estados": {}, "serie": []}
    estados, exterior = ant.get("estados", {}), ant.get("exterior")
    j = m.baixar()
    nacional = ler(j) if j else None
    with ThreadPoolExecutor(6) as ex:
        for uf, ju in zip(m.UFS, ex.map(m.baixar, m.UFS)):
            if ju:
                estados[uf.upper()] = ler(ju)
    jz = m.baixar("zz")
    if jz:
        exterior = ler(jz)
    partes = list(estados.values()) + ([exterior] if exterior else [])
    br = nacional
    if len(estados) == len(m.UFS) and sum(p["vv"] for p in partes):
        br = m.somar(partes, nacional)
    if br is None:
        return
    serie = ant.get("serie", [])
    if br["vv"] and (not serie or round(br["pct"], 2) > serie[-1][0]):
        serie.append([round(br["pct"], 2), br["hora"], round(br["lula"], 2), round(br["flavio"], 2)])
    with open(SAIDA, "w") as f:
        json.dump({"br": br, "estados": estados, "exterior": exterior, "serie": serie}, f, ensure_ascii=False)
    print(f"2º turno {br['hora']}  {br['pct']:.2f}% apurado  Flávio {br['flavio']:.2f}%  Lula {br['lula']:.2f}%")


if __name__ == "__main__":
    while True:
        rodada()
        if "--uma-vez" in sys.argv:
            break
        time.sleep(INTERVALO)

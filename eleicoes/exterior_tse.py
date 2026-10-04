"""Votos de brasileiros no exterior (TSE, 1º turno 2026): total e por cidade.

Grava dados_exterior_2026.json, usado pelo atualizar_pagina.py.
Uso: python exterior_tse.py
"""
import json, time
from monitor_tse import baixar, ler, URL
import requests

CM = "https://resultados.tse.jus.br/oficial/ele2026/6257/config/mun-e006257-cm.json"


def main():
    cfg = requests.get(CM, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).json()
    cidades = next(a for a in cfg["abr"] if a["cd"] == "zz")["mu"]
    total = ler(baixar("zz"))
    linhas = []
    for c in cidades:
        j = baixar(f"zz{c['cd']}")
        if j:
            d = ler(j)
            if d["vv"]:
                linhas.append({"nome": c["nm"].title(), **{k: d[k] for k in ("pct", "vv", "lula", "flavio", "lv", "fv")}})
        time.sleep(0.25)
    json.dump({"total": total, "cidades": linhas}, open("dados_exterior_2026.json", "w"), ensure_ascii=False)
    print(f"exterior: {total['pct']:.2f}% apurado, Lula {total['lula']:.2f}% × Flávio {total['flavio']:.2f}%, {len(linhas)} cidades")


if __name__ == "__main__":
    main()

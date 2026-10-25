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


URL_GOV = "https://resultados.tse.jus.br/oficial/ele2026/6260/dados/{uf}/{uf}-c0003-e006260-u.json"
UFS_GOV = ["ac", "am", "df", "es", "rn", "to"]   # estados com 2º turno de governador (eleição 6260)


def eleito(j):
    """Nome de quem o TSE declarou eleito no arquivo, ou None."""
    for a in j["carg"][0]["agr"]:
        for p in a["par"]:
            for c in p["cand"]:
                if c.get("e") == "s" or str(c.get("st", "")).lower().startswith("eleito"):
                    return c["nmu"].title()
    return None


def governadores(anterior):
    """2º turno de governador: % apurado e os dois candidatos em cada UF; UF que falhar mantém o dado anterior."""
    def uma(uf):
        try:
            r = m.requests.get(URL_GOV.format(uf=uf), timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            j = r.json() if r.ok else None
        except (m.requests.RequestException, ValueError):
            j = None
        if not j:
            return uf, None
        cs = sorted(((cd, par["sg"]) for a in j["carg"][0]["agr"] for par in a["par"] for cd in par["cand"]), key=lambda x: (-int(x[0]["vap"]), x[0]["nmu"]))
        return uf, {"apurado": m.num(j["s"]["pstn"]), "vv": int(j["v"]["vv"]), "hms": j.get("ht", ""),
                    "cands": [{"nome": cd["nmu"].title(), "partido": sg, "pct": m.num(cd["pvapn"]), "votos": int(cd["vap"]),
                               "eleito": cd.get("e") == "s"} for cd, sg in cs]}
    out = dict(anterior or {})
    with ThreadPoolExecutor(6) as ex:
        for uf, d in ex.map(uma, UFS_GOV):
            if d:
                out[uf.upper()] = d
    return out


MODELOS = {
    "electomaps": "https://electomaps.com.br/dados/6258-0001-proj.json",
    "mahlmeister": "https://projecao.2026elections.workers.dev/dados/apuracao.json",
}
SQ = {"280002551544": "flavio", "280002542548": "lula"}


def modelos(anterior):
    """Projeções publicadas por outros: ElectoMaps (por município) e Rodrigo Mahlmeister/Estadão (por seção).
    Guarda só o essencial, em pontos percentuais; quem não responder mantém o dado anterior."""
    out = dict(anterior or {})
    for nome, url in MODELOS.items():
        try:
            j = m.requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).json()
        except (m.requests.RequestException, ValueError):
            continue
        if nome == "electomaps":
            r = {"pct": j.get("pct_apurado"), "gerado": j.get("gerado"), "pronta": bool(j.get("suficiente")), "motivo": j.get("motivo")}
            for sq, k in SQ.items():
                c = (j.get("cand") or {}).get(sq)
                if c:
                    r[k] = {"med": 100 * c["media"], "lo": 100 * c["p025"], "hi": 100 * c["p975"], "apurado": 100 * c["apurado"], "p": c.get("p_maioria")}
            r["serie"] = [[p["pct"], 100 * p["c"][sq_f][0], 100 * p["c"][sq_f][1], 100 * p["c"][sq_f][2]]
                          for p in j.get("serie", []) for sq_f in ["280002551544"] if p.get("c", {}).get(sq_f)]
        else:
            pts = j.get("pontos") or []
            r = {"atualizado": j.get("atualizado"), "nivel": j.get("nivel_faixa"), "pronta": False, "pct": j.get("pct_eleitorado_apurado")}
            com = [p for p in pts if p.get("projecao")]
            if com:
                u = com[-1]
                r.update(pronta=True, pct=u.get("x"), t=u.get("t"),
                         flavio={"med": u["projecao"]["PL"], "lo": u["faixa"]["PL"][0], "hi": u["faixa"]["PL"][1], "apurado": u["apurado"]["PL"]},
                         lula={"med": u["projecao"]["PT"], "lo": u["faixa"]["PT"][0], "hi": u["faixa"]["PT"][1], "apurado": u["apurado"]["PT"]})
                r["serie"] = [[p["x"], p["projecao"]["PL"], p["faixa"]["PL"][0], p["faixa"]["PL"][1]] for p in com]
        out[nome] = r
    return out


def rodada():
    try:
        with open(SAIDA) as f:
            ant = json.load(f)
    except (OSError, ValueError):
        ant = {"estados": {}, "serie": []}
    estados, exterior = ant.get("estados", {}), ant.get("exterior")
    j = m.baixar()
    nacional = ler(j) if j else None
    eleito_br = eleito(j) if j else None
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
    br = dict(br, eleito=eleito_br or ant.get("br", {}).get("eleito"))
    serie = ant.get("serie", [])
    if br["vv"] and (not serie or round(br["pct"], 2) > serie[-1][0]):
        serie.append([round(br["pct"], 2), br["hora"], round(br["lula"], 2), round(br["flavio"], 2)])
    with open(SAIDA, "w") as f:
        json.dump({"br": br, "estados": estados, "exterior": exterior, "serie": serie,
                   "gov": governadores(ant.get("gov")), "modelos": modelos(ant.get("modelos"))}, f, ensure_ascii=False)
    print(f"2º turno {br['hora']}  {br['pct']:.2f}% apurado  Flávio {br['flavio']:.2f}%  Lula {br['lula']:.2f}%")


if __name__ == "__main__":
    while True:
        rodada()
        if "--uma-vez" in sys.argv:
            break
        time.sleep(INTERVALO)

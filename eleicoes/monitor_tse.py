"""Acompanha a apuração presidencial direto do JSON público do TSE.

A cada INTERVALO segundos baixa o boletim nacional e o de cada UF:
- quando o % de seções totalizadas no país muda, acrescenta uma linha em
  dados_2026.csv e regenera o gráfico PNG;
- grava dados_estados_2026.json com seções, votos válidos e votos de Lula e
  Flávio em cada UF (usado pelo atualizar_pagina.py).

Uso:  pip install requests pandas matplotlib
      python monitor_tse.py            # fica rodando; pare com Ctrl+C
      python monitor_tse.py --uma-vez  # uma leitura e sai
"""
import csv, json, subprocess, sys, time
from datetime import datetime, timedelta, timezone
import requests

# Arquivo que o painel resultados.tse.jus.br consulta (eleição 6257 = 1º turno 2026).
URL = "https://resultados.tse.jus.br/oficial/ele2026/6257/dados/{uf}/{uf}-c0001-e006257-u.json"
INTERVALO = 30
CSV = "dados_2026.csv"
JSON_UF = "dados_estados_2026.json"
LULA, FLAVIO = "LULA", "FLAVIO BOLSONARO"
UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to".split()

num = lambda s: float(str(s).replace(",", "."))


def baixar(uf="br"):
    for tentativa in range(4):
        try:
            r = requests.get(URL.format(uf=uf), timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if r.ok:
                return r.json()
            if r.status_code != 429:  # 429 = muitas requisições; espera e tenta de novo
                print("TSE respondeu", r.status_code, "para", uf, file=sys.stderr)
                return None
        except requests.RequestException as e:
            print("erro", uf, e, file=sys.stderr)
        time.sleep(2 ** tentativa)
    print("TSE não respondeu para", uf, file=sys.stderr)
    return None


def ler(j):
    """Resumo de um boletim: seções, horário da totalização e votos dos dois candidatos."""
    cands = {c["nmu"].upper(): c
             for agr in j["carg"][0]["agr"] for par in agr["par"] for c in par["cand"]}
    lula, flavio = cands[LULA], cands[FLAVIO]
    return {
        "pct": num(j["s"]["pstn"]), "st": int(j["s"]["st"]), "ts": int(j["s"]["ts"]),
        "hora": j["ht"][:5].replace(":", "h"), "hms": j["ht"], "data": j["dt"], "vv": int(j["v"]["vv"]), "tv": int(j["v"]["tv"]), "est": int(j["e"]["est"]), "comp": int(j["e"]["c"]), "abst": int(j["e"]["a"]), "vb": int(j["v"]["vb"]), "vn": int(j["v"]["tvn"]),
        "lula": num(lula["pvapn"]), "flavio": num(flavio["pvapn"]),
        "lv": int(lula["vap"]), "fv": int(flavio["vap"]),
    }


def ultimo_pct():
    with open(CSV) as f:
        linhas = list(csv.DictReader(f))
    return float(linhas[-1]["pct_secoes"]) if linhas else -1


URL_EST = "https://resultados.tse.jus.br/oficial/ele2026/6259/dados/{uf}/{uf}-c{c:04d}-e006259-u.json"
ACOMPANHAR = [("sp", 5, "Senado SP", ["SIMONE TEBET", "MARINA SILVA"]), ("sp", 6, "Dep. federal SP", ["ERIKA HILTON", "RODRIGO AGOSTINHO"])]


def outros_cargos():
    """Candidatos de outros cargos acompanhados (eleição estadual 6259): posição, % e votos."""
    out = []
    for uf, c, cargo, nomes in ACOMPANHAR:
        try:
            j = requests.get(URL_EST.format(uf=uf, c=c), timeout=30, headers={"User-Agent": "Mozilla/5.0"}).json()
        except (requests.RequestException, ValueError):
            continue
        cs = sorted(((cd, par["sg"]) for a in j["carg"][0]["agr"] for par in a["par"] for cd in par["cand"]), key=lambda x: -int(x[0]["vap"]))
        lideres = [{"nome": cd["nmu"].title(), "partido": sg, "pct": num(cd["pvapn"]), "votos": int(cd["vap"])} for cd, sg in cs[:2]]
        for pos, (cd, sg) in enumerate(cs, 1):
            if cd["nmu"].upper() in nomes:
                out.append({"nome": cd["nmu"].title(), "partido": sg, "cargo": cargo, "pos": pos, "pct": num(cd["pvapn"]), "votos": int(cd["vap"]),
                            "vagas": int(j["carg"][0].get("nv", 1)), "apurado": num(j["s"]["pstn"]), "lideres": lideres,
                            "vv_cargo": int(j["v"]["vv"]), "st": cd.get("st", ""), "eleito": cd.get("e") == "s"})
    return out


def somar(partes, nacional):
    """Total do Brasil somando as UFs e o exterior. O arquivo nacional do TSE às vezes fica parado
    enquanto os das UFs seguem atualizando; vale o que estiver mais adiantado."""
    t = {k: sum(p.get(k, 0) for p in partes) for k in ("st", "ts", "vv", "tv", "lv", "fv", "est", "comp", "abst", "vb", "vn")}
    # alguns arquivos (exterior, UFs em outro fuso) trazem horário local: vale o mais recente que já passou em Brasília
    agora = datetime.now(timezone(timedelta(hours=-3)))
    quando = lambda p: datetime.strptime(p["data"] + " " + p["hms"], "%d/%m/%Y %H:%M:%S").replace(tzinfo=agora.tzinfo)
    validos = [p for p in partes if quando(p) <= agora] or partes
    mais_novo = max(validos, key=quando)
    t.update(pct=100 * t["st"] / t["ts"], lula=100 * t["lv"] / t["vv"], flavio=100 * t["fv"] / t["vv"],
             hms=mais_novo["hms"], hora=mais_novo["hora"], data=mais_novo["data"], fonte="soma das UFs e exterior")
    return t if nacional is None or t["pct"] > nacional["pct"] + 0.01 else nacional


def rodada():
    j = baixar()
    nacional = ler(j) if j else None
    cands = sorted(({"nome": c["nmu"].title(), "pct": num(c["pvapn"]), "votos": int(c["vap"])}
                    for agr in j["carg"][0]["agr"] for par in agr["par"] for c in par["cand"]), key=lambda c: -c["votos"]) if j else []
    try:  # mantém o último dado de um estado que não responder
        with open(JSON_UF) as f:
            anterior = json.load(f)
        estados, exterior = anterior["estados"], anterior.get("exterior")
    except (OSError, ValueError, KeyError):
        estados, exterior = {}, None
    for uf in UFS:
        ju = baixar(uf)
        if ju:
            estados[uf.upper()] = ler(ju)
        time.sleep(0.3)
    jz = baixar("zz")
    if jz:
        exterior = ler(jz)
    partes = list(estados.values()) + ([exterior] if exterior else [])
    br = somar(partes, nacional) if len(estados) == len(UFS) else nacional
    if br is None:
        return
    if round(br["pct"], 2) > ultimo_pct():
        with open(CSV, "a", newline="") as f:
            csv.writer(f).writerow([f"{br['pct']:.2f}", br["hora"], f"{br['lula']:.2f}", f"{br['flavio']:.2f}"])
        subprocess.run([sys.executable, "grafico.py"])
    with open(JSON_UF, "w") as f:
        json.dump({"br": br, "estados": estados, "exterior": exterior, "outros": outros_cargos(), "candidatos": cands}, f, ensure_ascii=False)
    print(f"{br['hora']}  {br['pct']:.2f}% apurado  Flávio {br['flavio']:.2f}%  Lula {br['lula']:.2f}%  ({br.get('fonte', 'arquivo nacional')})")


if __name__ == "__main__":
    while True:
        rodada()
        if "--uma-vez" in sys.argv:
            break
        time.sleep(INTERVALO)

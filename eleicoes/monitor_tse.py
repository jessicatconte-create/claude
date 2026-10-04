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
        "hora": j["ht"][:5].replace(":", "h"), "hms": j["ht"], "data": j["dt"], "vv": int(j["v"]["vv"]),
        "lula": num(lula["pvapn"]), "flavio": num(flavio["pvapn"]),
        "lv": int(lula["vap"]), "fv": int(flavio["vap"]),
    }


def ultimo_pct():
    with open(CSV) as f:
        linhas = list(csv.DictReader(f))
    return float(linhas[-1]["pct_secoes"]) if linhas else -1


def rodada():
    j = baixar()
    if not j:
        return
    br = ler(j)
    if round(br["pct"], 2) > ultimo_pct():
        with open(CSV, "a", newline="") as f:
            csv.writer(f).writerow([f"{br['pct']:.2f}", br["hora"], f"{br['lula']:.2f}", f"{br['flavio']:.2f}"])
        subprocess.run([sys.executable, "grafico.py"])
    print(f"{br['hora']}  {br['pct']:.2f}% apurado  Flávio {br['flavio']:.2f}%  Lula {br['lula']:.2f}%")
    try:  # mantém o último dado de um estado que não responder
        with open(JSON_UF) as f:
            estados = json.load(f)["estados"]
    except (OSError, ValueError, KeyError):
        estados = {}
    for uf in UFS:
        ju = baixar(uf)
        if ju:
            estados[uf.upper()] = ler(ju)
        time.sleep(0.3)
    with open(JSON_UF, "w") as f:
        json.dump({"br": br, "estados": estados}, f, ensure_ascii=False)
    print(f"   {len(estados)} estados salvos em {JSON_UF}")


if __name__ == "__main__":
    while True:
        rodada()
        if "--uma-vez" in sys.argv:
            break
        time.sleep(INTERVALO)

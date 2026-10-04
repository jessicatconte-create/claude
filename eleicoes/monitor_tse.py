"""Acompanha a apuração presidencial direto do JSON público do TSE.

A cada INTERVALO segundos baixa o boletim nacional; quando o % de seções
totalizadas muda, acrescenta uma linha em dados_2026.csv e regenera o gráfico.
Também grava dados_estados_2026.csv com o % apurado e o placar de cada UF.

Uso:  pip install requests pandas matplotlib
      python monitor_tse.py
Pare com Ctrl+C.
"""
import csv, subprocess, sys, time
import requests

# Arquivo que o painel resultados.tse.jus.br consulta (eleição 6257 = 1º turno 2026).
# Se der 404, abra o painel, aperte F12 > Rede, filtre por "br-c0001" e cole a URL aqui.
URLS = [
    "https://resultados.tse.jus.br/oficial/ele2026/6257/dados-simplificados/br/br-c0001-e006257-r.json",
    "https://resultados.tse.jus.br/oficial/ele2026/6257/dados/br/br-c0001-e006257-u.json",
]
INTERVALO = 30
CSV = "dados_2026.csv"
LULA, BOLSONARO = "LULA", "FLAVIO BOLSONARO"
CSV_UF = "dados_estados_2026.csv"
UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to".split()

num = lambda s: float(str(s).replace(".", "").replace(",", ".")) if "," in str(s) else float(s)


def boletim(uf="br"):
    for url in URLS:
        url = url.replace("/br/br-", f"/{uf}/{uf}-")
        try:
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if r.ok:
                return r.json()
        except requests.RequestException as e:
            print("erro", url, e, file=sys.stderr)
    return None


def ler(j):
    cand = {c["nm"].upper(): c for c in j["cand"]}
    pct = lambda nome: num(next(c for k, c in cand.items() if nome in k)["pvap"])
    hora = j.get("hg", "")[:5].replace(":", "h")
    return num(j["pst"]), hora, pct(LULA), pct(BOLSONARO)


def ultimo_pct():
    with open(CSV) as f:
        linhas = list(csv.DictReader(f))
    return float(linhas[-1]["pct_secoes"]) if linhas else -1


while True:
    j = boletim()
    if j:
        pst, hora, lula, bol = ler(j)
        if pst > ultimo_pct():
            with open(CSV, "a", newline="") as f:
                csv.writer(f).writerow([f"{pst:.2f}", hora, f"{lula:.2f}", f"{bol:.2f}"])
            subprocess.run([sys.executable, "grafico.py"])
            print(f"{hora}  {pst:.2f}% apurado  Flávio {bol:.2f}%  Lula {lula:.2f}%")
        # por estado: arquivo pronto para colar no campo "Colar dados por estado" da página
        linhas = []
        for uf in UFS:
            ju = boletim(uf)
            if ju:
                p, h, l, b = ler(ju)
                linhas.append([uf.upper(), f"{p:.2f}", h, f"{l:.2f}", f"{b:.2f}"])
        with open(CSV_UF, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["uf", "pct_secoes", "hora", "lula", "flavio"]); w.writerows(linhas)
        print(f"   {len(linhas)} estados salvos em {CSV_UF}")
    else:
        print("TSE não respondeu; tentando de novo", file=sys.stderr)
    time.sleep(INTERVALO)

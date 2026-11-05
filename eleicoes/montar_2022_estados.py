"""Reconstrói o andamento da apuração de 2022 (1º turno, presidente) por estado
a partir dos boletins de urna publicados pelo TSE (dados abertos).

O TSE não guarda o histórico da divulgação, então cada seção entra no horário em
que a urna emitiu o boletim (DT_EMISSAO_BU), convertido para o horário de Brasília.
É uma aproximação: a totalização acontecia alguns minutos depois.

Saída: dados_2022_secoes.json -> {UF: [[minuto_emissao, lula, bolsonaro, validos, minuto_recebido_tse], ...]}
(DT_BU_RECEBIDO já vem no horário de Brasília e acompanha a totalização; DT_EMISSAO_BU é o fechamento da urna.)
Uso: python montar_2022_estados.py   (baixa ~3 GB, um estado por vez, e apaga cada zip)
"""
import csv, io, json, os, sys, time, zipfile
from datetime import datetime
import requests

URL = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_1t_{uf}_051020221321.zip"
UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
# diferença para o horário de Brasília em 2022 (sem horário de verão)
FUSO = {"AC": 2, "AM": 1, "RO": 1, "RR": 1, "MT": 1, "MS": 1}
SAIDA = "dados_2022_secoes.json"
TMP = "_bweb.zip"  # fica fora do git (.gitignore)


def baixar(uf):
    for tentativa in range(12):
        try:
            with requests.get(URL.format(uf=uf), stream=True, timeout=60, headers={"User-Agent": "Mozilla/5.0"}) as r:
                if r.status_code == 200:
                    with open(TMP, "wb") as f:
                        for bloco in r.iter_content(1 << 20):
                            f.write(bloco)
                    if zipfile.is_zipfile(TMP):
                        return True
                print(uf, "status", r.status_code, "tentativa", tentativa + 1, flush=True)
        except requests.RequestException as e:
            print(uf, "erro", e, flush=True)
        time.sleep(min(30 * (tentativa + 1), 300))
    return False


def ler(uf):
    secoes = {}
    with zipfile.ZipFile(TMP) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        with z.open(nome) as f:
            leitor = csv.reader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")
            cab = next(leitor)
            i = {c: cab.index(c) for c in ("NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "NR_VOTAVEL", "QT_VOTOS", "DT_EMISSAO_BU", "DT_BU_RECEBIDO")}
            for lin in leitor:
                if lin[i["CD_CARGO_PERGUNTA"]] != "1":
                    continue
                chave = (lin[i["NR_ZONA"]], lin[i["NR_SECAO"]])
                s = secoes.get(chave)
                if s is None:
                    t = datetime.strptime(lin[i["DT_EMISSAO_BU"]], "%d/%m/%Y %H:%M:%S")
                    rc = datetime.strptime(lin[i["DT_BU_RECEBIDO"]], "%d/%m/%Y %H:%M:%S")
                    dias = (rc.date() - t.date()).days
                    s = secoes[chave] = [t.hour * 60 + t.minute + 60 * FUSO.get(uf, 0), 0, 0, 0, rc.hour * 60 + rc.minute + 1440 * dias]
                nv, qt = lin[i["NR_VOTAVEL"]], int(lin[i["QT_VOTOS"]])
                if nv not in ("95", "96"):  # 95 branco, 96 nulo
                    s[3] += qt
                if nv == "13":
                    s[1] += qt
                elif nv == "22":
                    s[2] += qt
    return sorted(secoes.values())


if __name__ == "__main__":
    dados = json.load(open(SAIDA)) if os.path.exists(SAIDA) else {}
    for uf in UFS:
        if uf in dados and dados[uf] and len(dados[uf][0]) >= 5:
            continue
        if not baixar(uf):
            print(uf, "não baixou; rode de novo depois", flush=True)
            continue
        dados[uf] = ler(uf)
        os.remove(TMP)
        json.dump(dados, open(SAIDA, "w"), separators=(",", ":"))
        print(uf, len(dados[uf]), "seções", flush=True)
        time.sleep(5)
    print("pronto:", len(dados), "estados", flush=True)

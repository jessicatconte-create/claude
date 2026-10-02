"""Números do prompt (seção 5, 6 e 7). Nada aqui é calculado fora do prompt, exceto
coordenadas de gráfico derivadas das retas informadas."""

ITEMS = ["Copo", "Duralex", "Opaline", "Lasanheira"]
FULL = {"Copo": "Copo Americano (102010188)", "Duralex": "Duralex (SM400000800N)",
        "Opaline": "Opaline (58440200847084)", "Lasanheira": "Lasanheira (GD16538265N)"}
MARGIN = {"Copo": 0.296, "Duralex": 0.646, "Opaline": 0.542, "Lasanheira": 0.668}

# Reta nacional: a, beta, ci, p, r2, cv
NAT = {
    "Copo": dict(a=7.94, b=-0.54, ci=(-2.80, 1.73), p="0,60", r2="0,04", cv="47%",
                 center=(1.29, 2439.1), ends=[(0.98, 2826.4, 5254.1, 1520.5), (1.60, 2174.4, 1341.2, 3525.2)]),
    "Duralex": dict(a=10.68, b=-3.41, ci=(-4.76, -2.06), p="0,0004", r2="0,81", cv="27%",
                    center=(9.02, 24.2), ends=[(6.92, 59.7, 85.6, 41.7), (10.90, 12.7, 9.8, 16.4)]),
    "Opaline": dict(a=10.89, b=-3.22, ci=(-4.19, -2.24), p="0,0001", r2="0,88", cv="26%",
                    center=(10.12, 31.5), ends=[(6.22, 150.7, 242.7, 93.5), (12.23, 17.1, 14.2, 20.6)]),
    "Lasanheira": dict(a=7.63, b=-1.44, ci=(-2.10, -0.79), p="0,0010", r2="0,76", cv="25%",
                       center=(76.21, 4.0), ends=[(49.34, 7.4, 9.8, 5.6), (117.48, 2.1, 1.6, 2.8)]),
}

# Faixas: faixa, preço médio, mín, máx, comb, lojas-mês, peças/loja-mês, %SP, %promo, p10, med, p90, CV
FAIXAS = {
    "Copo": [
        (1, 0.98, 0.85, 1.05, 5, 433, 2939.1, 80, 0, 440, 1698, 5245, 1.85),
        (2, 1.09, 1.08, 1.09, 4, 439, 4045.6, 100, 0, 469, 1778, 5526, 4.25),
        (3, 1.16, 1.10, 1.19, 5, 443, 2451.7, 80, 26, 312, 1436, 4634, 2.36),
        (4, 1.23, 1.19, 1.29, 4, 337, 1347.6, 0, 0, 34, 285, 1905, 3.82),
        (5, 1.30, 1.29, 1.34, 5, 276, 2141.5, 0, 22, 22, 252, 2330, 4.30),
        (6, 1.36, 1.35, 1.39, 4, 158, 2499.3, 0, 0, 68, 741, 5026, 3.06),
        (7, 1.39, 1.39, 1.39, 4, 55, 3180.3, 0, 82, 281, 1880, 4648, 2.50),
        (8, 1.47, 1.39, 1.49, 5, 236, 3412.5, 0, 0, 169, 1268, 5624, 3.09),
        (9, 1.49, 1.49, 1.49, 4, 142, 1022.4, 0, 73, 35, 342, 1649, 3.18),
        (10, 1.60, 1.49, 1.89, 5, 333, 3194.3, 0, 47, 57, 582, 5415, 3.38)],
    "Duralex": [
        (1, 6.92, 6.88, 6.99, 4, 162, 46.3, 25, 0, 7, 34, 99, 0.90),
        (2, 7.54, 6.99, 7.99, 4, 140, 60.8, 25, 0, 7, 47, 128, 0.87),
        (3, 8.26, 7.99, 8.48, 4, 328, 31.1, 100, 0, 5, 24, 68, 0.89),
        (4, 8.49, 8.49, 8.49, 4, 151, 20.1, 0, 0, 2, 14, 48, 0.94),
        (5, 8.90, 8.89, 8.90, 4, 291, 34.3, 100, 0, 6, 25, 72, 0.85),
        (6, 9.23, 8.90, 9.90, 4, 338, 30.5, 50, 0, 5, 24, 66, 0.93),
        (7, 9.90, 9.90, 9.98, 4, 229, 17.4, 0, 0, 3, 14, 38, 0.87),
        (8, 10.09, 9.98, 10.90, 4, 91, 16.2, 0, 0, 2, 10, 29, 1.25),
        (9, 10.90, 10.90, 10.90, 4, 104, 13.1, 0, 0, 2, 11, 28, 0.80),
        (10, 10.90, 10.90, 10.90, 4, 45, 9.9, 0, 0, 1, 9, 22, 0.74)],
    "Opaline": [
        (1, 6.22, 5.99, 7.99, 4, 338, 114.3, 100, 89, 7, 62, 203, 2.53),
        (2, 8.96, 8.79, 8.99, 4, 217, 68.6, 75, 0, 6, 36, 137, 1.81),
        (3, 9.50, 9.40, 9.90, 4, 227, 46.2, 50, 0, 5, 30, 103, 1.05),
        (4, 9.95, 9.90, 9.99, 3, 178, 36.2, 67, 0, 5, 26, 72, 0.98),
        (5, 10.24, 9.99, 10.90, 4, 167, 30.8, 25, 0, 4, 22, 58, 1.06),
        (6, 10.90, 10.90, 10.90, 4, 93, 28.2, 0, 0, 4, 18, 59, 1.19),
        (7, 11.04, 10.90, 11.40, 3, 102, 24.4, 0, 0, 5, 16, 48, 1.36),
        (8, 11.90, 11.90, 11.90, 4, 76, 12.8, 0, 0, 3, 9, 28, 0.91),
        (9, 11.90, 11.90, 11.90, 4, 50, 14.2, 0, 0, 4, 13, 28, 0.79),
        (10, 12.23, 11.90, 12.90, 4, 156, 19.0, 0, 0, 2, 16, 35, 0.87)],
    "Lasanheira": [
        (1, 49.34, 47.99, 49.90, 4, 273, 6.2, 100, 45, 1, 5, 12, 0.73),
        (2, 49.90, 49.90, 49.90, 3, 189, 8.2, 100, 100, 2, 7, 17, 0.83),
        (3, 57.65, 49.98, 64.90, 3, 136, 7.1, 100, 0, 1, 5, 12, 2.19),
        (4, 76.82, 75.44, 79.90, 3, 142, 3.3, 33, 0, 1, 2, 6, 1.09),
        (5, 83.90, 83.90, 83.90, 3, 21, 3.0, 0, 0, 1, 3, 6, 0.51),
        (6, 84.90, 84.90, 84.90, 3, 22, 4.7, 0, 0, 1, 4, 10, 0.77),
        (7, 89.60, 85.90, 89.90, 3, 51, 3.1, 0, 0, 1, 2, 8, 0.95),
        (8, 89.90, 89.90, 89.90, 3, 62, 3.7, 0, 0, 1, 2, 9, 1.20),
        (9, 89.90, 89.90, 89.90, 3, 56, 2.0, 0, 0, 1, 2, 4, 0.60),
        (10, 117.48, 95.00, 129.90, 4, 117, 2.3, 0, 0, 1, 2, 5, 0.80)],
}

# Retas por porte: beta, ci, p, r2, a, pontos
PORTE = {
    "Copo": {
        "pequenas": (-1.38, (-5.78, 3.02), "0,49", "0,06", 6.93, []),
        "médias": (1.62, (-0.53, 3.77), "0,12", "0,27", 6.92, []),
        "grandes": (1.57, (-0.74, 3.88), "0,16", "0,23", 8.23, []),
    },
    "Duralex": {
        "pequenas": (-1.45, (-3.45, 0.54), "0,13", "0,26", 5.61,
                     [(6.91, 13.3), (7.63, 29.1), (8.47, 11.8), (8.49, 10.6), (8.90, 5.7), (9.90, 14.4), (9.90, 9.7), (9.98, 9.0), (10.90, 8.2), (10.90, 9.4)]),
        "médias": (-1.71, (-2.76, -0.66), "0,0057", "0,64", 6.73,
                   [(6.93, 33.2), (7.47, 28.5), (8.24, 17.3), (8.49, 18.6), (8.90, 21.9), (9.47, 23.9), (9.90, 20.1), (10.11, 13.5), (10.90, 16.8), (10.90, 11.1)]),
        "grandes": (-2.32, (-3.64, -1.00), "0,0036", "0,67", 8.65,
                    [(6.94, 68.5), (7.66, 39.5), (8.15, 50.3), (8.48, 32.5), (8.84, 35.6), (8.90, 44.0), (9.90, 33.6), (9.94, 39.9), (10.01, 24.1), (10.90, 16.4)]),
    },
    "Opaline": {
        "pequenas": (0.24, (-0.90, 1.38), "0,64", "0,03", 1.97,
                     [(5.99, 9.7), (8.75, 9.8), (9.55, 19.8), (9.91, 13.9), (10.62, 21.6), (10.90, 11.4), (10.90, 13.7), (11.30, 9.3), (11.90, 10.9), (12.23, 11.3)]),
        "médias": (-1.56, (-2.14, -0.97), "0,0003", "0,83", 6.76,
                   [(6.28, 42.7), (8.93, 29.6), (9.51, 30.8), (9.94, 30.8), (10.51, 23.2), (10.90, 17.8), (11.21, 18.5), (11.90, 16.0), (11.90, 19.6), (12.32, 15.4)]),
        "grandes": (-2.78, (-3.85, -1.71), "0,0003", "0,82", 10.23,
                    [(6.21, 143.7), (8.96, 86.3), (9.48, 57.1), (9.95, 44.7), (10.29, 48.9), (10.90, 44.7), (11.09, 30.6), (11.90, 19.4), (11.90, 19.1), (12.52, 34.3)]),
    },
    "Lasanheira": {
        "pequenas": (-1.52, (-3.05, 0.02), "0,052", "0,39", 7.50,
                     [(49.09, 13.5), (49.94, 2.0), (60.21, 5.3), (77.89, 2.0), (80.53, 1.6), (89.90, 1.8), (89.90, 1.0), (89.90, 2.9), (97.94, 1.6), (129.90, 1.9)]),
        "médias": (-1.16, (-1.66, -0.67), "0,0006", "0,79", 6.23,
                   [(49.38, 5.4), (49.90, 6.2), (57.42, 4.3), (78.05, 2.7), (83.90, 2.8), (84.90, 3.9), (89.41, 2.1), (89.90, 3.0), (91.12, 2.2), (121.21, 2.3)]),
        "grandes": (-1.17, (-1.97, -0.36), "0,010", "0,58", 6.62,
                    [(49.37, 6.7), (49.90, 8.6), (57.67, 8.6), (76.30, 3.9), (83.90, 3.3), (84.90, 6.1), (89.78, 4.1), (89.90, 2.3), (89.90, 4.5), (116.26, 3.5)]),
    },
}

# Outros recortes: beta, ci, p, r2, combinações
OUTROS = {
    "Copo": {"Só SP": (-0.73, (-5.75, 4.29), "0,74", "0,01", 12), "Fora de SP": (1.67, (-2.00, 5.35), "0,32", "0,12", 33),
             "Meses sem promoção": (-0.67, (-2.50, 1.16), "0,42", "0,08", 37), "2025": (-1.54, (-6.63, 3.54), "0,50", "0,06", 12),
             "2026": (-0.41, (-3.19, 2.38), "0,75", "0,01", 33)},
    "Duralex": {"Só SP": (-0.89, (-3.33, 1.56), "0,43", "0,08", 12), "Fora de SP": (-3.31, (-4.48, -2.14), "0,0002", "0,84", 28),
                "Meses sem promoção": (-3.41, (-4.76, -2.06), "0,0004", "0,81", 40), "2025": (-4.11, (-5.91, -2.31), "0,0008", "0,78", 10),
                "2026": (-3.24, (-4.24, -2.24), "0,0001", "0,88", 30)},
    "Opaline": {"Só SP": (-2.12, (-3.21, -1.03), "0,0020", "0,72", 12), "Fora de SP": (-1.88, (-4.66, 0.90), "0,16", "0,23", 26),
                "Meses sem promoção": (-4.47, (-6.02, -2.91), "0,0002", "0,84", 35), "2025": (-2.80, (-3.96, -1.65), "0,0005", "0,80", 11),
                "2026": (-4.67, (-7.17, -2.17), "0,0026", "0,70", 27)},
    "Lasanheira": {"Só SP": (-1.76, (-3.39, -0.14), "0,04", "0,44", 11), "Fora de SP": (-0.67, (-2.67, 1.33), "0,46", "0,07", 21),
                   "Meses sem promoção": (-1.30, (-2.55, -0.05), "0,04", "0,42", 27), "2025": (-0.25, (-1.76, 1.26), "0,70", "0,03", 8),
                   "2026": (-1.55, (-2.59, -0.51), "0,0089", "0,60", 24)},
}

M5 = {"Copo": (-2.54, (-11.41, 7.81), "0,50", "0,025"), "Duralex": (-1.59, (-2.10, -0.44), "0,022", "0,006"),
      "Opaline": (1.53, (-14.42, 15.79), "0,84", "0,007"), "Lasanheira": (-0.68, (-1.90, 0.54), "0,21", "0,030")}

COMB = {"Copo": 45, "Duralex": 40, "Opaline": 38, "Lasanheira": 32}
EMPATE10 = {"Copo": -3.91, "Opaline": -1.94, "Duralex": -1.60, "Lasanheira": -1.54}

# Robustez (A2): sens, p, r2  na ordem das colunas
ROBUST_COLS = ["10 faixas (referência)", "Ponderada por lojas-mês", "12 faixas", "Sem o 1% de lojas-mês com mais volume",
               "Sem as unidades -AT", "Sem os dois", "Todos os pontos loja-mês (sem agrupar)",
               "M5 (cada loja comparada com ela mesma)", "Mediana da curva de especificações"]
ROBUST = {
    "Copo": [(-0.54, "0,60", "0,04"), (-0.47, "0,60", "0,04"), (-0.29, "0,78", "0,01"), (-0.95, "0,36", "0,10"), (-1.46, "0,28", "0,14"),
             (-1.26, "0,32", "0,12"), (-2.65, "< 0,0001", "0,06"), (-2.54, "0,50", "0,025"), (-1.45, None, None)],
    "Duralex": [(-3.41, "0,0004", "0,81"), (-3.04, "0,0022", "0,71"), (-3.57, "< 0,0001", "0,89"), (-3.15, "0,0004", "0,81"), (-3.34, "0,0004", "0,81"),
                (-3.18, "0,0004", "0,81"), (-2.84, "< 0,0001", "0,10"), (-1.59, "0,022", "0,006"), (-1.52, None, None)],
    "Opaline": [(-3.22, "0,0001", "0,88"), (-2.81, "< 0,0001", "0,90"), (-3.33, "0,0002", "0,77"), (-2.66, "0,0003", "0,82"), (-3.22, "0,0001", "0,88"),
                (-2.66, "0,0003", "0,82"), (-2.38, "< 0,0001", "0,17"), (1.53, "0,84", "0,007"), (0.33, None, None)],
    "Lasanheira": [(-1.44, "0,0010", "0,76"), (-1.39, "0,0002", "0,84"), (-1.51, "0,0019", "0,64"), (-1.31, "0,0009", "0,77"), (-1.45, "0,0010", "0,76"),
                   (-1.32, "0,0010", "0,76"), (-1.27, "< 0,0001", "0,19"), (-0.68, "0,21", "0,030"), (-0.89, None, None)],
}

# Base completa por rede (A6)
SO = {
    "Copo Americano (6.334 pontos × mês; geral 71 / 738 / 4.616)": [
        ("Tenda", "Atacarejo", "BASE SO", "loja", "preço de gôndola (PDV)", "102", "1,15", "64 / 1.356 / 127.010"),
        ("Atacadão", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "6.123", "1,20", "70 / 716 / 4.235"),
        ("Esperança", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "16", "1,28", "4.635 / 10.304 / 61.330"),
        ("Sendas (Assaí)", "Atacarejo", "BASE SO", "UF", "preço de gôndola (PDV)", "83", "1,39", "717 / 4.347 / 61.757"),
        ("Roldão", "Atacarejo", "BASE SO", "conta (total da rede)", "preço de gôndola (PDV)", "10", "1,55", "7.196 / 13.588 / 27.889")],
    "Duralex (4.233 pontos × mês; geral 4 / 21 / 76)": [
        ("Esperança", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "16", "7,56", "270 / 373 / 668"),
        ("Atakarejo", "Atacado", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "8,42", "595 / 974 / 1.224"),
        ("Grupo Pereira", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "168", "8,59", "3 / 16 / 52"),
        ("Sendas (Assaí)", "Atacarejo", "BASE SO", "UF", "preço de gôndola (PDV)", "62", "8,99", "17 / 80 / 579"),
        ("Atacadão", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "3.877", "9,11", "4 / 21 / 70"),
        ("BMP", "Lojas de UD", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "12", "9,18", "922 / 1.340 / 1.611"),
        ("Roldão", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "9,39", "30 / 126 / 330"),
        ("Tenda", "Atacarejo", "BASE SO", "loja", "preço de gôndola (PDV)", "61", "9,59", "5 / 31 / 1.104")],
    "Opaline (3.825 pontos × mês; geral 4 / 24 / 115)": [
        ("Esperança", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "16", "9,86", "202 / 444 / 722"),
        ("Sendas (Assaí)", "Atacarejo", "BASE SO", "UF", "preço de gôndola (PDV)", "68", "9,90", "9 / 176 / 1.470"),
        ("Atacadão", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "3.527", "9,99", "4 / 24 / 95"),
        ("Atakarejo", "Atacado", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "9,99", "938 / 1.148 / 1.411"),
        ("Tenda", "Atacarejo", "BASE SO", "loja", "preço de gôndola (PDV)", "61", "11,90", "7 / 28 / 1.015"),
        ("Grupo Pereira", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "104", "12,34", "4 / 18 / 107"),
        ("BMP", "Lojas de UD", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "12", "12,89", "932 / 1.664 / 4.446"),
        ("Americanas", "Magazine", "BASE SO", "conta (total da rede)", "preço de gôndola (PDV)", "9", "12,99", "630 / 1.133 / 2.149"),
        ("Roldão", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "13,22", "30 / 80 / 174")],
    "Lasanheira (2.566 pontos × mês; geral 1 / 3 / 15)": [
        ("Grupo Pereira", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "193", "57,50", "1 / 6 / 34"),
        ("Atacadão", "Atacarejo", "BASE SO", "loja", "faturamento ÷ peças", "2.216", "64,90", "1 / 3 / 12"),
        ("Tenda", "Atacarejo", "BASE SO", "loja", "preço de gôndola (PDV)", "54", "69,90", "2 / 6 / 66"),
        ("Esperança", "Atacarejo", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "16", "75,08", "14 / 26 / 153"),
        ("Sendas (Assaí)", "Atacarejo", "BASE SO", "UF", "preço de gôndola (PDV)", "65", "82,40", "1 / 8 / 40"),
        ("Roldão", "Atacarejo", "BASE SO", "conta (total da rede)", "preço de gôndola (PDV)", "10", "88,25", "4 / 16 / 30")],
}
PDV = "PDV atendido pelo distribuidor"
ST = {
    "Copo Americano (4.926 pontos × mês; geral 24 / 72 / 720)": [
        ("Martins", "Atacado", "BASE SO", "CD", "faturamento ÷ peças", "27", "0,90", "9.893 / 322.440 / 870.346"),
        ("Tambasa", "Atacado", "BASE SO", "UF", "faturamento ÷ peças", "57", "0,90", "2.362 / 11.520 / 368.582"),
        ("Grand Marca Caruaru (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "700", "0,98", "24 / 144 / 1.512"),
        ("Vision PR (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "530", "0,99", "24 / 72 / 480"),
        ("Marfim Jaboatão (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "1.938", "1,00", "24 / 72 / 480"),
        ("Marfim PB (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "1.640", "1,00", "24 / 72 / 240"),
        ("Atacadão, CD 111-MATRIZ CD/AT", "Atacarejo", "BASE SO", "CD", "preço de gôndola (PDV)", "16", "1,07", "120.965 / 341.856 / 650.916"),
        ("Paraty", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "17", "1,11", "7.267 / 21.840 / 44.966")],
    "Duralex (3.473 pontos × mês; geral 24 / 24 / 168)": [
        ("Tambasa", "Atacado", "BASE SO", "UF", "faturamento ÷ peças", "57", "3,52", "1.214 / 5.328 / 68.606"),
        ("Paraty", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "17", "3,65", "8.059 / 19.200 / 29.112"),
        ("Modenuti", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "3,74", "39.242 / 47.700 / 58.577"),
        ("Martins", "Atacado", "BASE SO", "CD", "faturamento ÷ peças", "27", "3,74", "1.584 / 17.280 / 50.582"),
        ("Vision PR (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "609", "3,88", "24 / 24 / 240"),
        ("Grand Marca Caruaru (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "313", "3,96", "24 / 24 / 187"),
        ("Marfim PB (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "661", "3,98", "24 / 24 / 48"),
        ("Scotti (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "659", "4,04", "24 / 24 / 120"),
        ("Marfim Jaboatão (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "985", "4,24", "24 / 24 / 110"),
        ("Vision Campo Grande MS (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "133", "4,28", "24 / 48 / 240")],
    "Opaline (2.072 pontos × mês; geral 24 / 24 / 142)": [
        ("Tambasa", "Atacado", "BASE SO", "UF", "faturamento ÷ peças", "56", "4,90", "264 / 1.680 / 26.112"),
        ("Martins", "Atacado", "BASE SO", "CD", "faturamento ÷ peças", "26", "5,04", "2.844 / 18.876 / 56.640"),
        ("Paraty", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "17", "5,15", "14.102 / 21.864 / 36.624"),
        ("Vision PR (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "474", "5,99", "24 / 24 / 240"),
        ("Grand Marca Caruaru (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "177", "6,00", "24 / 24 / 48"),
        ("Marfim PB (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "443", "6,06", "24 / 24 / 48"),
        ("Marfim Jaboatão (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "652", "6,34", "24 / 24 / 48"),
        ("Modenuti", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "7,16", "7.930 / 10.500 / 13.774"),
        ("Vision Campo Grande MS (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "72", "7,26", "24 / 24 / 120"),
        ("Scotti (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "140", "7,93", "24 / 24 / 48")],
    "Lasanheira (2.114 pontos × mês; geral 4 / 8 / 44)": [
        ("Vision PR (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "553", "33,84", "2 / 6 / 60"),
        ("Martins", "Atacado", "BASE SO", "CD", "faturamento ÷ peças", "23", "36,94", "121 / 528 / 3.122"),
        ("Paraty", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "12", "38,47", "112 / 416 / 883"),
        ("Vision Campo Grande MS (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "85", "39,65", "2 / 4 / 20"),
        ("Scotti (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "1.326", "40,18", "4 / 8 / 40"),
        ("Modenuti", "Distribuidor", "BASE SO", "conta (total da rede)", "faturamento ÷ peças", "10", "41,40", "1.193 / 2.114 / 5.122"),
        ("Marfim PB (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "35", "41,54", "1 / 2 / 6"),
        ("Marfim Jaboatão (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "20", "46,16", "2 / 4 / 12"),
        ("Tambasa", "Atacado", "BASE SO", "UF", "faturamento ÷ peças", "41", "47,94", "4 / 16 / 520"),
        ("Grand Marca Caruaru (Mtrix)", "Distribuidor", "Mtrix", PDV, "faturamento ÷ peças", "9", "48,08", "1 / 2 / 8")],
}

# Footers (copiados inteiros do prompt)
F_GERAL = ("Fonte: base conciliada, BASE SO (venda no caixa das lojas do Atacadão, marcada como sell-out, com consumidor final e pequeno comerciante sem separação; empresa fonte não informada); coleta Involves de preço de gôndola (PDV); SAP Nadir (sell-in) para a margem; sell-through (CD e Mtrix) não entra nas contas | Elaboração: DOC Consulting. Período: volume e preço em SP de abr/25 a mai/26 (sem jul e ago/25) e nas demais regiões de dez/25 a mai/26; margem SAP de jun/25 a mai/26.")
F_BASES = ("Fonte: base conciliada com fonte e tipo de dado, conciliada pela DOC: BASE SO (marcada como sell-out: venda no caixa de lojas, contas e UFs, que no atacarejo inclui o pequeno comerciante; sell-through: CD, distribuidores e atacados; empresa fonte não informada) e Mtrix (sell-through dos distribuidores ao varejo); coleta Involves de preço de gôndola (PDV), bruta e sanitizada; SAP Nadir (sell-in) e cascata de margem SAP (sell-in, Net Net); Excel v8.1 (02/10/2026), abas Bases de dados e Sanitização | Elaboração: DOC Consulting. Período: BASE SO de jan/25 a mai/26; coleta Involves de abr/25 a mai/26; SAP de jan/25 a jun/26; Mtrix em jul/24 e de jan a jul de 2025 e 2026.")
CAIXA = "BASE SO (venda no caixa por loja e mês das lojas do Atacadão, marcada como sell-out na base, com consumidor final e pequeno comerciante sem separação; sem o CD 111-MATRIZ CD/AT, que é sell-through; empresa fonte não informada"
CAIXA2 = "BASE SO (venda no caixa das lojas do Atacadão, marcada como sell-out na base, com consumidor final e pequeno comerciante sem separação; sem o CD 111-MATRIZ CD/AT, que é sell-through; empresa fonte não informada"
PER_VP = "Período: SP em 12 meses de abr/25 a mai/26 (sem jul e ago/25); demais regiões de dez/25 a mai/26."
PER_VPM = "Período: volume e preço em SP de abr/25 a mai/26 (sem jul e ago/25) e nas demais regiões de dez/25 a mai/26; margem SAP de jun/25 a mai/26."

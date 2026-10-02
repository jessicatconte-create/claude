import math
from lib import *
from data import *

REP = ("A conta supõe repasse integral: a baixa no preço Nadir chega inteira, em %, ao preço de gôndola (PDV). O repasse não foi medido; "
       "sem repasse, o volume não vem e a baixa vira só perda.")
F_MARG = (f"Fonte: base conciliada, {CAIXA2}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; margem SAP Nadir (sell-in; "
          f"margem bruta ÷ Net Net); Mtrix (sell-through) não entra; cálculo DOC das faixas nacionais de preço")


def fx(v):
    """tick label for R$ axes"""
    return num(v, 0) if v >= 5 else num(v, 2)


def fy(v):
    return num(v, 0) if v >= 1 else num(v, 1)


def line_pts(a, b, p0, p1):
    return [(p0, math.exp(a + b * math.log(p0))), (p1, math.exp(a + b * math.log(p1)))]


# ------------------------------------------------------------------ 10 sensibilidade
PANEL_CFG = {
    "Copo": dict(x=(0.92, 1.70), y=(800, 6500), xt=[1.0, 1.2, 1.4, 1.6], yt=[1000, 2000, 5000]),
    "Duralex": dict(x=(6.6, 11.6), y=(8, 100), xt=[7, 8, 9, 10, 11], yt=[10, 20, 50, 100]),
    "Opaline": dict(x=(5.9, 13.0), y=(10, 280), xt=[6, 8, 10, 12], yt=[10, 20, 50, 100, 200]),
    "Lasanheira": dict(x=(45, 128), y=(1.4, 12), xt=[50, 70, 100, 120], yt=[2, 5, 10]),
}


def s10():
    sv = Svg(100, 252, 1190, 706, "Volume médio por loja nas 10 faixas nacionais de preço, com a reta log-log e a faixa de 95%")
    # legenda
    sv.circle(8, 12, 7, BLUE); sv.text(22, 17, "Faixa com maioria de combinações em SP", 14, INK)
    sv.circle(318, 12, 7, WHITE, BLUE, 2); sv.text(332, 17, "Maioria de outras regiões", 14, INK)
    sv.line(528, 12, 568, 12, INK, 2.5); sv.text(576, 17, "Reta log-log", 14, INK)
    sv.line(680, 12, 720, 12, G1, 2, "6 5"); sv.text(728, 17, "Limites da faixa de 95%", 14, INK)
    sv.circle(915, 12, 4, G3); sv.circle(932, 12, 9, G3); sv.text(948, 17, "Tamanho = lojas-mês", 14, INK)
    for k, it in enumerate(ITEMS):
        c, r = k % 2, k // 2
        px, py = c * 600, 34 + r * 336
        cfg = PANEL_CFG[it]; nat = NAT[it]
        sx = Scale(cfg["x"][0], cfg["x"][1], px + 78, px + 580, log=True)
        sy = Scale(cfg["y"][0], cfg["y"][1], py + 268, py + 38, log=True)
        lab = f"{it} · sensibilidade {num(nat['b'], 2)} · p {nat['p']} · R² {nat['r2']}" + (" · sem leitura" if it == "Copo" else "")
        sv.text(px + 78, py + 22, lab, 16, INK if it != "Copo" else G1, bold=True)
        axes(sv, sx, sy, cfg["xt"], cfg["yt"], fx, fy, tick_size=14)
        sv.text((sx.r0 + sx.r1) / 2, py + 306, "Preço de gôndola (PDV) por peça (R$, escala log)", 13, G1, "middle")
        sv.text(px + 18, (sy.r0 + sy.r1) / 2, "Peças por loja-mês (escala log)", 13, G1, "middle", rotate=-90)
        (p0, v0, l0a, l0b), (p1, v1, l1a, l1b) = nat["ends"]
        sv.line(sx(p0), sy(l0a), sx(p1), sy(l1a), G1, 2, "6 5")
        sv.line(sx(p0), sy(l0b), sx(p1), sy(l1b), G1, 2, "6 5")
        sv.line(sx(p0), sy(v0), sx(p1), sy(v1), INK, 2.5)
        for f in FAIXAS[it]:
            rad = 3 + math.sqrt(f[5]) * 0.45
            if f[7] > 50:
                sv.circle(sx(f[1]), sy(f[6]), rad, BLUE, WHITE, 1)
            else:
                sv.circle(sx(f[1]), sy(f[6]), rad, WHITE, BLUE, 2)
    rows = [(it, num(NAT[it]["b"], 2), f"{num(NAT[it]['ci'][0], 2)} a {num(NAT[it]['ci'][1], 2)}", NAT[it]["p"], NAT[it]["r2"], NAT[it]["cv"])
            for it in ["Duralex", "Opaline", "Lasanheira", "Copo"]]
    tbl = mini_table(rows, [86, 52, 110, 58, 40, 44], 14, head=["Item", "Sensib.", "Faixa de 95%", "p-valor", "R²", "CV"],
                     colors=[INK, INK, INK, G1])
    body = "".join([
        P("Volume médio por loja nas 10 faixas nacionais de preço, com a reta log-log e a faixa de 95%", 100, 216, 1050, 18, INK, bold=True),
        seals(["PARCIAL"], 1290, 212),
        sv.render(),
        rail([("Como ler", p("Sensibilidade do volume ao preço −3,41 = 1% a mais no preço de gôndola (PDV), cerca de 3,4% a menos de volume "
                             "por loja, na média nacional. CV = distância média dos pontos à reta.", 16), "info"),
              ("Reta nacional, com a faixa de 95%", tbl + p("Copo: faixa de 95% passa pelo zero, sem leitura.", 14, G1), "info"),
              ("O que decidir", p("Usar como ordem de grandeza, nunca sozinha: ver os recortes (slides 11 e 12).", 18, bold=True), "decide")]),
    ])
    notes = ("Esta é a tendência que o agrupamento mostra, com o grau de confiança. No Duralex, 1% a mais no preço vem com cerca de 3,4% a menos "
             "de volume por loja, e a faixa de 95% vai de 2,1% a 4,8%. A Opaline é parecida. A Lasanheira responde menos, cerca de 1,4% para cada "
             "1%. No Copo, a reta é quase plana e a faixa de 95% passa pelo zero: não há leitura. Esses números são a média nacional e misturam "
             "regiões; por isso, a seguir, os recortes.\n\nNúmeros: Duralex −3,41 (faixa de 95%: −4,76 a −2,06; p-valor 0,0004; R² 0,81; pontos a "
             "27% da reta). Opaline −3,22 (−4,19 a −2,24; p 0,0001; R² 0,88; 26%). Lasanheira −1,44 (−2,10 a −0,79; p 0,0010; R² 0,76; 25%). "
             "Copo −0,54 (−2,80 a 1,73; p 0,60; R² 0,04; 47%): sem leitura. Gráfico refeito em versão editável com os pontos, retas e limites "
             "da seção de dados (equivalente ao Gráfico 3 em PNG).")
    sub = ("No agregado nacional, Duralex e Opaline respondem forte ao preço, a Lasanheira responde menos e o Copo não mostra relação; os "
           "pontos ficam, em média, a 25% a 27% da reta.")
    foot = (f"Fonte: base conciliada, {CAIXA}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; Mtrix (sell-through) e SAP "
            f"(sell-in) não entram; cálculo DOC: reta log-log nas 10 faixas nacionais de preço | Elaboração: DOC Consulting. {PER_VP}")
    return slide("s10", "Sensibilidade", sub, body, foot, "10", notes)


# ------------------------------------------------------------------ 11 retas por porte
PORTE_CFG = {
    "Duralex": dict(x=(6.6, 11.6), y=(4.5, 90), xt=[7, 8, 9, 10, 11], yt=[5, 10, 20, 50]),
    "Opaline": dict(x=(5.6, 13.2), y=(7, 260), xt=[6, 8, 10, 12], yt=[10, 20, 50, 100, 200]),
    "Lasanheira": dict(x=(45, 140), y=(0.8, 16), xt=[50, 70, 100], yt=[1, 2, 5, 10]),
}
PCOL = {"pequenas": G3, "médias": G1, "grandes": INK}


def s11():
    sv = Svg(100, 252, 1190, 706, "Retas log-log por porte de loja contra a reta nacional")
    x = 0
    for k, lab in [("pequenas", "Lojas pequenas"), ("médias", "Lojas médias"), ("grandes", "Lojas grandes")]:
        sv.line(x, 12, x + 32, 12, PCOL[k], 3); sv.circle(x + 16, 12, 4, PCOL[k]); sv.text(x + 40, 17, lab, 14, INK); x += 40 + len(lab) * 7.5 + 26
    sv.line(x, 12, x + 32, 12, BLUE, 3, "7 5"); sv.text(x + 40, 17, "Reta nacional", 14, INK)
    for k, it in enumerate(["Duralex", "Opaline", "Lasanheira"]):
        px = k * 400
        cfg = PORTE_CFG[it]
        sx = Scale(cfg["x"][0], cfg["x"][1], px + 62, px + 380, log=True)
        sy = Scale(cfg["y"][0], cfg["y"][1], px * 0 + 470, 70, log=True)
        sv.text(px + 62, 56, it, 18, INK, bold=True)
        axes(sv, sx, sy, cfg["xt"], cfg["yt"], fx, fy, tick_size=14)
        sv.text((sx.r0 + sx.r1) / 2, 512, "Preço de gôndola (PDV) por peça", 13, G1, "middle")
        sv.text((sx.r0 + sx.r1) / 2, 528, "(R$, escala log)", 13, G1, "middle")
        sv.text(px + 12, 270, "Peças por loja-mês (escala log)", 13, G1, "middle", rotate=-90)
        nat = NAT[it]
        (p0, v0, *_), (p1, v1, *_) = nat["ends"]
        sv.line(sx(p0), sy(v0), sx(p1), sy(v1), BLUE, 3, "7 5")
        ly = 556
        for pk in ["grandes", "médias", "pequenas"]:
            b, ci, pv, r2, a, pts = PORTE[it][pk]
            prices = [q for q, _ in pts]
            (q0, w0), (q1, w1) = line_pts(a, b, min(prices), max(prices))
            sv.line(sx(q0), sy(w0), sx(q1), sy(w1), PCOL[pk], 2.5)
            for q, w in pts:
                sv.circle(sx(q), sy(w), 3.6, PCOL[pk])
            sv.line(px + 62, ly - 5, px + 84, ly - 5, PCOL[pk], 3)
            sv.text(px + 92, ly, f"{pk.capitalize()} {num(b, 2, sign=True)} (p {pv}; R² {r2})", 14, INK)
            ly += 22
        sv.line(px + 62, ly - 5, px + 84, ly - 5, BLUE, 3, "5 3")
        sv.text(px + 92, ly, f"Nacional {num(nat['b'], 2)} (p {nat['p']}; R² {nat['r2']})", 14, BLUE, bold=True)
    sv.text(62, 686, "Copo: sem leitura em nenhum porte. Porte: terços das lojas do Atacadão pelo faturamento da venda no caixa (marcada como "
                     "sell-out) de todos os itens Nadir na BASE SO.", 13, G1)

    def big(v, lab):
        return (f'<div style="display:flex;flex-direction:row;gap:16px;align-items:center">{p(v, 40, BLUE, bold=True, lh=1.0, extra="width:110px;")}'
                f'{p(lab, 15, INK, lh=1.3, extra="width:300px;")}</div>')
    body = "".join([
        P("Retas log-log por porte de loja contra a reta nacional", 100, 216, 1000, 18, INK, bold=True),
        seals(["COMPROVADA"], 1290, 212),
        sv.render(),
        rail([("Grandes ÷ pequenas, no mesmo preço", big("3,1×", "Duralex, em R$ 9,06: 34,5 contra 11,1 peças por loja-mês")
               + big("3,1×", "Opaline, em R$ 10,57: 39,2 contra 12,8") + big("1,9×", "Lasanheira, em R$ 84,40: 4,2 contra 2,2"), "info"),
              ("Inclinação muda", p("Sensibilidade do volume ao preço, com a faixa de 95% no anexo A3: na Opaline, as lojas pequenas quase não "
                                    "respondem (+0,24; p 0,64; R² 0,03) e as grandes respondem forte (−2,78; p 0,0003; R² 0,82).", 15), "info"),
              ("O que decidir", p("Não aplicar a reta nacional a toda loja: o porte muda altura e inclinação.", 18, bold=True), "decide")]),
    ])
    notes = ("Quando voltamos aos recortes mais específicos, as retas mudam de posição. No mesmo preço, a loja grande vende três vezes o que vende "
             "a pequena, e a inclinação também muda: na Opaline, as lojas pequenas praticamente não respondem ao preço, e as grandes respondem forte. "
             "Por isso a reta nacional não pode ser lida como verdade para toda loja.\n\nFaixas de 95%: Duralex pequenas −1,45 (−3,45 a 0,54), médias "
             "−1,71 (−2,76 a −0,66), grandes −2,32 (−3,64 a −1,00). Opaline pequenas +0,24 (−0,90 a 1,38), médias −1,56 (−2,14 a −0,97), grandes "
             "−2,78 (−3,85 a −1,71). Lasanheira pequenas −1,52 (−3,05 a 0,02; p 0,052), médias −1,16 (−1,66 a −0,67), grandes −1,17 (−1,97 a "
             "−0,36). Copo: pequenas −1,38 (p 0,49; R² 0,06), médias +1,62 (p 0,12; R² 0,27), grandes +1,57 (p 0,16; R² 0,23), todas com a faixa "
             "de 95% passando pelo zero.")
    sub = ("Quando voltamos aos recortes, as retas mudam de altura e de inclinação: no mesmo preço, a loja grande vende 3 vezes o que vende a "
           "pequena no Duralex e na Opaline.")
    foot = (f"Fonte: base conciliada, {CAIXA}; porte pelo faturamento da venda no caixa); preço de gôndola (PDV) da coleta Involves por "
            f"macrorregião × mês; Mtrix (sell-through) e SAP (sell-in) não entram; cálculo DOC das faixas nacionais de preço por porte de loja | "
            f"Elaboração: DOC Consulting. {PER_VP}")
    return slide("s11", "Retas por recorte", sub, body, foot, "11", notes)


# ------------------------------------------------------------------ 12 forest
RECORTES = ["Nacional (10 faixas)", "Lojas pequenas", "Lojas médias", "Lojas grandes", "Só SP", "Fora de SP",
            "Meses sem promoção", "2025", "2026", "Cada loja comparada com ela mesma (M5)"]


def recorte_rows(it):
    n = NAT[it]
    rows = [(n["b"], n["ci"], n["p"], n["r2"])]
    for k in ["pequenas", "médias", "grandes"]:
        b, ci, pv, r2, *_ = PORTE[it][k]
        rows.append((b, ci, pv, r2))
    for k in ["Só SP", "Fora de SP", "Meses sem promoção", "2025", "2026"]:
        b, ci, pv, r2, _ = OUTROS[it][k]
        rows.append((b, ci, pv, r2))
    rows.append(M5[it])
    return rows


def s12():
    sv = Svg(100, 244, 1190, 724, "Sensibilidade por recorte com a faixa de 95%, contra o empate da baixa de 10%")
    sv.hatch_def("h12")
    # legenda
    sv.circle(8, 12, 7, BLUE); sv.text(20, 17, "Nacional", 14, INK)
    sv.circle(108, 12, 6, G1); sv.text(120, 17, "Recorte", 14, INK)
    sv.line(200, 12, 240, 12, G1, 3); sv.text(248, 17, "Faixa de 95%", 14, INK)
    sv.line(372, 2, 372, 22, INK, 2, "4 3"); sv.text(380, 17, "Empate da baixa de 10%", 14, INK)
    sv.rect(560, 4, 30, 16, "url(#h12)"); sv.text(598, 17, "A baixa de 10% perde margem", 14, INK)
    sv.text(830, 17, "▸ barra passa do eixo", 14, INK)
    order = ["Copo", "Lasanheira", "Duralex", "Opaline"]
    top, rh = 82, 58
    for i, r in enumerate(RECORTES):
        y = top + i * rh
        words = r.split(" ")
        if len(r) > 22:
            sv.text(0, y + 18, "Cada loja comparada", 14, INK, bold=(i == 0))
            sv.text(0, y + 36, "com ela mesma (M5)", 14, INK)
        else:
            sv.text(0, y + 24, r, 14, BLUE if i == 0 else INK, bold=(i == 0))
        if i:
            sv.line(0, y, 1190, y, GRID)
    for k, it in enumerate(order):
        cx = 192 + k * 250
        sx = Scale(-8, 4, cx + 14, cx + 236)
        emp = EMPATE10[it]
        sv.text(cx + 125, 50, it, 17, INK, "middle", bold=True)
        sv.text(cx + 125, 70, f"empate {num(emp, 2)}", 13, G1, "middle")
        sv.rect(sx(emp), top, sx(4) - sx(emp), rh * 10, "url(#h12)", opacity=0.9)
        sv.line(sx(0), top, sx(0), top + rh * 10, G3, 1)
        sv.line(sx(emp), top - 4, sx(emp), top + rh * 10, INK, 2, "5 4")
        for t in [-8, -4, 0, 4]:
            sv.text(sx(t), top + rh * 10 + 20, num(t, 0, sign=True) if t else "0", 13, G1, "middle")
        sv.line(sx(-8), top + rh * 10, sx(4), top + rh * 10, G2)
        for i, (b, (lo, hi), pv, r2) in enumerate(recorte_rows(it)):
            y = top + i * rh + 20
            col = BLUE if i == 0 else G1
            l, h = max(lo, -8), min(hi, 4)
            sv.line(sx(l), y, sx(h), y, col, 3, cap="round")
            if lo < -8:
                sv.add(f'<path d="M{sx(-8)-2:.1f} {y} L{sx(-8)+8:.1f} {y-6} L{sx(-8)+8:.1f} {y+6} Z" fill="{col}"/>')
            if hi > 4:
                sv.add(f'<path d="M{sx(4)+2:.1f} {y} L{sx(4)-8:.1f} {y-6} L{sx(4)-8:.1f} {y+6} Z" fill="{col}"/>')
            sv.circle(sx(b), y, 7 if i == 0 else 6, col, WHITE, 1.5)
            sv.rect(cx + 50, y + 15, 150, 15, WHITE, rx=3, opacity=0.9)
            sv.text(cx + 125, y + 26, f"{num(b, 2, sign=True)} · p {pv} · R² {r2}", 12, BLUE if i == 0 else G1, "middle", bold=(i == 0))
    sv.text(192 + 500, top + rh * 10 + 42, "Sensibilidade (variação % do volume para 1% de preço), de −8 a +4", 14, G1, "middle")
    sv.text(0, top + rh * 10 + 42, "Eixo Y: recorte", 13, G1)
    rules = ("<ol style=\"font-size:15px;line-height:1.35;color:#14171F;padding:0px 0px 0px 22px\">"
             "<li>Usar a faixa, não o ponto: decidir olhando o pior e o melhor recorte.</li>"
             "<li>Só confiar no sinal que aparece na maioria dos recortes e também quando cada loja é comparada com ela mesma.</li>"
             "<li>Não usar a reta fora da faixa de preço observada: Duralex R$ 6,92 a R$ 10,90; Opaline R$ 6,22 a R$ 12,23; Lasanheira R$ 49,34 a R$ 117,48.</li>"
             "<li>Confirmar com teste antes de mudar a tabela.</li></ol>")
    pays = mini_table([("Copo", "0 de 8"), ("Lasanheira", "2 de 8"), ("Opaline", "5 de 8"), ("Duralex", "6 de 8")], [150, 120], 16)
    body = "".join([
        P("Sensibilidade do volume ao preço por recorte, com a faixa de 95%, contra o empate da baixa de 10%", 100, 210, 1100, 18, INK, bold=True),
        seals(["PARCIAL"], 1290, 206),
        sv.render(),
        rail([("Como usar com moderação", rules, "info"),
              ("Recortes que pagam a baixa de 10%", pays, "info"),
              ("O que decidir", p("Duralex e Opaline vão para teste antes de qualquer mudança de tabela.", 18, bold=True), "decide")], top=206, gap=12),
    ])
    notes = ("Este é o slide do \"com moderação\". O número nacional é útil para pensar a conta, mas não é verdade absoluta: em cada item, a "
             "sensibilidade muda bastante conforme o recorte. Só no Copo todos os recortes ficam do lado em que a baixa perde margem. No Duralex e "
             "na Opaline, parte dos recortes paga a baixa e parte não, e a comparação de cada loja com ela mesma fica no empate ou do lado da "
             "perda.\n\nEmpate da baixa de 10%: Copo −3,91; Opaline −1,94; Duralex −1,60; Lasanheira −1,54. M5 (efeito de loja e de mês): Copo "
             "−2,54 (faixa de 95%: −11,41 a 7,81; p 0,50; R² dentro da loja 0,025); Duralex −1,59 (−2,10 a −0,44; p 0,022; R² 0,006); Opaline +1,53 "
             "(−14,42 a 15,79; p 0,84; R² 0,007); Lasanheira −0,68 (−1,90 a 0,54; p 0,21; R² 0,030). No Duralex, \"Meses sem promoção\" é igual ao "
             "Nacional (nenhuma combinação com promoção). Recortes completos no anexo A3. A margem usada no empate é a margem SAP; a conta supõe "
             "repasse integral ao preço de gôndola (PDV), que não foi medido: sem repasse, o volume não vem e a baixa vira só perda.")
    sub = ("A sensibilidade nacional é um ponto dentro de uma faixa larga: só o Copo fica todo do lado da perda; no Duralex e na Opaline, os "
           "recortes cruzam o empate.")
    foot = (f"{F_MARG}; M5 do Excel v8.1 (02/10/2026), aba Resumo | Elaboração: DOC Consulting. {PER_VPM}").replace(
        "não entra; cálculo DOC", "não entra; cálculo DOC").replace("margem SAP Nadir (sell-in; margem bruta ÷ Net Net);",
                                                                    "margem SAP Nadir (sell-in; margem bruta ÷ Net Net) para o empate;")
    return slide("s12", "Com moderação", sub, body, foot, "12", notes)


# ------------------------------------------------------------------ 13 volume e margem
def s13():
    sv = Svg(100, 252, 1190, 706, "Variação da margem bruta total numa baixa de 10%, conforme o volume sobe")
    cols = {"Copo": (BLUE, 3.5), "Duralex": (INK, 2.5), "Opaline": (G1, 2.5), "Lasanheira": (G2, 3)}
    x = 0
    for it in ITEMS:
        c, w = cols[it]
        sv.line(x, 12, x + 32, 12, c, w, "9 5" if it == "Lasanheira" else None); sv.text(x + 40, 17, it, 14, INK); x += 40 + len(it) * 8 + 24
    sv.circle(x + 6, 12, 6, WHITE, INK, 2); sv.text(x + 18, 17, "Volume necessário para empatar", 14, INK); x += 250
    sv.rect(x, 4, 24, 16, G4); sv.text(x + 30, 17, "Exemplo ilustrativo de +15%", 14, INK)
    sx = Scale(0, 60, 90, 1170)
    sy = Scale(-35, 30, 620, 60)
    sv.rect(sx(14), 60, sx(16) - sx(14), 560, G4)
    sv.text(sx(15), 78, "exemplo ilustrativo", 13, G1, "middle", italic=True)
    axes(sv, sx, sy, list(range(0, 61, 10)), list(range(-30, 31, 10)), lambda t: (f"+{t}%" if t else "0%"),
         lambda t: (num(t, 0, sign=True) + "%" if t else "0%"), "Variação do volume (%), de 0% a +60%",
         "Variação da margem bruta total (%), de −35% a +30%", 15, ytitle_dx=60)
    sv.line(sx(0), sy(0), sx(60), sy(0), INK, 1.5)
    need = {}
    for it in ITEMS:
        m = MARGIN[it]
        k = (m - 0.1) / m
        vmax = min(60, (1.3 / k - 1) * 100)
        c, w = cols[it]
        sv.line(sx(0), sy((k - 1) * 100), sx(vmax), sy(((1 + vmax / 100) * k - 1) * 100), c, w, "9 5" if it == "Lasanheira" else None)
        need[it] = (1 / k - 1) * 100
    lab = {"Lasanheira": (14, 20, "end"), "Duralex": (14, 12, "end"), "Opaline": (14, 4, "end"), "Copo": (47, 8, "end")}
    tx = {"Lasanheira": "Lasanheira +17,6%", "Duralex": "Duralex +18,3%", "Opaline": "Opaline +22,6%", "Copo": "Copo +51,0%"}
    for it in ITEMS:
        vx = need[it]
        lx, ly, anc = lab[it]
        sv.line(sx(vx), sy(0), sx(lx) + 4, sy(ly) + 4, G2, 1)
        sv.circle(sx(vx), sy(0), 6, WHITE, cols[it][0] if it != "Lasanheira" else G1, 2.5)
        sv.text(sx(lx), sy(ly) + 5, tx[it], 15, INK, anc, bold=True)
    sv.text(90, 700, "Repasse integral suposto ao preço de gôndola (PDV). Margem SAP: Copo 29,6%; Duralex 64,6%; Opaline 54,2%; Lasanheira 66,8%.", 13, G1)
    formula = (f'<div style="background:{WHITE};border-radius:12px;padding:12px 14px">'
               f'{p("Margem total depois ÷ margem total antes = (1 + variação do volume) × (margem % + variação do preço) ÷ margem %", 16, INK, bold=True)}</div>')
    ex = (f'<div style="display:flex;flex-direction:row">{seal_p("EXEMPLO ILUSTRATIVO")}</div>'
          + p("Não é resultado da Nadir: mostra a conta. Preço −10% e volume +15%: Copo −23,9%; Opaline −6,2%; Duralex −2,8%; Lasanheira −2,2%. "
              "Copo: 1,15 × (29,6% − 10%) ÷ 29,6% = 0,761.", 15))
    body = "".join([
        P("Variação da margem bruta total numa baixa de 10%, conforme o volume sobe", 100, 216, 1000, 18, INK, bold=True),
        seals(["COMPROVADA", "EXEMPLO ILUSTRATIVO"], 1290, 212),
        sv.render(),
        rail([("A conta", formula + ex, "info"),
              ("Repasse", p("Supõe repasse integral ao preço de gôndola (PDV), não medido. Sem repasse, a baixa de 10% tira de −15,0% a −33,8% da margem.", 15), "info"),
              ("O que decidir", p("Com +15% de volume, nenhum dos quatro empata: só seguir onde o volume esperado passar do necessário.", 17, bold=True), "decide")]),
    ])
    notes = ("Agora a pergunta de negócio. Primeiro, como pensar a conta: o exemplo de 10% de baixa com 15% a mais de volume não é resultado da "
             "Nadir, serve para mostrar o raciocínio. A baixa tira margem de cada peça; o volume precisa compensar. Quanto mais fina a margem, mais "
             "volume a baixa precisa comprar: o Copo precisa de 51% a mais; os outros, de 18% a 23%. Com 15% a mais, nenhum dos quatro empata.\n\n"
             "Volume necessário para manter a margem bruta total, com repasse integral: baixa de 5%: Copo +20,3%, Opaline +10,2%, Duralex +8,4%, "
             "Lasanheira +8,1%; baixa de 10%: Copo +51,0%, Opaline +22,6%, Duralex +18,3%, Lasanheira +17,6%; baixa de 15%: Copo +102,7%, Opaline "
             "+38,3%, Duralex +30,2%, Lasanheira +29,0%. Sem repasse, a baixa de 10% tira da margem: Copo −33,8%, Opaline −18,5%, Duralex −15,5%, "
             "Lasanheira −15,0%. Sensibilidade de empate na baixa de 10%: Copo −3,91; Opaline −1,94; Duralex −1,60; Lasanheira −1,54. "
             "Sensibilidade do volume ao preço, faixa de 95%, p-valor e R²: não se aplica neste slide (é aritmética da margem SAP, sem estimativa). "
             + REP)
    sub = ("Uma baixa só se paga se o volume extra cobrir a margem que sai de cada peça: numa baixa de 10%, o Copo precisa de +51% de volume e "
           "os outros três de +18% a +23%.")
    foot = ("Fonte: margem SAP Nadir (sell-in; margem bruta ÷ Net Net, cascata de margem SAP, Atacadão); cálculo DOC com repasse integral ao preço "
            "de gôndola (PDV); exemplo ilustrativo DOC, sem dado de volume | Elaboração: DOC Consulting. Período: margem SAP de jun/25 a mai/26.")
    return slide("s13", "Volume e margem", sub, body, foot, "13", notes)


# ------------------------------------------------------------------ 14 bullet
BUL = [("Copo", 51.0, 5.8, (-16.6, 34.4), (-16.2, 17.7), 30.6, "sensibilidade do volume ao preço −0,54 · faixa de 95% −2,80 a 1,73 · p 0,60 · R² 0,04 · sem leitura"),
       ("Lasanheira", 17.6, 16.4, (8.7, 24.8), (2.7, 20.4), 7.4, "sensibilidade −1,44 · faixa de 95% −2,10 a −0,79 · p 0,0010 · R² 0,76"),
       ("Duralex", 18.3, 43.2, (24.2, 65.2), (9.8, 54.2), 18.2, "sensibilidade −3,41 · faixa de 95% −4,76 a −2,06 · p 0,0004 · R² 0,81"),
       ("Opaline", 22.6, 40.3, (26.6, 55.6), (-2.5, 63.6), -14.9, "sensibilidade −3,22 · faixa de 95% −4,19 a −2,24 · p 0,0001 · R² 0,88")]


def s14():
    sv = Svg(100, 252, 1190, 706, "Volume que a baixa de 10% traz contra o volume que ela precisa trazer")
    sv.rect(0, 4, 30, 16, G4); sv.text(36, 17, "Volume necessário", 14, INK)
    sv.circle(186, 12, 7, BLUE); sv.text(198, 17, "Esperado (nacional)", 14, INK)
    sv.line(350, 12, 390, 12, BLUE, 4); sv.text(396, 17, "Faixa de 95%", 14, INK)
    sv.line(510, 12, 550, 12, G1, 2); sv.line(510, 6, 510, 18, G1, 2); sv.line(550, 6, 550, 18, G1, 2)
    sv.text(556, 17, "Mín. a máx. dos 8 recortes", 14, INK)
    sv.diamond(770, 12, 8, INK); sv.text(784, 17, "M5 (cada loja comparada com ela mesma)", 14, INK)
    sx = Scale(-20, 70, 150, 1170)
    top, rh = 70, 142
    for t in range(-20, 71, 10):
        sv.line(sx(t), top, sx(t), top + rh * 4, GRID)
        sv.text(sx(t), top + rh * 4 + 22, (num(t, 0, sign=True) + "%") if t else "0%", 15, G1, "middle")
    sv.line(sx(0), top - 6, sx(0), top + rh * 4, INK, 1.5)
    sv.line(sx(-20), top + rh * 4, sx(70), top + rh * 4, G2)
    for i, (it, need, exp, ci, rc, m5, lab) in enumerate(BUL):
        y = top + i * rh + 46
        sv.text(0, y + 6, it, 18, INK, bold=True)
        sv.rect(sx(0), y - 30, sx(need) - sx(0), 60, G4, rx=4)
        sv.text(sx(need) - 6, y + 25, "necessário " + num(need, 1, sign=True) + "%", 13, INK, "end", bold=True)
        sv.line(sx(ci[0]), y, sx(ci[1]), y, BLUE, 4, cap="round")
        sv.line(sx(rc[0]), y + 40, sx(rc[1]), y + 40, G1, 2)
        sv.line(sx(rc[0]), y + 34, sx(rc[0]), y + 46, G1, 2); sv.line(sx(rc[1]), y + 34, sx(rc[1]), y + 46, G1, 2)
        sv.diamond(sx(m5), y, 9, INK)
        sv.circle(sx(exp), y, 10, BLUE, WHITE, 2)
        sv.text(sx(exp), y - 36, "esperado " + num(exp, 1, sign=True) + "%", 15, BLUE, "middle", bold=True)
        tl = lab + f" · M5 {num(m5, 1, sign=True)}% · recortes {num(rc[0], 1, sign=True)}% a {num(rc[1], 1, sign=True)}%"
        sv.rect(sx(-20), y + 50, len(tl) * 6.4, 17, WHITE)
        sv.text(sx(-20), y + 62, lab + f" · M5 {num(m5, 1, sign=True)}% · recortes {num(rc[0], 1, sign=True)}% a {num(rc[1], 1, sign=True)}%", 13, G1)
    sv.text(sx(25), top + rh * 4 + 48, "Variação do volume (%), de −20% a +70%", 15, G1, "middle")
    sv.text(0, top + rh * 4 + 48, "Eixo Y: item", 13, G1)

    def verdict(it, txt):
        return (f'<div style="display:flex;flex-direction:row;gap:10px">{p(it, 16, INK, bold=True, extra="width:100px;")}'
                f'{p(txt, 16, INK, extra="width:320px;")}</div>')
    body = "".join([
        P("Volume que a baixa de 10% traz contra o volume que ela precisa trazer", 100, 216, 1000, 18, INK, bold=True),
        seals(["PARCIAL"], 1290, 212),
        sv.render(),
        rail([("Leitura", f'<div style="display:flex;flex-direction:column;gap:8px">'
                          + verdict("Copo", "+5,8% contra +51,0%: longe, e sem leitura.")
                          + verdict("Lasanheira", "+16,4% contra +17,6%: empata.")
                          + verdict("Duralex", "+43,2% contra +18,3% no agregado; M5 empata.")
                          + verdict("Opaline", "+40,3% contra +22,6% no agregado; M5 −14,9%.") + "</div>", "info"),
              ("Premissa", p("Sensibilidade do volume ao preço nacional, com a faixa de 95%. " + REP, 14, G1), "info"),
              ("O que decidir", p("Duralex e Opaline só passam no agregado: confirmar em teste.", 18, bold=True), "decide")]),
    ])
    notes = ("Aqui juntamos os dois lados da conta. A barra cinza é o volume que a baixa de 10% precisa trazer; o ponto azul é o volume que a "
             "sensibilidade nacional diz que ela traz. No Copo, a distância é enorme. Na Lasanheira, o ponto fica em cima da barra: empata. No "
             "Duralex e na Opaline, o ponto passa da barra, mas os recortes e a comparação de cada loja com ela mesma mostram que pode não passar.\n\n"
             "Baixa de 10%, com repasse integral. Copo: necessário +51,0%; esperado +5,8% (faixa de 95%: −16,6% a +34,4%; sensibilidade −0,54, "
             "p 0,60, R² 0,04); recortes de −16,2% a +17,7%; M5 +30,6%. Lasanheira: necessário +17,6%; esperado +16,4% (+8,7% a +24,8%; −1,44, "
             "p 0,0010, R² 0,76); recortes de +2,7% a +20,4%; M5 +7,4%. Duralex: necessário +18,3%; esperado +43,2% (+24,2% a +65,2%; −3,41, "
             "p 0,0004, R² 0,81); recortes de +9,8% a +54,2%; M5 +18,2%. Opaline: necessário +22,6%; esperado +40,3% (+26,6% a +55,6%; −3,22, "
             "p 0,0001, R² 0,88); recortes de −2,5% a +63,6%; M5 −14,9%. " + REP)
    sub = ("Numa baixa de 10%, o Copo traria +6% de volume contra +51% necessários e a Lasanheira empata; Duralex e Opaline passam no agregado, "
           "mas não em todos os recortes.")
    foot = (f"{F_MARG}, com repasse integral; M5 do Excel v8.1 (02/10/2026), aba Resumo | Elaboração: DOC Consulting. {PER_VPM}")
    return slide("s14", "Volume esperado", sub, body, foot, "14", notes)


# ------------------------------------------------------------------ 15 efeito na margem
EF = {5: {"Copo": (-14.6, -23.9, -4.0, -5.3, -16.9), "Lasanheira": (-0.4, -6.3, 3.0, -4.2, -7.5),
          "Duralex": (9.9, -3.4, 17.8, 0.1, -7.7), "Opaline": (7.1, -16.1, 15.3, -16.1, -9.2)},
      10: {"Copo": (-29.9, -44.8, -11.0, -13.5, -33.8), "Lasanheira": (-1.0, -12.7, 6.1, -8.7, -15.0),
           "Duralex": (21.1, -7.2, 39.6, -0.1, -15.5), "Opaline": (14.4, -30.6, 33.4, -30.6, -18.5)}}


def s15():
    sv = Svg(100, 252, 1190, 706, "Variação da margem bruta total numa baixa de preço, em todos os cenários de sensibilidade")
    sv.hatch_def("h15")
    sv.rect(0, 4, 30, 16, G3, rx=3); sv.text(36, 17, "Do pior ao melhor cenário", 14, INK)
    sv.circle(236, 12, 7, BLUE); sv.text(248, 17, "Estimativa nacional", 14, INK)
    sv.diamond(410, 12, 8, INK); sv.text(424, 17, "M5", 14, INK)
    sv.line(476, 0, 476, 24, INK, 2.5); sv.text(484, 17, "Sem repasse", 14, INK)
    sv.rect(596, 4, 30, 16, "url(#h15)"); sv.text(632, 17, "Perda de margem", 14, INK)
    order = ["Copo", "Lasanheira", "Duralex", "Opaline"]
    top, rh = 96, 130
    for i, it in enumerate(order):
        sv.text(0, top + i * rh + 62, it, 18, INK, bold=True)
    for bi, (cut, x0) in enumerate([(5, 130), (10, 650)]):
        sx = Scale(-50, 45, x0 + 10, x0 + 500)
        sv.text(x0 + 255, 62, f"Baixa de {cut}%", 18, INK, "middle", bold=True)
        sv.rect(sx(-50), top, sx(0) - sx(-50), rh * 4, "url(#h15)", opacity=0.8)
        for t in [-40, -20, 0, 20, 40]:
            sv.line(sx(t), top, sx(t), top + rh * 4, GRID)
            sv.text(sx(t), top + rh * 4 + 22, (num(t, 0, sign=True) + "%") if t else "0%", 14, G1, "middle")
        sv.line(sx(0), top - 6, sx(0), top + rh * 4, INK, 1.5)
        sv.line(sx(-50), top + rh * 4, sx(45), top + rh * 4, G2)
        sv.text(x0 + 255, top + rh * 4 + 48, "Variação da margem bruta total (%)", 14, G1, "middle")
        for i, it in enumerate(order):
            nat, lo, hi, m5, sr = EF[cut][it]
            y = top + i * rh + 56
            sv.rect(sx(lo), y - 12, sx(hi) - sx(lo), 24, G3, rx=12)
            sv.line(sx(sr), y - 24, sx(sr), y + 24, INK, 2.5)
            sv.diamond(sx(m5), y, 9, INK)
            sv.circle(sx(nat), y, 10, BLUE, WHITE, 2)
            sv.text(sx(nat), y - 20, num(nat, 1, sign=True) + "%", 16, BLUE, "middle", bold=True)
            dt = f"{num(lo, 1, sign=True)}% a {num(hi, 1, sign=True)}% · M5 {num(m5, 1, sign=True)}% · sem repasse {num(sr, 1, sign=True)}%"
            sv.rect(sx(lo) - 2, y + 31, len(dt) * 6.0, 15, WHITE)
            sv.text(sx(lo), y + 42, f"{num(lo, 1, sign=True)}% a {num(hi, 1, sign=True)}% · M5 {num(m5, 1, sign=True)}% · sem repasse {num(sr, 1, sign=True)}%",
                    12, G1)
    sv.text(0, 690, "Cenários: estimativa nacional e sua faixa de 95%, 8 recortes, M5 e a curva de especificações do estudo (mediana e quartis). Eixo Y: item.", 13, G1)
    curva = mini_table([("Copo", "−1,45"), ("Duralex", "−1,52"), ("Opaline", "+0,33"), ("Lasanheira", "−0,89")], [150, 100], 15)
    body = "".join([
        P("Variação da margem bruta total numa baixa de preço, em todos os cenários de sensibilidade", 100, 216, 1050, 18, INK, bold=True),
        seals(["PARCIAL"], 1290, 212),
        sv.render(),
        rail([("Sem repasse, todos perdem", p("Na baixa de 10%, sem repasse ao preço de gôndola (PDV): Copo −33,8%; Opaline −18,5%; Duralex −15,5%; "
                                              "Lasanheira −15,0%. A conta supõe repasse integral, que não foi medido.", 15), "info"),
              ("Curva de especificações, mediana", curva + p("Sensibilidade do volume ao preço. P-valor e R²: não se aplica (mediana de 118 a 126 "
                                                             "versões do cálculo, não um modelo). Nacional com a faixa de 95%: slide 10.", 13, G1), "info"),
              ("O que decidir", p("Copo e Lasanheira: não baixar. Duralex e Opaline: o pior cenário é perda, só com teste.", 17, bold=True), "decide")]),
    ])
    notes = ("É o resultado final da conta, com todos os cenários de sensibilidade. O Copo perde margem em qualquer cenário. A Lasanheira fica em "
             "torno de zero, então baixar não cria margem. Duralex e Opaline ganham margem pela média nacional, mas o pior cenário de cada um é "
             "perda. E, se o varejo não repassar a baixa para a gôndola, todos perdem: a baixa vira só desconto.\n\nBaixa de 5%: Copo −14,6% (todos "
             "os cenários de −23,9% a −4,0%; M5 −5,3%; sem repasse −16,9%). Duralex +9,9% (−3,4% a +17,8%; M5 +0,1%; sem repasse −7,7%). Opaline "
             "+7,1% (−16,1% a +15,3%; M5 −16,1%; sem repasse −9,2%). Lasanheira −0,4% (−6,3% a +3,0%; M5 −4,2%; sem repasse −7,5%). Baixa de 10%: "
             "Copo −29,9% (−44,8% a −11,0%; M5 −13,5%; sem repasse −33,8%). Duralex +21,1% (−7,2% a +39,6%; M5 −0,1%; sem repasse −15,5%). "
             "Opaline +14,4% (−30,6% a +33,4%; M5 −30,6%; sem repasse −18,5%). Lasanheira −1,0% (−12,7% a +6,1%; M5 −8,7%; sem repasse −15,0%). "
             "Sensibilidades usadas, com p-valor e R²: nacional (slide 10), recortes e M5 (slide 12 e anexo A3); curva de especificações: mediana "
             "Copo −1,45, Duralex −1,52, Opaline +0,33, Lasanheira −0,89 (p-valor e R²: não se aplica, porque é a mediana de 118 a 126 versões do "
             "cálculo, não um modelo).")
    sub = ("Com todos os cenários à vista, o Copo perde margem sempre, a Lasanheira fica perto de zero e Duralex e Opaline ganham no agregado, "
           "mas podem perder.")
    foot = (f"{F_MARG}; M5 e curva de especificações do Excel v8.1 (02/10/2026), abas Resumo e Resumo da curva | Elaboração: DOC Consulting. {PER_VPM}")
    return slide("s15", "Efeito na margem", sub, body, foot, "15", notes)


# ------------------------------------------------------------------ 16 decisao
def s16():
    W = [210, 150, 250, 760, 300]
    heads = ["Item", "Margem SAP", "O que a baixa de 10% exige", "O que a sensibilidade do volume ao preço mostra", "Decisão"]
    rows = [("Copo", "29,6%", "+51,0% de volume", "+5,8% (faixa de 95%: −16,6% a +34,4%; p 0,60; R² 0,04), sem leitura", "Não baixar", False),
            ("Lasanheira", "66,8%", "+17,6% de volume", "+16,4% (faixa de 95%: +8,7% a +24,8%; p 0,0010; R² 0,76)", "Não baixar: no máximo empata", False),
            ("Duralex", "64,6%", "+18,3% de volume", "+43,2% no agregado (faixa de 95%: +24,2% a +65,2%; p 0,0004; R² 0,81); empate quando cada loja é comparada com ela mesma", "Testar a baixa", True),
            ("Opaline", "54,2%", "+22,6% de volume", "+40,3% no agregado (faixa de 95%: +26,6% a +55,6%; p 0,0001; R² 0,88); sem sinal quando cada loja é comparada com ela mesma", "Testar a baixa", True)]

    def cell(t, w, **k):
        return p(t, k.pop("size", 17), k.pop("color", INK), extra=f"width:{w}px;", **k)
    hdr = "".join(cell(h, w, size=14, color=G1, bold=True) for h, w in zip(heads, W))
    out = [f'<div style="display:flex;flex-direction:row;gap:12px;padding:0px 0px 8px 0px;border-bottom:2px solid {INK}">{hdr}</div>']
    for it, m, req, sens, dec, test in rows:
        col = BLUE if test else INK
        chip = (f'<p style="font-size:16px;font-weight:700;color:{col};border:2px solid {col};border-radius:8px;padding:6px 12px;'
                f'line-height:1.2">{e(dec)}</p>')
        out.append(f'<div style="display:flex;flex-direction:row;gap:12px;align-items:center;padding:18px 0px;border-bottom:1px solid {G4}">'
                   f'{cell(it, W[0], size=19, bold=True)}{cell(m, W[1], size=19)}{cell(req, W[2])}{cell(sens, W[3], size=16)}'
                   f'<div style="width:{W[4]}px;display:flex;flex-direction:row">{chip}</div></div>')
    matrix = f'<div style="position:absolute;left:100px;top:226px;width:1720px;display:flex;flex-direction:column">{"".join(out)}</div>'
    tests = [("Onde", "Baixa em algumas macrorregiões e preço mantido em outras (grupo de controle), alternando meses; no mínimo 4 regiões e 15 combinações região × mês com mudança de 5% ou mais."),
             ("O quê", "Baixa de 5% e de 10% no preço Nadir do Duralex e da Opaline, com repasse ao preço de gôndola (PDV) acordado com o Atacadão e conferido na coleta Involves."),
             ("Medida", "Volume por loja-mês na venda no caixa da BASE SO (marcada como sell-out), com e sem baixa, e margem bruta no SAP (sell-in), sem misturar sell-through."),
             ("Regra de manter ou voltar", "Manter só se o aumento medido, com a faixa de 95% inteira, passar do necessário: Duralex +8,4% (5%) e +18,3% (10%); Opaline +10,2% e +22,6%. Senão, voltar.")]
    tb = "".join(f'<div style="width:415px;background:{PANEL};border-radius:16px;padding:16px 20px;display:flex;flex-direction:column;gap:6px">'
                 f'{h3(t)}{p(d, 17, INK, lh=1.35)}</div>' for t, d in tests)
    body = "".join([
        seals(["RECOMENDAÇÃO"], 1820, 190),
        matrix,
        P("Desenho do teste de preço (Duralex e Opaline) · prazo e donos: a validar", 100, 610, 1200, 18, INK, bold=True),
        f'<div style="position:absolute;left:100px;top:646px;width:1720px;display:flex;flex-direction:row;justify-content:space-between">{tb}</div>',
    ])
    notes = ("Primeiro calculamos a sensibilidade; agora precisamos testar o efeito dela na margem. Para o Copo e a Lasanheira, a conta já "
             "responde: baixar não se paga. Para o Duralex e a Opaline, a média nacional diz que pagaria, mas o sinal não é firme. A forma de saber "
             "é um teste com grupo de controle: baixar em algumas regiões, manter em outras e medir o volume e a margem, com a regra de manter ou "
             "voltar escrita antes de começar.\n\nDetalhe do teste. Onde: no mínimo 4 regiões e 15 combinações região × mês com mudança de 5% ou "
             "mais (regra do estudo, Excel v8.1, aba Desenho do teste). Medida: volume por loja-mês na venda no caixa da BASE SO (marcada como "
             "sell-out), entre regiões com e sem baixa, e margem bruta no SAP (sell-in), sem misturar sell-through; coleta Involves sem buracos "
             "(como jul e ago/25) e com preço por peça. Prazo e donos: a validar. " + REP)
    sub = ("Nenhum item baixa a tabela agora: Copo e Lasanheira porque a conta não fecha; Duralex e Opaline entram no teste de preço com um "
           "braço de baixa.")
    foot = (f"Fonte: base conciliada, {CAIXA2}); preço de gôndola (PDV) da coleta Involves; margem SAP Nadir (sell-in; margem bruta ÷ Net Net); "
            f"Mtrix (sell-through) não entra; cálculo DOC das faixas nacionais de preço; Excel v8.1 (02/10/2026), abas Resumo e Desenho do teste | "
            f"Elaboração: DOC Consulting. {PER_VPM}")
    return slide("s16", "Decisão", sub, body, foot, "16", notes)


# ------------------------------------------------------------------ 17 proximos passos
def s17():
    cards = [("1", "Manter a tabela dos 4 itens: nenhuma baixa agora."),
             ("2", "Incluir no teste de preço por região um braço de baixa de 5% e de 10% para Duralex e Opaline, com grupo de controle e repasse acordado com o Atacadão."),
             ("3", "Adotar a regra de uso: a sensibilidade nacional só entra em decisão junto da faixa dos recortes, do p-valor e do R².")]
    ch = "".join(f'<div style="width:540px;background:rgba(255,255,255,0.07);border:1px solid rgba(154,180,232,0.45);border-radius:20px;'
                 f'padding:32px 34px;display:flex;flex-direction:column;gap:16px">{p(n, 64, LB2, bold=True, lh=1.0)}{p(t, 24, WHITE, lh=1.35)}</div>'
                 for n, t in cards)
    body = "".join([
        P("RECOMENDAÇÃO", 100, 150, 400, 14, LB2, bold=True, extra="letter-spacing:2px;"),
        P("Próximos passos", 100, 180, 1400, 72, WHITE, bold=True, lh=1.1),
        P("Três aprovações pedidas hoje para transformar a estimativa em decisão.", 100, 272, 1400, 28, G3, italic=True),
        f'<div style="position:absolute;left:100px;top:370px;width:1720px;display:flex;flex-direction:row;justify-content:space-between;align-items:stretch">{ch}</div>',
        f'<div style="position:absolute;left:100px;top:780px;width:1720px;border:1px solid {LB2};border-radius:16px;padding:20px 28px">'
        + p("Antes do teste: confirmar a empresa fonte da BASE SO, acordar o repasse por região, manter a coleta Involves sem buracos e resolver a "
            "mistura de peça e caixa no preço do Copo. Donos e datas: a validar.", 21, WHITE, lh=1.4) + "</div>",
    ])
    notes = ("Pedimos três aprovações: manter a tabela, colocar Duralex e Opaline no teste com braço de baixa e grupo de controle, e usar a "
             "sensibilidade nacional sempre com a faixa dos recortes ao lado. Antes do teste, quatro ajustes de dado.")
    foot = ("Fonte: base conciliada, BASE SO (venda no caixa das lojas do Atacadão, marcada como sell-out, com consumidor final e pequeno "
            "comerciante sem separação; empresa fonte não informada); coleta Involves de preço de gôndola (PDV); SAP Nadir (sell-in) para a margem; "
            "sell-through (CD e Mtrix) não entra nas contas; cálculo DOC das faixas nacionais de preço | Elaboração: DOC Consulting. " + PER_VPM)
    return slide("s17", "", "", body, foot, "17", notes, dark=True)


SLIDES_B = [s10, s11, s12, s13, s14, s15, s16, s17]

from lib import *
from data import *


# ------------------------------------------------------------------ 01 capa
def s01():
    dot = '<span style="color:#7F95CF">  ·  </span>'
    body = "".join([
        P("CONFIDENCIAL · PROJETO INTERNO", 100, 76, 600, 15, "#AFC1EE", extra="letter-spacing:1px;"),
        P("Preço, volume e margem", 100, 423, 1540, 100, WHITE, bold=True, lh=1.06),
        P("Nadir, 4 itens no Atacadão: o que a base mostra, quanto o volume responde ao preço e se uma baixa se paga na margem.",
          100, 551, 1540, 32, "#C9D6F5", lh=1.3),
        P(f"Nadir{dot}Copo Americano, Duralex, Opaline e Lasanheira{dot}Atacadão{dot}outubro de 2026", 100, 660, 1500, 20, WHITE, raw=True),
        '<div style="position:absolute;left:100px;top:760px;width:1500px;display:flex;flex-direction:row;gap:80px">'
        + "".join(f'<div style="display:flex;flex-direction:column;gap:6px;border-left:2px solid rgba(175,193,238,0.6);padding:0px 0px 0px 22px">'
                  f'{p(v, 44, WHITE, bold=True, lh=1.05)}{p(l, 16, "#AFC1EE", lh=1.3, extra="width:300px;")}</div>'
                  for v, l in [("4", "itens"), ("278 a 416", "lojas do Atacadão por item"),
                               ("32 a 45", "combinações região × mês com preço de gôndola (PDV) por item")])
        + "</div>",
    ])
    notes = ("A pergunta da Nadir é prática: se baixarmos o preço, o volume que vem paga a margem que sai? Vamos começar pela base, "
             "mostrar por que a conta direta não funciona, explicar o tratamento que escolhemos e, no fim, responder a pergunta com a "
             "estimativa e as ressalvas dela.")
    return slide("s01", "", "", body, F_GERAL, "01", notes, dark=True)


# ------------------------------------------------------------------ 02 sumario
def pill(n, t, d):
    circ = (f'<div style="width:44px;height:44px;background:{BLUE};border-radius:50%;display:flex;justify-content:center;'
            f'align-items:center;flex:none">{p(n, 17, WHITE, bold=True, lh=1.0)}</div>')
    txt = f'<div style="display:flex;flex-direction:column;gap:2px">{p(t, 19, INK, bold=True, lh=1.2)}{p(d, 16, G1, lh=1.25)}</div>'
    return (f'<div style="display:flex;flex-direction:row;align-items:center;gap:16px;{CARD};'
            f'padding:9px 18px">{circ}{txt}</div>')


def group(name, pills):
    return (f'<div style="display:flex;flex-direction:column;gap:7px">'
            f'{p(name, 14, G1, bold=True, extra="letter-spacing:1.5px;text-transform:uppercase;")}{"".join(pill(*x) for x in pills)}</div>')


def s02():
    left = [("Abertura", [("03", "Fundamentos", "As bases e o tipo de cada dado")]),
            ("Etapa 1 · A base recebida", [("04", "Base completa", "Pontos marcados como sell-out, todas as redes"),
                                           ("05", "Atacadão por loja", "Mesmo preço, volumes diferentes")]),
            ("Etapa 2 · Por que a regressão direta não conclui", [("06", "Regressão direta", "O que a reta mistura"),
                                                                  ("07", "Motores do volume", "Loja, mês e preço"),
                                                                  ("08", "Causas além do preço", "O que move o volume")]),
            ("Etapa 3 · O tratamento", [("09", "Faixas nacionais", "Como agrupamos")])]
    right = [("Etapa 4 · Sensibilidade e grau de confiança", [("10", "Sensibilidade", "A tendência e a faixa de 95%"),
                                                              ("11", "Retas por recorte", "O porte da loja"),
                                                              ("12", "Com moderação", "A faixa contra o empate")]),
             ("Etapa 5 · A pergunta de negócio", [("13", "Volume e margem", "A conta"),
                                                  ("14", "Volume esperado", "O que a baixa traz"),
                                                  ("15", "Efeito na margem", "Todos os cenários"),
                                                  ("16", "Decisão", "Tabela e teste"),
                                                  ("17", "Próximos passos", "O que aprovar hoje")])]
    col = lambda gs, x: (f'<div style="position:absolute;left:{x}px;top:206px;width:840px;display:flex;flex-direction:column;gap:16px">'
                         + "".join(group(n, ps) for n, ps in gs) + "</div>")
    body = col(left, 100) + col(right, 980)
    notes = ("São cinco etapas: a base que recebemos, por que a regressão direta não conclui, o tratamento escolhido, a sensibilidade "
             "com o grau de confiança e a pergunta de negócio.")
    return slide("s02", "Sumário", "Da base recebida à pergunta de negócio, em cinco etapas.", body, F_GERAL, "02", notes)


# ------------------------------------------------------------------ 03 fundamentos
def s03():
    sv = Svg(100, 250, 1720, 500, "Diagrama da cadeia da Nadir com o dado de cada elo")

    def node(x, y, w, h, label, kind):
        fill, stroke, tc = {"ind": (NAVY, None, WHITE), "main": (PANEL, INK, INK), "mid": (LB1, LB2, INK),
                            "shop": (BLUE, None, WHITE)}[kind]
        sv.rect(x, y, w, h, fill, stroke, 1.5 if stroke else 1, rx=16)
        lines = label.split("\n")
        y0 = y + h / 2 - (len(lines) - 1) * 11 + 6
        for i, ln in enumerate(lines):
            sv.text(x + w / 2, y0 + i * 22, ln, 17, tc, "middle", bold=(i == 0))

    def chip(x, y, w, lines, kind):
        col = {"blue": BLUE, "gray": G1, "none": G2}[kind]
        h = 10 + 16 * len(lines)
        if kind == "none":
            sv.rect(x, y, w, h, WHITE, G2, 1.5, rx=8, dash="5 4")
        else:
            sv.rect(x, y, w, h, col, rx=8)
        for i, ln in enumerate(lines):
            sv.text(x + 9, y + 18 + i * 16, ln, 13, WHITE if kind != "none" else G1, "start", bold=(i == 0 and kind != "none"))

    node(0, 50, 170, 400, "Indústria /\nfábrica\n(Nadir)", "ind")
    node(400, 50, 240, 90, "Atacarejo", "main")
    node(400, 215, 240, 90, "Varejista tradicional\n(grandes redes / super)", "main")
    node(400, 360, 240, 90, "Distribuidor", "mid")
    node(900, 145, 260, 80, "Pequeno varejo /\ntransformador", "mid")
    node(900, 360, 260, 90, "Médio / pequeno varejo", "main")
    node(1500, 50, 220, 400, "Shopper /\nconsumidor", "shop")

    A = lambda pts, lab, lx, ly, anc="middle": sv.arrow(pts, G2, 2, lab, lx, ly, 15, INK, anc)
    A([(170, 95), (398, 95)], "Sell-in direto atacarejo", 284, 85)
    A([(170, 260), (398, 260)], "Sell-in direto varejo", 284, 250)
    A([(170, 405), (398, 405)], "Sell-in indireto", 284, 395)
    A([(640, 68), (1498, 68)], "Sell-out direto", 1330, 60)
    A([(560, 140), (560, 185), (898, 185)], "Sell-through B2B", 730, 177)
    A([(1160, 185), (1498, 185)], "Sell-out", 1330, 177)
    A([(640, 260), (1498, 260)], "Sell-out varejo", 1330, 250)
    A([(640, 405), (898, 405)], "Sell-through", 770, 395)
    A([(1160, 405), (1498, 405)], "Sell-out", 1330, 395)

    chip(400, 6, 290, ["Coleta Involves: preço de gôndola (PDV)"], "blue")
    chip(652, 78, 236, ["BASE SO: venda no caixa do", "atacarejo, marcada como sell-out;", "inclui o pequeno comerciante,", "sem separação"], "blue")
    chip(176, 112, 218, ["BASE SO: CD 111-MATRIZ CD/AT", "do Atacadão, sell-through B2B"], "gray")
    chip(900, 268, 500, ["BASE SO: sell-out do varejo direto (supermercado, lojas de UD, magazine)"], "gray")
    chip(560, 458, 400, ["BASE SO (distribuidores e atacados) e Mtrix: sell-through"], "gray")
    chip(0, 458, 470, ["SAP Nadir: sell-in (margem e preço Nadir), nas 3 setas de sell-in"], "blue")
    chip(1290, 194, 90, ["Sem dado"], "none")
    chip(1290, 414, 90, ["Sem dado"], "none")
    # legenda
    sv.rect(1010, 466, 18, 14, BLUE, rx=3); sv.text(1034, 478, "entra nas contas", 14, INK)
    sv.rect(1170, 466, 18, 14, G1, rx=3); sv.text(1194, 478, "só no anexo A5 e A6", 14, INK)
    sv.rect(1350, 466, 18, 14, WHITE, G2, 1.5, rx=3, dash="3 2"); sv.text(1374, 478, "tracejado = sem dado", 14, INK)

    stats = [("4", "itens"), ("278 a 416", "lojas do Atacadão por item"), ("32 a 45", "combinações região × mês com preço"),
             ("1.069 a 2.852", "lojas-mês por item")]
    stat_html = "".join(f'<div style="width:225px;display:flex;flex-direction:column;gap:4px">{p(v, 40, BLUE, bold=True, lh=1.05)}'
                        f'{p(l, 15, G1, lh=1.3)}</div>' for v, l in stats)

    def card(t, txt):
        return (f'<div style="width:385px;{CARD};padding:16px 20px;display:flex;flex-direction:column;gap:6px">'
                f'{h3(t)}{p(txt, 15, INK, lh=1.35)}</div>')
    body = "".join([
        ctitle("Onde cada dado está na cadeia da Nadir"),
        seals(["COMPROVADA"], 1791, 229),
        sv.render(),
        f'<div style="position:absolute;left:100px;top:782px;width:930px;display:flex;flex-direction:row;gap:10px">{stat_html}</div>',
        P("Margem SAP (margem bruta ÷ Net Net, jun/25 a mai/26): Copo 29,6% · Duralex 64,6% · Opaline 54,2% · Lasanheira 66,8%. "
          "Sensibilidade, p-valor e R²: não se aplica. Tabela completa das bases: anexo A7.", 100, 900, 900, 15, G1),
        '<div style="position:absolute;left:1050px;top:782px;width:770px;display:flex;flex-direction:row;gap:0px;justify-content:space-between">'
        + card("Sanitizado", "Volume em peças; 0 duplicadas e 0 quantidades zero ou negativas; tipo de dado e fonte em cada linha; "
                             "preço por região × mês (mediana). Fora: 276 linhas sem mês, mar/25 sem loja, Paraty repetido no Mtrix.")
        + card("Ainda em alerta", "Caixa do atacarejo mistura consumidor final e pequeno comerciante; 6,4% das coletas atípicas; "
                                  "Copo mistura peça e caixa; fonte da BASE SO não informada; frete zero no SAP: margem bruta.")
        + "</div>",
    ])
    notes = ("Antes de qualquer análise, onde cada dado está na cadeia. A Nadir vende para o atacarejo, para o varejo e para o distribuidor: "
             "isso é sell-in, e é o que o SAP mede. O atacarejo vende ao consumidor final, que é sell-out, e ao pequeno comerciante, que "
             "revende ou transforma, e isso é sell-through; no caixa da loja, a base recebe as duas vendas juntas, sem separação, marcadas "
             "como sell-out. O distribuidor vende ao médio e pequeno varejo: sell-through, que vem da BASE SO e do Mtrix. Nas contas do deck "
             "entram só a venda no caixa das lojas do Atacadão, o preço de gôndola (PDV) da Involves e a margem do SAP; o sell-through fica "
             "no anexo, à parte.\n\nDetalhe dos cartões. Sanitizado: volume convertido em peças; 0 linhas duplicadas e 0 quantidades zero ou "
             "negativas; tipo de dado e empresa fonte marcados em cada linha; preço de gôndola (PDV) da coleta sanitizada (só coletas com preço, "
             "caixa convertida em peça no Copo, mediana por região × mês); fora das contas: 276 linhas da Millenium sem mês, mar/25 sem loja e o "
             "Paraty repetido no Mtrix. Ainda em alerta: no atacarejo, a venda no caixa mistura consumidor final (sell-out) e pequeno comerciante "
             "(sell-through), e a base não separa; 6,4% das coletas de preço são atípicas e ficam marcadas dentro da mediana; no Copo, a coleta "
             "ainda mistura preço de peça e de caixa; o 1% de lojas-mês com mais volume e as unidades -AT ficam na conta principal e foram "
             "testados à parte (anexo A2: a conclusão não muda); a empresa fonte da BASE SO não está informada; o SAP traz frete zero, então a "
             "margem é bruta.")
    sub = ("Cada dado mede um elo diferente da cadeia: SAP no sell-in, coleta Involves na gôndola, BASE SO na venda no caixa e Mtrix no "
           "sell-through dos distribuidores; sell-out e sell-through nunca se juntam.")
    return slide("s03", "Fundamentos", sub, body, F_BASES, "03", notes, cards=[(100, 206, 1720, 556)])


# ------------------------------------------------------------------ 04 base completa
def s04():
    rows = [("Copo", "71", "738", "4.616", "6.334 (5)"), ("Duralex", "4", "21", "76", "4.233 (11)"),
            ("Opaline", "4", "24", "115", "3.825 (11)"), ("Lasanheira", "1", "3", "15", "2.566 (8)")]
    tbl = mini_table(rows, [100, 52, 76, 70, 110], 16, head=["Item", "P10", "Mediana", "P90", "Pontos × mês (redes)"])
    body = "".join([
        ctitle("Volume por ponto de venda no mês contra o preço: pontos marcados como sell-out, todas as redes"),
        seals(["COMPROVADA"], 1290, 212),
        placeholder(100, 256, 1190, 700, "Gráfico 1 · Pontos marcados como sell-out por ponto de venda",
                    "Deck faixas - Gráfico 1 v2 - Pontos marcados como sell-out por ponto de venda - 02-10-2026.png",
                    "Legenda e eixos já vêm no PNG: cada ponto = um ponto de venda marcado como sell-out, num mês. "
                    "X: preço por peça (R$, escala log). Y: peças por ponto de venda no mês (escala log)."),
        rail([("Dispersão (peças por ponto de venda × mês)", tbl, "info"),
              ("Formato pesa", p("Duralex: mediana de 21 peças na loja do Atacadão e 1.340 na conta da BMP, que informa o total da rede. "
                                 "Por rede: anexo A6.", 17), "info"),
              ("Fora do gráfico", p("Sell-through fica fora: anexo A5. Sensibilidade, p-valor e R²: não se aplica (descrição da base, sem reta).", 17), "info"),
              ("O que decidir", p("Não ler a resposta ao preço nesta nuvem: o formato do ponto pesa mais que o preço.", 18, bold=True), "decide")]),
    ])
    notes = ("Esta é a base que recebemos, só com os pontos marcados como sell-out; no atacarejo, essa venda também atende o pequeno "
             "comerciante. Cada ponto é um ponto de venda num mês. No mesmo preço há pontos que vendem uma peça e pontos que vendem milhares. "
             "Parte disso é o formato: algumas redes mandam a venda de cada loja, outras mandam o total da UF ou da rede inteira.\n\n"
             "Números: 10º percentil, mediana e 90º percentil por ponto de venda × mês. Copo 71, 738 e 4.616 peças (6.334 pontos de venda × mês, "
             "5 redes); Duralex 4, 21 e 76 (4.233; 11 redes); Opaline 4, 24 e 115 (3.825; 11 redes); Lasanheira 1, 3 e 15 (2.566; 8 redes).")
    sub = ("Nos pontos marcados como sell-out, em todas as redes, o mesmo item vende de 1 a milhares de peças por ponto de venda no mês, "
           "no mesmo preço; parte da diferença é o formato do ponto.")
    foot = ("Fonte: base conciliada, BASE SO (pontos marcados como sell-out em todas as redes, por loja, UF ou conta; no atacarejo, a venda no "
            "caixa inclui o pequeno comerciante, sem separação; empresa fonte não informada); preço de gôndola (PDV) da coleta Involves quando "
            "há coleta, senão faturamento ÷ peças da BASE SO; sell-through (CD, distribuidores, atacados e Mtrix) fora do gráfico; 407 linhas "
            "com preço fora de 1/3 a 3 vezes a mediana do item fora | Elaboração: DOC Consulting. Período: jan/25 a mai/26.")
    return slide("s04", "Base completa", sub, body, foot, "04", notes, cards=CHART_CARD)


# ------------------------------------------------------------------ 05 atacadao por loja
def cv_svg():
    sv = Svg(0, 0, 446, 196, "CV do volume por faixa, do menor ao maior, por item")
    sx = Scale(0, 4.5, 104, 432)
    rows = [("Copo", 1.85, 4.30), ("Duralex", 0.74, 1.25), ("Opaline", 0.79, 2.53), ("Lasanheira", 0.51, 2.19)]
    for t in [0, 1, 2, 3, 4]:
        sv.line(sx(t), 18, sx(t), 150, GRID)
        sv.text(sx(t), 168, num(t, 0), 14, G1, "middle")
    sv.line(sx(1), 10, sx(1), 150, INK, 1.5, "5 4")
    sv.text(sx(1) + 5, 14, "CV 1: desvio igual à média", 13, INK)
    for i, (n, a, b) in enumerate(rows):
        y = 34 + i * 32
        sv.text(0, y + 5, n, 15, INK, bold=True)
        sv.rect(sx(a), y - 6, sx(b) - sx(a), 12, LB2, rx=6)
        sv.text(sx(a) - 5, y + 5, num(a, 2), 13, G1, "end")
        sv.text(sx(b) + 5, y + 5, num(b, 2), 13, INK, "start", bold=True)
    sv.text(268, 188, "CV nas 10 faixas (desvio padrão ÷ média)", 13, G1, "middle")
    return sv.render().replace("position:absolute;left:0px;top:0px;", "")


def s05():
    rows = [("Duralex", "F1 · R$ 6,92", "7", "34", "99"), ("Opaline", "F1 · R$ 6,22", "7", "62", "203"),
            ("Lasanheira", "F2 · R$ 49,90", "2", "7", "17"), ("Copo", "F1 · R$ 0,98", "440", "1.698", "5.245")]
    tbl = mini_table(rows, [96, 116, 50, 64, 64], 15, head=["Item", "Faixa", "P10", "Mediana", "P90"])
    body = "".join([
        ctitle("Volume por loja no mês contra o preço de gôndola (PDV): lojas do Atacadão, venda no caixa, sem o CD"),
        seals(["COMPROVADA"], 1290, 212),
        placeholder(100, 256, 1190, 700, "Gráfico 2 · Atacadão por loja",
                    "Deck faixas - Gráfico 2 v2 - Atacadão por loja - 02-10-2026.png",
                    "Legenda e eixos já vêm no PNG: azul = lojas-mês da faixa de preço destacada; cinza = demais lojas-mês; cada coluna é "
                    "o preço de uma região × mês. X: preço de gôndola (PDV) por peça (R$, escala log). Y: peças por loja no mês (escala log)."),
        rail([("Faixa destacada (peças por loja no mês)", tbl, "info"),
              ("Variação no mesmo preço", cv_svg() + p("Barra = do menor ao maior CV entre as 10 faixas. Sensibilidade, p-valor e R²: não se aplica.", 13, G1), "info"),
              ("O que decidir", p("Tirar o ruído de loja antes de medir preço: é o que o agrupamento em faixas faz (slide 09).", 18, bold=True), "decide")]),
    ])
    notes = ("Agora só o Atacadão, loja por loja, com o preço de gôndola (PDV) da região no mês; por isso as lojas formam colunas. Em cada coluna, "
             "o preço é o mesmo e o volume vai de poucas peças a centenas. Essa variação não é preço: é perfil de loja, região, sortimento e "
             "promoção.\n\nCV = desvio padrão ÷ média do volume das lojas-mês na mesma faixa; acima de 1, o desvio passa da média. Copo de 1,85 a "
             "4,30 nas 10 faixas; Duralex de 0,74 a 1,25; Opaline de 0,79 a 2,53; Lasanheira de 0,51 a 2,19. Base: 2.852, 1.879, 1.604 e 1.069 "
             "lojas-mês; 416, 373, 326 e 278 lojas (Copo, Duralex, Opaline e Lasanheira). Sensibilidade, p-valor e R²: não se aplica neste slide "
             "(é a descrição da base, sem reta).")
    sub = ("Mesmo dentro do Atacadão, no mesmo preço uma loja vende 7 peças de Duralex no mês e outra vende 99; o desvio do volume chega a "
           "4 vezes a média.")
    foot = (f"Fonte: base conciliada, {CAIXA}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; Mtrix (sell-through) e SAP "
            f"(sell-in) não entram | Elaboração: DOC Consulting. {PER_VP}")
    return slide("s05", "Atacadão por loja", sub, body, foot, "05", notes, cards=CHART_CARD)


# ------------------------------------------------------------------ 06 regressao direta
def bar_panel(left, width, title_lines, legend, groups, note, alt, xlab_sub=None):
    """groups: list of (item, v_blue, v_gray, label_blue_inside, label_gray_inside)"""
    H = 704
    sv = Svg(left, 252, width, H, alt)
    for i, t in enumerate(title_lines):
        sv.text(0, 18 + i * 21, t, 17, INK, bold=True)
    ly = 18 + len(title_lines) * 21 + 8
    sv.rect(0, ly - 11, 14, 14, BLUE, rx=2); sv.text(20, ly + 1, legend[0], 14, INK)
    lx = 20 + len(legend[0]) * 7.6 + 16
    sv.rect(lx, ly - 11, 14, 14, G2, rx=2); sv.text(lx + 20, ly + 1, legend[1], 14, INK)
    top, bot = ly + 52, 560
    x0 = 40
    sv.line(x0, bot, width, bot, G2)
    sv.line(x0, top - 10, x0, bot, G2)
    sv.text(14, (top + bot) / 2, "Peças por loja no mês (escala de cada item)", 14, G1, "middle", rotate=-90)
    gw = (width - x0) / len(groups)
    bw = min(48, gw * 0.4)
    for i, (item, vb, vg, lb, lg) in enumerate(groups):
        cx = x0 + gw * (i + 0.5)
        mx = max(vb, vg)
        for j, (v, col, lab) in enumerate([(vb, BLUE, lb), (vg, G2, lg)]):
            h = (bot - top) * v / mx
            x = cx - bw - 3 if j == 0 else cx + 3
            sv.rect(x, bot - h, bw, h, col, rx=3)
            sv.text(x + bw / 2, bot - h - 8, num(v, 1 if v < 100 else 0), 15, INK, "middle", bold=True)
            if lab:
                sv.text(x + bw / 2, bot - h + 20, lab[0], 13, WHITE, "middle")
                sv.text(x + bw / 2, bot - h + 36, lab[1], 13, WHITE, "middle", bold=True)
        sv.text(cx, bot + 22, item, 15, INK, "middle", bold=True)
        if xlab_sub:
            sv.text(cx, bot + 40, xlab_sub[i], 13, G1, "middle")
    sv.text((x0 + width) / 2, bot + 66, "Item", 14, G1, "middle")
    for i, t in enumerate(note):
        sv.text(0, bot + 100 + i * 18, t, 13, G1)
    return sv.render()


def s06():
    reg = [("Copo", 3077, 2422, ("R$", "1,07"), ("R$", "1,43")), ("Duralex", 36.9, 23.1, ("R$", "8,38"), ("R$", "8,77")),
           ("Opaline", 76.4, 19.9, ("R$", "7,70"), ("R$", "11,15")), ("Lasanheira", 6.6, 2.8, ("R$", "53,20"), ("R$", "94,63"))]
    por = [("Duralex", 34.5, 11.1, None, None), ("Opaline", 39.2, 12.8, None, None), ("Lasanheira", 4.2, 2.2, None, None)]
    pro = [("Opaline", 132.2, 38.0, ("R$", "5,99"), ("R$", "9,73")), ("Lasanheira", 7.5, 4.3, ("R$", "49,90"), ("R$", "69,15"))]
    rows = [("Copo", "−2,65", "−3,75 a −1,55", "< 0,0001", "0,06"), ("Duralex", "−2,84", "−3,40 a −2,27", "< 0,0001", "0,10"),
            ("Opaline", "−2,38", "−2,84 a −1,93", "< 0,0001", "0,17"), ("Lasanheira", "−1,27", "−1,57 a −0,96", "< 0,0001", "0,19")]
    tbl = mini_table(rows, [92, 58, 124, 78, 44], 15, head=["Item", "Sensib.", "Faixa de 95%", "p-valor", "R²"])
    body = "".join([
        seals(["COMPROVADA"], 1290, 212),
        bar_panel(100, 470, ["Região: SP é mais barato e vende", "mais por loja"], ["SP", "demais regiões"], reg,
                  ["Rótulo dentro da barra: preço médio de gôndola (PDV)."], "Volume por loja, SP contra demais regiões"),
        bar_panel(595, 360, ["Porte: no mesmo preço, a loja", "grande vende mais"], ["lojas grandes", "lojas pequenas"], por,
                  ["No preço do meio das faixas.", "Grandes ÷ pequenas: 3,1×; 3,1×; 1,9×."], "Volume por loja, grandes contra pequenas",
                  xlab_sub=["R$ 9,06", "R$ 10,57", "R$ 84,40"]),
        bar_panel(980, 310, ["Promoção: mês com promoção tem", "preço menor e mais volume"], ["com promoção", "sem"], pro,
                  ["Duralex sem promoção nas coletas;", "Copo: 15,0% do volume em promoção."], "Volume por loja, com e sem promoção",
                  xlab_sub=["40,1% do volume", "41,1% do volume"]),
        rail([("Reta com todos os pontos", p("Sensibilidade do volume ao preço, log-log, com a faixa de 95% (erro agrupado por região × mês).", 14, G1) + tbl, "info"),
              ("Por que não conclui", p("O preço explica no máximo 19% do volume, e a inclinação carrega região, porte e promoção.", 17), "info"),
              ("O que decidir", p("Não usar esta inclinação para decidir preço.", 18, bold=True), "decide")]),
    ])
    notes = ("Se traçamos a reta com todos os pontos, ela sai inclinada e o p-valor fica perto de zero. Parece uma resposta, mas não é: o preço "
             "explica no máximo 19% do volume, e a inclinação carrega outras coisas. Em SP o preço é menor e as lojas vendem mais; as lojas "
             "grandes vendem três vezes mais no mesmo preço; e o mês com promoção tem preço menor e mais volume. Não dá para separar quanto da "
             "inclinação é preço.\n\nNúmeros dos mini gráficos. Região (preço médio e peças por loja no mês): Copo SP R$ 1,07 e 3.077, demais "
             "R$ 1,43 e 2.422; Duralex SP R$ 8,38 e 36,9, demais R$ 8,77 e 23,1; Opaline SP R$ 7,70 e 76,4, demais R$ 11,15 e 19,9; Lasanheira SP "
             "R$ 53,20 e 6,6, demais R$ 94,63 e 2,8. Porte (no preço do meio das faixas): Duralex R$ 9,06, grandes 34,5 e pequenas 11,1 (3,1 vezes); "
             "Opaline R$ 10,57, grandes 39,2 e pequenas 12,8 (3,1 vezes); Lasanheira R$ 84,40, grandes 4,2 e pequenas 2,2 (1,9 vez). Promoção: "
             "Opaline com promoção R$ 5,99 e 132,2 peças, sem promoção R$ 9,73 e 38,0, 40,1% do volume em mês com promoção; Lasanheira com "
             "promoção R$ 49,90 e 7,5, sem promoção R$ 69,15 e 4,3, 41,1% do volume. O Duralex não teve promoção nas coletas; no Copo, 15,0% do "
             "volume foi em mês com promoção. Barras em escala própria de cada item; o valor está no rótulo.")
    sub = ("A reta com todos os pontos sai inclinada e com p-valor perto de zero, mas explica só de 6% a 19% do volume e mistura região, "
           "porte de loja e promoção.")
    foot = (f"Fonte: base conciliada, {CAIXA}; porte pelo faturamento da venda no caixa); preço de gôndola (PDV) e marcação de promoção da "
            f"coleta Involves por macrorregião × mês; Mtrix (sell-through) e SAP (sell-in) não entram; cálculo DOC | Elaboração: DOC Consulting. {PER_VP}")
    return slide("s06", "Regressão direta", sub, body, foot, "06", notes, cards=CHART_CARD)


# ------------------------------------------------------------------ 07 motores
def s07():
    sv = Svg(100, 252, 1190, 690, "Parte da variação do volume explicada por loja, mês e resto, por item")
    data = [("Copo", 53.2, 2.2, 44.6, 1.1), ("Duralex", 39.8, 0.7, 59.5, 0.4), ("Opaline", 44.3, 4.0, 51.7, 0.4),
            ("Lasanheira", 40.8, 8.3, 50.9, 1.5)]
    leg = [(INK, "Loja"), (G1, "Mês"), (G3, "Resto dentro da loja"), (BLUE, "Preço e promoção (parte do resto)")]
    x = 0
    for c, t in leg:
        sv.rect(x, 6, 16, 16, c, rx=3); sv.text(x + 22, 19, t, 15, INK); x += 22 + len(t) * 7.8 + 28
    sx = Scale(0, 100, 150, 1040)
    for t in range(0, 101, 20):
        sv.line(sx(t), 70, sx(t), 590, GRID)
        sv.text(sx(t), 612, f"{t}%", 16, G1, "middle")
    sv.line(sx(0), 590, sx(100), 590, G2)
    sv.text(1115, 66, "Preço e", 14, BLUE, "middle", bold=True)
    sv.text(1115, 82, "promoção", 14, BLUE, "middle", bold=True)
    for i, (n, lj, ms, rs, pp) in enumerate(data):
        y = 110 + i * 120
        sv.text(0, y + 41, n, 18, INK, bold=True)
        segs = [(lj, INK, WHITE), (ms, G1, WHITE), (rs - pp, G3, INK), (pp, BLUE, WHITE)]
        acc = 0
        for v, c, tc in segs:
            sv.rect(sx(acc), y, sx(acc + v) - sx(acc), 66, c)
            acc += v
        sv.text(sx(lj / 2), y + 40, num(lj) + "%", 18, WHITE, "middle", bold=True)
        mx = sx(lj + ms / 2)
        if ms >= 6:
            sv.text(mx, y + 40, num(ms) + "%", 16, WHITE, "middle", bold=True)
        else:
            sv.line(mx, y - 2, mx, y - 10, G1)
            sv.text(mx, y - 14, "mês " + num(ms) + "%", 14, G1, "middle")
        sv.text(sx(lj + ms + (rs - pp) / 2), y + 40, "resto " + num(rs) + "%", 16, INK, "middle")
        sv.text(1115, y + 41, num(pp) + "%", 20, BLUE, "middle", bold=True)
    sv.text(sx(50), 642, "% da variação do volume (log), de 0% a 100%", 15, G1, "middle")
    sv.text(0, 680, "É participação na variação, não efeito causal. Eixo Y: item.", 13, G1)
    r2 = mini_table([("Copo", "0,55"), ("Duralex", "0,41"), ("Opaline", "0,48"), ("Lasanheira", "0,49")], [140, 80], 16,
                    head=["Item", "R²"])
    body = "".join([
        ctitle("Parte da variação do volume (em log) explicada por loja, mês e resto, por item"),
        seals(["COMPROVADA"], 1290, 212),
        sv.render(),
        rail([("R² de loja e mês juntos", r2 + p("P-valor: não se aplica (é repartição da variação, não teste de efeito).", 14, G1), "info"),
              ("Leitura", p("Quase metade da variação vem de qual loja vende. Preço e promoção juntos ficam abaixo de 2%.", 17), "info"),
              ("O que decidir", p("Medir preço só depois de tirar o efeito de loja.", 18, bold=True), "decide")]),
    ])
    notes = ("Aqui a pergunta muda de lado: em vez de perguntar quanto o volume reage ao preço, perguntamos o que move o volume. A resposta é a "
             "loja: quase metade da variação vem de qual loja vende. O preço e a promoção juntos ficam abaixo de 2%.\n\nLoja: Copo 53,2%, Duralex "
             "39,8%, Opaline 44,3%, Lasanheira 40,8%. Mês: 2,2%, 0,7%, 4,0% e 8,3%. Resto dentro da loja: 44,6%, 59,5%, 51,7% e 50,9%. Preço e "
             "promoção, como parte do total: 1,1%, 0,4%, 0,4% e 1,5%. R² de loja e mês juntos: 0,55; 0,41; 0,48 e 0,49. P-valor: não se aplica.")
    sub = "A loja explica de 40% a 53% da variação do volume e o mês até 8%; preço e promoção somam de 0,4% a 1,5%."
    foot = (f"Fonte: base conciliada, {CAIXA2}), em logaritmo do volume; preço de gôndola (PDV) e promoção da coleta Involves; Mtrix "
            f"(sell-through) e SAP (sell-in) não entram; Excel v8.1 (02/10/2026), abas Loja, mês e resto e O que explica o volume | Elaboração: "
            f"DOC Consulting. Período: jan/25 a mai/26.")
    return slide("s07", "Motores do volume", sub, body, foot, "07", notes, cards=CHART_CARD)


# ------------------------------------------------------------------ 08 causas
def s08():
    sv = Svg(100, 252, 1190, 706, "O que explica a variação do volume dentro da loja, por fator e item")
    F = [("Região × mês", [8.6, 4.3, 4.9, 7.9], [7.1, 1.8, 2.1, 4.7]),
         ("Presença e ruptura", [2.9, 1.6, 1.9, 1.8], [2.8, 1.4, 1.7, 1.5]),
         ("Caixa fechada e unidades -AT", [0.9, 1.5, 1.2, 5.2], [0.6, 1.1, 0.9, 5.0]),
         ("Movimento da loja no mês", [1.2, 1.6, 2.4, 0.5], [1.2, 1.6, 2.3, 0.4]),
         ("Promoção", [0.2, 0.0, 0.2, 0.1], [0, 0, 0, 0]),
         ("Preço de gôndola (PDV)", [0.1, 0.1, 0.1, 0.1], [0, 0, 0, 0]),
         ("Troca de fonte do sell-out (nov/25)", [9.7, 10.7, 10.0, 11.4], [2.5, 1.0, 0.0, -1]),
         ("Ciclo de vida da loja", [10.4, 10.4, 12.3, 12.7], [2.9, -1, 0.6, -1])]
    # legenda
    sv.rect(0, 4, 16, 16, BLUE, rx=3); sv.text(22, 17, "Preço de gôndola (PDV)", 15, INK)
    sv.rect(220, 4, 16, 16, G2, rx=3); sv.text(242, 17, "Outros fatores", 15, INK)
    sv.circle(388, 12, 5, INK); sv.text(400, 17, "Fator acima do acaso", 15, INK)
    sv.text(590, 17, "Sem explicação: ver nota ao lado das barras", 15, G1)
    sx = Scale(0, 14, 360, 1100)
    top = 46
    gh = 76
    for t in [0, 2, 4, 6, 8, 10, 12, 14]:
        sv.line(sx(t), top, sx(t), top + gh * 8, GRID)
        sv.text(sx(t), top + gh * 8 + 20, f"{t}%", 15, G1, "middle")
    sv.line(sx(0), top, sx(0), top + gh * 8, G2)
    for gi, (name, vals, above) in enumerate(F):
        gy = top + gi * gh + 4
        words = name.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) > 20:
                lines.append(cur.strip()); cur = ""
            cur += w + " "
        lines.append(cur.strip())
        isp = name.startswith("Preço")
        for li, ln in enumerate(lines):
            sv.text(0, gy + 24 + li * 18, ln, 15, BLUE if isp else INK, bold=True)
        for k, it in enumerate(ITEMS):
            y = gy + k * 16
            sv.text(350, y + 11, it, 12, G1, "end")
            w = sx(vals[k]) - sx(0)
            sv.rect(sx(0), y, max(w, 1.5), 12, BLUE if isp else G2, rx=2)
            sv.text(sx(0) + w + (14 if above[k] > 0 else 5), y + 11, num(vals[k]) + "%", 12, INK)
            if above[k] > 0:
                sv.circle(sx(0) + w + 6, y + 6, 4, INK)
    sv.text(sx(7), top + gh * 8 + 44, "% da variação dentro da loja (log do volume)", 15, G1, "middle")
    sv.text(0, top + gh * 8 + 44, "Fator", 15, G1)
    # anotação
    ax, ay = 640, top + 4 * gh + 6
    sv.rect(ax, ay, 450, 132, PANEL, rx=14)
    sv.text(ax + 20, ay + 34, "Preço de gôndola (PDV): 0,1% em todos", 18, BLUE, bold=True)
    sv.text(ax + 20, ay + 58, "os itens (0,0 acima do acaso).", 18, BLUE, bold=True)
    sv.text(ax + 20, ay + 90, "Sem explicação, descontado o acaso: 72% a", 16, G1)
    sv.text(ax + 20, ay + 112, "86% do que varia dentro da loja.", 16, G1)

    def row(status, txt, meta):
        col = {"COMPROVADA": BLUE, "PARCIAL": G1, "REFUTADA": INK, "NÃO MENSURÁVEL": G2}[status]
        chip = (f'<p style="width:116px;flex:none;font-size:11px;font-weight:700;letter-spacing:0.5px;color:{col};border:1px solid {col};'
                f'border-radius:6px;padding:3px 6px;text-align:center;line-height:1.2">{e(status)}</p>')
        return (f'<div style="display:flex;flex-direction:row;gap:10px;align-items:start">{chip}<div style="display:flex;flex-direction:column;gap:1px">'
                f'{p(txt, 14, INK, lh=1.25)}{p(meta, 12, G1, lh=1.2)}</div></div>')
    mapa = "".join([
        row("COMPROVADA", "O volume se explica sobretudo pela loja, não pelo preço de gôndola (PDV).", "Outra coisa · loja: 40% a 53%"),
        row("COMPROVADA", "Unidades -AT vendem caixa fechada (múltiplo de 12 em cerca de 90% das linhas).", "Base do dado · 0,9% a 5,2%"),
        row("COMPROVADA", "A falta de leitura vem da pouca variação do preço de gôndola (PDV).", "Preço · 0,1%"),
        row("REFUTADA", "Limpar a base (CD, -AT, troca de fonte, extremos) dá leitura à elasticidade.", "Base do dado · anexo A2"),
        row("REFUTADA", "A medida de preço de gôndola (PDV) do Copo é confiável.", "Preço · Copo sem leitura"),
        row("PARCIAL", "Presença e ruptura mexem no volume.", "Outra coisa · 1,6% a 2,9%"),
        row("NÃO MENSURÁVEL", "Promoção mexe no volume (com o dado atual).", "Outra coisa · 0,0% a 0,2%"),
    ])
    body = "".join([
        ctitle("O que explica a variação do volume dentro da loja, por fator e item"),
        seals(["PARCIAL"], 1290, 212),
        sv.render(),
        rail([("Mapa de causas: hipótese, tipo e peso", f'<div style="display:flex;flex-direction:column;gap:9px">{mapa}</div>', "info"),
              ("O que decidir", p("Para medir preço, o preço precisa variar: só um teste controlado cria essa variação.", 17, bold=True), "decide")],
             gap=12),
    ])
    notes = ("Dentro de cada loja, o que mais pesa no volume não é o preço: é o choque de cada região no mês, a presença do produto na gôndola e, "
             "na Lasanheira, a venda em caixa fechada das unidades -AT. O preço de gôndola (PDV) explica 0,1% do que sobra. E de 72% a 86% do que "
             "varia dentro da loja não tem explicação no dado que temos.\n\nParcela no que varia dentro da loja (Copo; Duralex; Opaline; "
             "Lasanheira), com o quanto fica acima do acaso entre parênteses: região × mês 8,6% (7,1 pontos); 4,3% (1,8); 4,9% (2,1); 7,9% (4,7). "
             "Presença e ruptura 2,9% (2,8); 1,6% (1,4); 1,9% (1,7); 1,8% (1,5). Caixa fechada e unidades -AT 0,9% (0,6); 1,5% (1,1); 1,2% (0,9); "
             "5,2% (5,0). Movimento da loja no mês (outros itens Nadir) 1,2% (1,2); 1,6% (1,6); 2,4% (2,3); 0,5% (0,4). Promoção 0,2%; 0,0%; 0,2%; "
             "0,1%. Preço de gôndola (PDV) 0,1% nos 4 itens (0,0 acima do acaso). Troca de fonte do sell-out em nov/25 9,7% (2,5); 10,7% (1,0); "
             "10,0% (0,0); 11,4% (abaixo do acaso). Ciclo de vida da loja 10,4% (2,9); 10,4% (abaixo do acaso); 12,3% (0,6); 12,7% (abaixo do "
             "acaso). R² ajustado do resto: 0,28; 0,14; 0,16 e 0,15; o acaso sozinho daria 0,17; 0,23; 0,24 e 0,33. P-valor: não se aplica "
             "(repartição da variação). Tipo de cada causa no mapa: base do dado, preço ou outra coisa.")
    sub = ("Dentro da loja pesam o choque região × mês, a presença e ruptura e, na Lasanheira, a caixa fechada das unidades -AT; o preço de "
           "gôndola (PDV) explica 0,1% do resto.")
    foot = (f"Fonte: base conciliada, {CAIXA2}); preço de gôndola (PDV), promoção e presença da coleta Involves; Mtrix (sell-through) e SAP "
            f"(sell-in) não entram; Excel v8.1 (02/10/2026), abas O que explica o volume, Base, preço ou outra coisa e Hipóteses e evidências | "
            f"Elaboração: DOC Consulting. Período: jan/25 a mai/26.")
    return slide("s08", "Causas além do preço", sub, body, foot, "08", notes, cards=CHART_CARD)


# ------------------------------------------------------------------ 09 faixas nacionais
def s09():
    steps = [("1 · Combinação região × mês", "32 a 45", "combinações por item: o nível em que o preço de gôndola (PDV) é coletado. Copo 45, Duralex 40, Opaline 38, Lasanheira 32."),
             ("2 · 10 faixas", "10 faixas", "Ordenar as combinações pelo preço e cortar em 10 grupos do mesmo tamanho (3 a 5 combinações cada)."),
             ("3 · Ponto da faixa", "1 ponto", "Preço médio ponderado pelo volume; volume por loja-mês = peças vendidas ÷ lojas-mês."),
             ("4 · Reta log-log", "10 pontos", "ln(volume) = a + sensibilidade do volume ao preço × ln(preço), com a faixa de 95%, o p-valor e o R².")]
    cards = []
    for i, (lab, big, desc) in enumerate(steps):
        x = 100 + i * 442
        cards.append(f'<div style="position:absolute;left:{x}px;top:232px;width:392px;height:280px;{CARD};'
                     f'padding:24px 26px;display:flex;flex-direction:column;gap:10px">{h3(lab)}{p(big, 44, INK, bold=True, lh=1.05)}'
                     f'{p(desc, 17, INK, lh=1.35)}</div>')
        if i < 3:
            cards.append(f'<svg aria-label="seta" xmlns="http://www.w3.org/2000/svg" width="40" height="60" viewBox="0 0 40 60" '
                         f'style="position:absolute;left:{x + 396}px;top:342px;width:40px;height:60px">'
                         f'<path d="M6 6 L32 30 L6 54" stroke="{BLUE}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    # mini grafico % SP Duralex
    sv = Svg(0, 0, 780, 214, "Duralex: % de combinações de SP em cada faixa")
    sp = [25, 25, 100, 0, 100, 50, 0, 0, 0, 0]
    sy = Scale(0, 100, 168, 30)
    for t in [0, 50, 100]:
        sv.line(60, sy(t), 770, sy(t), GRID)
        sv.text(52, sy(t) + 5, f"{t}%", 14, G1, "end")
    for i, v in enumerate(sp):
        x = 72 + i * 70
        if v > 0:
            sv.rect(x, sy(v), 46, sy(0) - sy(v), BLUE, rx=3)
        sv.text(x + 23, sy(v) - 6, f"{v}%", 14, INK, "middle", bold=True)
        sv.text(x + 23, 186, f"F{i + 1}", 14, G1, "middle")
    sv.line(60, sy(0), 770, sy(0), G2)
    sv.text(14, 100, "% SP", 14, G1, "middle", rotate=-90)
    sv.text(415, 208, "Faixa nacional de preço (F1 = mais barata) · barra = % de combinações de SP", 13, G1, "middle")
    msvg = sv.render().replace("position:absolute;left:0px;top:0px;", "")
    left = (f'<div style="position:absolute;left:100px;top:540px;width:820px;height:416px;background:{WHITE};border:1px solid {G4};border-radius:18px;'
            f'padding:24px 28px;display:flex;flex-direction:column;gap:12px">{h3("O que o agrupamento resolve")}'
            f'<div style="display:flex;flex-direction:row;gap:28px;align-items:end">'
            f'<div style="display:flex;flex-direction:column;gap:2px">{p("7 contra 99", 44, G1, bold=True, lh=1.05)}{p("peças de Duralex por loja no mesmo preço", 15, G1)}</div>'
            f'{p("→", 40, BLUE, bold=True, lh=1.2)}'
            f'<div style="display:flex;flex-direction:column;gap:2px">{p("1 média", 44, BLUE, bold=True, lh=1.05)}{p("por faixa, sem o ruído de loja", 15, G1)}</div></div>'
            f'{p("Lojas: 416, 373, 326 e 278. Lojas-mês: 2.852, 1.879, 1.604 e 1.069 (Copo, Duralex, Opaline, Lasanheira).", 16)}'
            f'{p("Com 12 faixas no lugar de 10, a sensibilidade quase não muda: Duralex −3,57 (p < 0,0001; R² 0,89); Opaline −3,33 (p 0,0002; R² 0,77); Lasanheira −1,51 (p 0,0019; R² 0,64); Copo −0,29 (p 0,78; R² 0,01), sem leitura.", 15, G1)}'
            f'</div>')
    right = (f'<div style="position:absolute;left:960px;top:540px;width:860px;height:416px;background:{WHITE};border:1px solid {G4};border-radius:18px;'
             f'padding:24px 28px;display:flex;flex-direction:column;gap:10px">{h3("O que ele não resolve", INK)}'
             f'{p("Duralex: % de combinações de SP em cada faixa", 16, INK, bold=True)}{msvg}'
             f'{p("Faixas baratas quase só de SP, caras quase só de outras regiões. Lasanheira: SP entre R$ 48 e R$ 75; demais entre R$ 80 e R$ 130. Parte da inclinação é região: por isso os recortes dos slides 11 e 12.", 15, INK)}'
             f'</div>')
    body = seals(["COMPROVADA"], 1820, 196) + "".join(cards) + left + right
    notes = ("Em vez de olhar loja por loja, olhamos o Atacadão inteiro. O preço de gôndola (PDV) é coletado por região e mês, então cada "
             "combinação região × mês é uma observação de preço. Ordenamos essas combinações do preço mais baixo ao mais alto e cortamos em 10 "
             "faixas. Em cada faixa, calculamos o preço médio e quantas peças, em média, cada loja vendeu no mês. Isso tira o ruído de loja. O que o "
             "agrupamento não tira é a diferença entre regiões: as faixas baratas são quase todas de SP.\n\nNo Duralex, as faixas 3 e 5 são 100% SP "
             "e as faixas 7 a 10, 0% SP; na Lasanheira, as combinações de SP ficam entre R$ 48 e R$ 75 e as das demais regiões entre R$ 80 e R$ 130.")
    sub = ("O tratamento: juntar o Atacadão inteiro em 10 faixas de preço e usar o volume médio por loja em cada faixa, o que tira o ruído de "
           "loja e deixa 10 pontos por item para a reta.")
    foot = (f"Fonte: base conciliada, {CAIXA}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; Mtrix (sell-through) e SAP "
            f"(sell-in) não entram; cálculo DOC das faixas nacionais de preço (decis das combinações região × mês) | Elaboração: DOC Consulting. {PER_VP}")
    return slide("s09", "Faixas nacionais", sub, body, foot, "09", notes)


SLIDES_A = [s01, s02, s03, s04, s05, s06, s07, s08, s09]

from lib import *
from data import *

F_FAIXAS = (f"Fonte: base conciliada, {CAIXA}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; Mtrix (sell-through) e SAP "
            f"(sell-in) não entram; cálculo DOC das faixas nacionais de preço")


def table(left, top, width, title, head, widths, rows, size=13, head_bg=PANEL, head_color=G1, row_colors=None, group_bg=None, pad="4px 7px"):
    th = "".join(f'<th style="width:{w}%;color:{head_color};font-weight:700;text-align:{"left" if i == 0 else "right"}">{e(h)}</th>'
                 for i, (h, w) in enumerate(zip(head, widths)))
    trs = [f'<tr style="background:{head_bg}">{th}</tr>']
    for ri, r in enumerate(rows):
        if isinstance(r, str):  # group row
            cells = f'<td style="font-weight:700">{e(r)}</td>' + "".join("<td></td>" for _ in head[1:])
            trs.append(f'<tr style="background:{group_bg or PANEL}">{cells}</tr>')
            continue
        col = row_colors[ri] if row_colors else INK
        cells = "".join(f'<td style="color:{col};text-align:{"left" if i == 0 else "right"}">{e(c)}</td>' for i, c in enumerate(r))
        trs.append(f"<tr>{cells}</tr>")
    t = (f'<table style="font-size:{size}px;line-height:1.25;color:{INK};padding:{pad};border:none">{"".join(trs)}</table>')
    tt = p(title, 16, INK, bold=True) if title else ""
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px;display:flex;flex-direction:column;gap:8px">'
            f'{tt}{t}</div>')


# ------------------------------------------------------------------ A1
def a1():
    head = ["Faixa", "Preço médio (R$)", "Mín a máx (R$)", "Comb.", "Lojas-mês", "Peças por loja-mês", "% SP", "% promo", "P10 / Med / P90", "CV"]
    w = [6, 10, 15, 7, 9, 12, 7, 8, 17, 9]
    out = []
    for k, it in enumerate(ITEMS):
        rows = [(f"F{f[0]}", num(f[1], 2), f"{num(f[2], 2)} a {num(f[3], 2)}", str(f[4]), num(f[5], 0), num(f[6], 1), f"{f[7]}%", f"{f[8]}%",
                 f"{num(f[9], 0)} / {num(f[10], 0)} / {num(f[11], 0)}", num(f[12], 2)) for f in FAIXAS[it]]
        x = 100 + (k % 2) * 875
        y = 212 + (k // 2) * 384
        out.append(table(x, y, 845, f"Faixas nacionais de preço: {FULL[it]} · margem SAP {num(MARGIN[it] * 100, 1)}%", head, w, rows, 13))
    body = seals(["COMPROVADA"], 1820, 176) + "".join(out)
    notes = ("Tabela de consulta; mostra de onde sai cada ponto das retas. Peças por loja-mês = peças vendidas ÷ lojas-mês na venda no caixa "
             "das lojas do Atacadão, marcada como sell-out. CV = desvio padrão ÷ média do volume das lojas-mês na faixa. P10, Med e P90 = 10º "
             "percentil, mediana e 90º percentil das peças por loja-mês.")
    return slide("a1", "A1 · Faixas de preço", "As 10 faixas de cada item, com o preço, o volume por loja-mês, o CV e quanto do dado vem de SP.",
                 body, F_FAIXAS + f" | Elaboração: DOC Consulting. {PER_VP}", "18", notes)


# ------------------------------------------------------------------ A2
def a2():
    cw = 160
    hdr = [p("Item", 13, G1, bold=True, extra="width:150px;")] + [
        p(c, 13, BLUE if i == 0 else G1, bold=True, lh=1.25, extra=f"width:{cw}px;") for i, c in enumerate(ROBUST_COLS)]
    rows = [f'<div style="display:flex;flex-direction:row;gap:12px;align-items:end;padding:0px 0px 10px 0px;border-bottom:2px solid {INK}">{"".join(hdr)}</div>']
    for it in ITEMS:
        cells = [p(it, 20, INK, bold=True, extra="width:150px;")]
        for i, (b, pv, r2) in enumerate(ROBUST[it]):
            col = BLUE if i == 0 else INK
            sub = f"p {pv} · R² {r2}" if pv else "p e R²: não se aplica"
            cells.append(f'<div style="width:{cw}px;display:flex;flex-direction:column;gap:2px">{p(num(b, 2, sign=True), 22, col, bold=True, lh=1.1)}'
                         f'{p(sub, 12, G1, lh=1.2)}</div>')
        rows.append(f'<div style="display:flex;flex-direction:row;gap:12px;align-items:center;padding:14px 0px;border-bottom:1px solid {G4}">{"".join(cells)}</div>')
    grid = (f'<div style="position:absolute;left:100px;top:250px;width:1720px;display:flex;flex-direction:column">{"".join(rows)}</div>')
    notes_txt = [
        "O CD 111-MATRIZ CD/AT é sell-through e não entra em nenhuma versão: sell-out e sell-through nunca se juntam.",
        "\"Todos os pontos\" com erro agrupado por região × mês, porque o preço só varia nesse nível; M5 com R² dentro da loja; curva de especificações sem p-valor e R² porque é a mediana de 118 a 126 versões do cálculo.",
        "As 26 unidades -AT (marcadas como sell-out, vendem caixa fechada) são 33,8% do volume do Copo nas combinações com preço, 1,1% do Duralex e 0,1% da Opaline e da Lasanheira. Corte do 1% maior: 33.065 peças por loja-mês no Copo, 153 no Duralex, 425 na Opaline e 22 na Lasanheira.",
    ]
    nb = "".join(p(t, 16, INK if i == 0 else G1, bold=(i == 0), lh=1.4) for i, t in enumerate(notes_txt))
    body = "".join([
        P("Sensibilidade do volume ao preço nas faixas nacionais por versão do cálculo", 100, 212, 1100, 18, INK, bold=True),
        seals(["COMPROVADA"], 1820, 208), grid,
        f'<div style="position:absolute;left:100px;top:742px;width:1720px;display:flex;flex-direction:column;gap:10px;background:{PANEL};border-radius:16px;padding:20px 24px">{nb}</div>',
    ])
    notes = ("A forma de agrupar e a limpeza de extremos mexem pouco nos números do Duralex, da Opaline e da Lasanheira, e o Copo continua sem "
             "leitura em todas as versões. O que não fazemos em nenhuma versão é misturar o sell-through do CD com a venda no caixa das lojas, "
             "marcada como sell-out. Faixas de 95% de cada versão na seção de dados do estudo; as das 10 faixas estão no slide 10 e no anexo A3.")
    foot = (f"Fonte: base conciliada, {CAIXA2}); preço de gôndola (PDV) da coleta Involves por macrorregião × mês; Mtrix (sell-through) não entra; "
            f"cálculo DOC das faixas nacionais de preço; M5 e curva de especificações do Excel v8.1 (02/10/2026), abas Resumo e Resumo da curva | "
            f"Elaboração: DOC Consulting. {PER_VP}")
    return slide("a2", "A2 · Robustez e sanitização", "A conclusão não muda com outra forma de agrupar nem sem os extremos e as unidades -AT; o "
                 "sell-through nunca entra.", body, foot, "19", notes)


# ------------------------------------------------------------------ A3
def a3():
    head = ["Recorte", "Sensib.", "Faixa de 95%", "p-valor", "R²", "Combinações"]
    w = [30, 11, 22, 13, 9, 15]
    out = []
    for k, it in enumerate(ITEMS):
        n = NAT[it]
        rows = [("Nacional (10 faixas)", num(n["b"], 2, sign=True), f"{num(n['ci'][0], 2)} a {num(n['ci'][1], 2)}", n["p"], n["r2"], str(COMB[it]))]
        cols = [BLUE]
        for pk, lab in [("pequenas", "Lojas pequenas"), ("médias", "Lojas médias"), ("grandes", "Lojas grandes")]:
            b, ci, pv, r2, *_ = PORTE[it][pk]
            rows.append((lab, num(b, 2, sign=True), f"{num(ci[0], 2)} a {num(ci[1], 2)}", pv, r2, "a validar"))
            cols.append(G2 if ci[0] < 0 < ci[1] else INK)
        for lab in ["Só SP", "Fora de SP", "Meses sem promoção", "2025", "2026"]:
            b, ci, pv, r2, c = OUTROS[it][lab]
            rows.append((lab, num(b, 2, sign=True), f"{num(ci[0], 2)} a {num(ci[1], 2)}", pv, r2, str(c)))
            cols.append(G2 if ci[0] < 0 < ci[1] else INK)
        x = 100 + (k % 2) * 875
        y = 212 + (k // 2) * 372
        out.append(table(x, y, 845, f"{FULL[it]}", head, w, rows, 15, row_colors=cols, pad="5px 8px"))
    body = (P("Sensibilidade do volume ao preço por recorte, item a item · azul = nacional; cinza = faixa de 95% passa pelo zero", 100, 176, 1400, 16, G1)
            + seals(["COMPROVADA"], 1820, 176) + "".join(out))
    notes = ("Tabela de consulta dos recortes. A faixa de 95% é o intervalo de confiança da sensibilidade do volume ao preço. Linhas em cinza: a "
             "faixa de 95% passa pelo zero. Combinações região × mês das retas por porte: a validar (não informadas na base de números). No "
             "Duralex, \"Meses sem promoção\" é igual ao Nacional: nenhuma combinação com promoção.")
    foot = F_FAIXAS + f" por recorte | Elaboração: DOC Consulting. {PER_VP}"
    return slide("a3", "A3 · Recortes", "Sensibilidade, faixa de 95%, p-valor e R² de cada recorte: a base dos slides 11 e 12.", body, foot, "20", notes)


# ------------------------------------------------------------------ A4
def a4():
    cards = [("1 · Volume necessário", "Quanto o volume precisa subir para manter a margem bruta total.", "m ÷ (m + Δp) − 1"),
             ("2 · Sensibilidade de empate", "A sensibilidade do volume ao preço que faz a baixa empatar.", "ln[m ÷ (m + Δp)] ÷ ln(1 + Δp)"),
             ("3 · Volume esperado", "O que a sensibilidade estimada diz que a baixa traz.", "(1 + Δp)^β − 1"),
             ("4 · Variação da margem bruta total", "O efeito final na margem, com o volume esperado.", "(1 + Δp)^β × (m + Δp) ÷ m − 1")]
    ch = "".join(f'<div style="width:410px;background:{PANEL};border-radius:18px;padding:24px 24px;display:flex;flex-direction:column;gap:14px">'
                 f'{h3(t)}{p(d, 17, INK)}<div style="background:{WHITE};border-radius:12px;padding:16px 16px">{p(f, 22, BLUE, bold=True, lh=1.3)}</div></div>'
                 for t, d, f in cards)
    leg = p("m = margem SAP (margem bruta ÷ Net Net) · Δp = variação do preço (−0,10 para uma baixa de 10%) · β = sensibilidade do volume ao preço", 18, INK)
    ex = p("Exemplo do Copo, baixa de 10%: volume necessário = 0,296 ÷ 0,196 − 1 = +51,0%; sensibilidade de empate = −3,91.", 18, INK, bold=True)
    prem = ("Premissas: repasse integral da baixa ao preço de gôndola (PDV), não medido (sem repasse, o volume não vem e a baixa vira só perda); "
            "custo por peça constante; sem efeito sobre outros itens Nadir nem reação de concorrente; margem SAP de jun/25 a mai/26; reta usada "
            "só dentro da faixa de preço observada. P-valor e R²: não se aplica (fórmulas).")
    body = "".join([
        seals(["COMPROVADA"], 1820, 200),
        f'<div style="position:absolute;left:100px;top:236px;width:1720px;display:flex;flex-direction:row;justify-content:space-between">{ch}</div>',
        f'<div style="position:absolute;left:100px;top:620px;width:1720px;display:flex;flex-direction:column;gap:14px">{leg}{ex}</div>',
        f'<div style="position:absolute;left:100px;top:780px;width:1720px;border:1px solid {G3};border-radius:16px;padding:20px 24px">{p(prem, 17, INK, lh=1.45)}</div>',
    ])
    notes = "Toda conta de margem do deck sai destas quatro fórmulas."
    foot = ("Fonte: margem SAP Nadir (sell-in; margem bruta ÷ Net Net, cascata de margem SAP, Atacadão); cálculo DOC | Elaboração: DOC Consulting. "
            "Período: margem SAP de jun/25 a mai/26.")
    return slide("a4", "A4 · A conta", "As quatro fórmulas do deck e as premissas que valem para todas.", body, foot, "21", notes)


# ------------------------------------------------------------------ A5
def a5():
    rows = [("Copo", "24", "72", "720", "4.926 (9)"), ("Duralex", "24", "24", "168", "3.473 (11)"),
            ("Opaline", "24", "24", "142", "2.072 (11)"), ("Lasanheira", "4", "8", "44", "2.114 (10)")]
    tbl = mini_table(rows, [100, 52, 76, 70, 110], 16, head=["Item", "P10", "Mediana", "P90", "Pontos × mês (redes)"])
    body = "".join([
        P("Volume por ponto de venda no mês contra o preço: sell-through (distribuidores, atacados, CD e Mtrix)", 100, 216, 1100, 18, INK, bold=True),
        seals(["COMPROVADA"], 1290, 212),
        placeholder(100, 256, 1190, 700, "Gráfico A · Sell-through à parte",
                    "Deck faixas - Gráfico A - Sell-through à parte - 02-10-2026.png",
                    "Legenda e eixos já vêm no PNG: cada ponto = venda de um distribuidor, atacado ou CD ao varejo num mês. X: preço por peça "
                    "(R$, escala log). Y: peças por ponto de venda no mês (escala log). Nunca ao lado do sell-out no mesmo eixo."),
        rail([("Sell-through por ponto de venda × mês", tbl, "info"),
              ("Leitura", p("O Mtrix registra compras em múltiplos da caixa (24 peças): por isso as linhas horizontais. O CD 111-MATRIZ CD/AT "
                            "vendeu 4,47 milhões de peças de Copo nas combinações com preço. O Paraty entra uma vez só (BASE SO).", 15), "info"),
              ("O que decidir", p("Manter o sell-through fora das contas de preço e margem: ele não mede a compra do consumidor.", 17, bold=True), "decide")]),
    ])
    notes = ("Este é o sell-through, mostrado sozinho para ficar claro o que deixamos de fora e por quê.\n\nSell-through por ponto de venda × mês "
             "(10º percentil, mediana e 90º percentil): Copo 24, 72 e 720 peças (4.926 pontos de venda × mês, 9 redes); Duralex 24, 24 e 168 "
             "(3.473; 11); Opaline 24, 24 e 142 (2.072; 11); Lasanheira 4, 8 e 44 (2.114; 10). O Paraty aparece na BASE SO e no Mtrix: entra uma "
             "vez só (BASE SO). Tabela por rede no anexo A6. Sensibilidade, p-valor e R²: não se aplica (descrição da base).")
    sub = ("O sell-through mede a venda de distribuidores, atacados e do CD ao varejo, não a compra do consumidor; por isso fica fora de todas as "
           "contas e aparece só aqui, sozinho.")
    foot = ("Fonte: base conciliada, BASE SO (sell-through do CD 111-MATRIZ CD/AT, de distribuidores e de atacados; empresa fonte não informada) e "
            "Mtrix (sell-through dos distribuidores ao varejo); preço = faturamento ÷ peças (preço de venda ao varejo), exceto o CD, com preço de "
            "gôndola (PDV) da coleta Involves; sell-out fora do gráfico | Elaboração: DOC Consulting. Período: BASE SO de jan/25 a mai/26; Mtrix em "
            "jan a jul de 2025 e 2026.")
    return slide("a5", "A5 · Sell-through à parte", sub, body, foot, "22", notes)


# ------------------------------------------------------------------ A6
def net_rows(groups, keys):
    rows = []
    for k in keys:
        rows.append(k)
        for r in groups[k]:
            rede, canal, fonte, ponto, preco, n, pm, pct = r
            ponto = {"conta (total da rede)": "conta (rede)", PDV: "PDV atendido"}.get(ponto, ponto)
            rows.append((rede, canal, fonte, ponto, preco, n, pm, pct))
    return rows


A6_HEAD = ["Rede", "Canal", "Fonte", "Ponto de venda", "Preço usado", "Pontos × mês", "Preço med. (R$)", "P10 / Med / P90"]
A6_W = [22, 10, 8, 11, 16, 8, 8, 17]
A6_FOOT = ("Fonte: base conciliada com fonte e tipo de dado: BASE SO (sell-out e sell-through, em tabelas separadas; empresa fonte não informada) "
           "e Mtrix (sell-through); preço de gôndola (PDV) da coleta Involves quando há coleta, senão faturamento ÷ peças; redes com 8 pontos × mês "
           "ou mais | Elaboração: DOC Consulting. Período: BASE SO de jan/25 a mai/26; Mtrix em jan a jul de 2025 e 2026.")


def a6_slide(sid, title, groups, head_bg, group_bg, page, label, note_extra):
    keys = list(groups)
    t1 = table(100, 250, 845, None, A6_HEAD, A6_W, net_rows(groups, keys[:2]), 12, head_bg=head_bg, head_color=WHITE, group_bg=group_bg, pad="3px 6px")
    t2 = table(975, 250, 845, None, A6_HEAD, A6_W, net_rows(groups, keys[2:]), 12, head_bg=head_bg, head_color=WHITE, group_bg=group_bg, pad="3px 6px")
    body = "".join([
        P(label, 100, 212, 1300, 18, INK, bold=True),
        seals(["COMPROVADA"], 1820, 208), t1, t2,
        P("Ponto de venda: conta (rede) = total da rede; PDV atendido = PDV atendido pelo distribuidor. P10 / Med / P90 = 10º percentil, mediana e "
          "90º percentil de peças por ponto de venda no mês. " + note_extra, 100, 940, 1720, 13, G1),
    ])
    notes = ("Tabela de consulta. Rede a rede, o volume por ponto de venda depende do formato do ponto. Sell-out e sell-through ficam em tabelas "
             "separadas, nunca somadas.")
    return slide(sid, title, "Rede a rede, o volume por ponto de venda depende do formato do ponto; sell-out e sell-through em tabelas separadas.",
                 body, A6_FOOT, page, notes)


def a6():
    return a6_slide("a6", "A6 · Base completa por rede", SO, BLUE, LB1, "23", "Sell-out por rede (marcado como sell-out na base)",
                    "Sell-through por rede na página seguinte, em tabela separada.")


def a6b():
    return a6_slide("a6b", "A6 · Base completa por rede", ST, G1, G4, "24", "Sell-through por rede (fora das contas)",
                    "Nunca somar com a tabela de sell-out da página anterior.")


# ------------------------------------------------------------------ A7
def a7():
    W = [190, 400, 140, 190, 170, 160, 330]
    head = ["Base", "Tipo de dado", "Empresa fonte", "Uma linha é", "Período", "Linhas", "Uso no deck"]
    chipc = {"Sell-out": (BLUE, WHITE), "Sell-through": (G1, WHITE), "Preço de gôndola (PDV)": (LB2, INK), "Sell-in": (INK, WHITE)}
    data = [
        ("BASE SO da base conciliada, sell-out", "Sell-out", "Na marcação da base: venda no caixa de lojas, UFs e contas; no atacarejo inclui o pequeno comerciante (papel de sell-through), sem separação; inclui as 26 unidades -AT, que vendem caixa fechada.",
         "Não informada na base", "cliente × loja × SKU × mês", "jan/25 a mai/26", "339.077 linhas, 18 clientes", "Volume de todas as contas."),
        ("BASE SO da base conciliada, sell-through", "Sell-through", "CD 111-MATRIZ CD/AT, distribuidores e atacados.", "Não informada na base",
         "cliente × ponto × SKU × mês", "jan/25 a mai/26", "21.636 linhas, 6 clientes", "Fora das contas; só no anexo."),
        ("Mtrix", "Sell-through", "Distribuidor para a loja de varejo.", "Mtrix", "distribuidor × PDV × SKU × mês", "jul/24; jan a jul/25; jan a jul/26",
         "232.243 linhas, 7 distribuidores", "Fora das contas; só no anexo."),
        ("Coleta de preço", "Preço de gôndola (PDV)", "Coleta em loja.", "Involves", "rede × macrorregião × SKU × data", "28/04/2025 a 30/05/2026",
         "868.065 brutas; 454.947 com preço", "Preço por macrorregião × mês."),
        ("SAP sell-in por nota fiscal (4 itens)", "Sell-in", "Venda da Nadir ao cliente.", "SAP Nadir", "item de nota fiscal", "jan/25 a jun/26", "15.580",
         "Preço Nadir e custo."),
        ("Cascata de margem SAP", "Sell-in", "Sell-in agregado.", "SAP Nadir, agregada pela DOC", "mês × SKU × grupo de cliente", "jan/25 a jun/26", "329",
         "Margem SAP (margem bruta ÷ Net Net), jun/25 a mai/26: Copo 29,6%, Duralex 64,6%, Opaline 54,2%, Lasanheira 66,8%."),
    ]
    rows = [f'<div style="display:flex;flex-direction:row;gap:14px;padding:0px 0px 8px 0px;border-bottom:2px solid {INK}">'
            + "".join(p(h, 13, G1, bold=True, extra=f"width:{w}px;") for h, w in zip(head, W)) + "</div>"]
    for base, tipo, desc, emp, linha, per, n, uso in data:
        bg, fg = chipc[tipo]
        chip = (f'<div style="display:flex;flex-direction:row"><p style="font-size:12px;font-weight:700;color:{fg};background:{bg};border-radius:6px;'
                f'padding:3px 8px;line-height:1.2">{e(tipo)}</p></div>')
        cells = [p(base, 14, INK, bold=True, extra=f"width:{W[0]}px;"),
                 f'<div style="width:{W[1]}px;display:flex;flex-direction:column;gap:4px">{chip}{p(desc, 13, INK, lh=1.3)}</div>']
        cells += [p(v, 14, INK, lh=1.3, extra=f"width:{w}px;") for v, w in zip([emp, linha, per, n, uso], W[2:])]
        rows.append(f'<div style="display:flex;flex-direction:row;gap:14px;padding:10px 0px;border-bottom:1px solid {G4}">{"".join(cells)}</div>')
    body = (P("Bases do estudo", 100, 212, 600, 18, INK, bold=True) + seals(["COMPROVADA"], 1820, 208)
            + f'<div style="position:absolute;left:100px;top:252px;width:1720px;display:flex;flex-direction:column">{"".join(rows)}</div>')
    notes = "Tabela de consulta das bases."
    return slide("a7", "A7 · Bases de dados", "As seis bases do estudo, com o tipo de dado, a empresa fonte, o período e o uso de cada uma.",
                 body, F_BASES, "25", notes)


SLIDES_C = [a1, a2, a3, a4, a5, a6, a6b, a7]

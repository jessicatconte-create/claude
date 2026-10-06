"""Status Report semanal PremieRpet | Projeto Politica Comercial.

Gera um HTML compativel com e-mail (Outlook/Gmail): tabelas, estilos inline,
sem CSS externo. Segue o template visual do Status Report da DOC (cabecalho
navy, secoes em caixas de fundo suave). Todo o conteudo fica nos dados
abaixo; para a proxima semana, atualize os dados e rode:  python3 build.py
"""
from pathlib import Path

# ---------------------------------------------------------------- identidade
NAVY = "#0B1F3A"; INK = "#1F2937"; SUB = "#6B7280"; MUTE = "#9CA3AF"
LINE = "#E5E7EB"; BLUE = "#1A56DB"
FONT = "'Segoe UI', Arial, Helvetica, sans-serif"
W = 760

# caixas por secao (fundo, borda, cor do titulo) - mesmas do template original
BOX = {
    "cinza":    ("#F8FAFC", "#E2E8F0", "#334155"),
    "vermelho": ("#FEF2F2", "#FECACA", "#B91C1C"),
    "verde":    ("#ECFDF5", "#A7F3D0", "#047857"),
    "azul":     ("#EFF6FF", "#BFDBFE", BLUE),
    "branco":   ("#FFFFFF", LINE, "#334155"),
}

# Criterios objetivos de status (mesma escala para atividade e entrega)
STATUS = {
    "Concluído":    ("#15803D", "Critério de conclusão atendido e validado pela PremieRpet."),
    "Em andamento": (BLUE,      "Iniciado, dependências em dia, prazo preservado."),
    "Em atenção":   ("#B45309", "Prazo preservado, mas com dependência pendente, sem dono/data ou fora de sequência."),
    "Atrasado":     ("#B91C1C", "Prazo vencido, ou dependência vencida que já compromete a data."),
    "Não iniciado": ("#6B7280", "Início previsto para data futura."),
}

META = {
    "numero": "#2", "data": "02/10/2026", "versao": "versão revisada",
    "titulo": "PremieRpet | Projeto Política Comercial",
    "saude": "Em atenção",
    "saude_txt": "Piloto GO/DF mantido para jan/27. A Política Comercial (13/10) pode sair parcial por uma "
                 "dependência vencida desde 23/09.",
}

SUMARIO = [
    ("Onde estamos.",
     "Desenho da nova política comercial do piloto GO/DF, com início mantido em janeiro/2027. "
     "Na semana, fechamos três definições do piloto (ver Avanços)."),
    ("O que está em risco.",
     "A Política Comercial (13/10) pode sair parcial: a base de apuração da remuneração VI, com a Gisele, "
     "venceu em 23/09 e ainda não foi recebida. O Business Case (30/10) tem dois pontos de atenção: a base de "
     "clientes do piloto não tem responsável e o item de capacidade depende da Governança, prevista só para 06/11."),
    ("O que muda no plano.",
     "O Business Case passa a trazer a lógica econômica <i>ex ante</i> do piloto antes da decisão de "
     "implementação, e o Protocolo do Piloto vira entrega acompanhada semanalmente."),
]

# Decisoes necessarias / escalonamentos
DECISOES = [
    ("Escalonamento", "Priorizar a base de apuração da remuneração VI e fixar nova data de entrega.",
     "Sem ela, metas e percentuais da Política Comercial saem sem calibração histórica.",
     "Michelle Uema, com a Gisele", "09/10"),
    ("Decisão", "Critério de apuração: 100% dos clientes, amostra ou média.",
     "Trava a regra de apuração da Governança e a mecânica da Banda/RTP.",
     "Gisele", "09/10"),
    ("Decisão", "Apuração meta x realizado no piloto: manual ou semiautomatizada.",
     "Folga de só 5 dias até a entrega de Banda/RTP (21/10).",
     "Henrique (TI) e Yves (IC)", "16/10"),
    ("Decisão", "Responsável e data da base de clientes do piloto.",
     "Sem baseline, Business Case e Protocolo não fecham em 30/10.",
     "PremieRpet (a indicar)", "09/10*"),
]

# Entregas: saude da ENTREGA + por que + criterio de conclusao
ENTREGAS = [
    ("1. Política Comercial", "13/10", "Em atenção",
     "Dependência vencida desde 23/09 (base remuneração VI, Gisele).",
     "tabela de preço e camadas por canal com pocket price; metas, percentuais e elegibilidade por alavanca "
     "(sell-in volume e mix); simulação do investimento por faixa de atingimento; validação com RGM/Comercial."),
    ("2. Economia dos Canais", "14/10", "Em andamento",
     "Visita ao distribuidor GO em 06–07/10 alimenta a DRE.",
     "DRE do distribuidor GO validada com dados de campo; economia de cada canal, modelo atual x proposto."),
    ("3. Banda, RTP e incentivo ao shopper", "21/10", "Em andamento",
     "Depende da decisão TI + IC em 16/10.",
     "banda de preço por SKU/canal; mecânica da RTP on-invoice (SKU → pedido); cenários de impacto em preço, "
     "volume e margem."),
    ("5. Business Case <i>ex ante</i>", "30/10", "Em atenção",
     "Base de clientes do piloto sem responsável; capacidade depende da Governança (06/11).",
     "investimento previsto; impacto em volume, mix e margem; incrementalidade necessária; ROI esperado e "
     "break-even em três cenários; premissas e sensibilidades. <b>A decisão de implementar o piloto é tomada "
     "com ele aprovado</b>; jan–abr/27 mede só o resultado realizado."),
    ("4. Governança", "06/11", "Em andamento",
     "Plano de ação com TI, IC e Gisele em curso.",
     "macrofluxo de apuração, pagamento e exceções com RACI; critério e calendário de apuração; guardrails; "
     "validação de Trade, RGM, IC e TI."),
    ("5.1 Protocolo do Piloto", "30/10* (v0)", "Não iniciado",
     "Nova entrega. Versão final em 30/11.",
     "os oito componentes abaixo definidos e aprovados."),
]

# Avancos: resultado + implicacao
AVANCOS = [
    ("O piloto não depende da nova ferramenta.",
     "Apuração manual ou semiautomatizada tira a ferramenta do caminho crítico de jan/27."),
    ("RTP on-invoice validada no menor nível (SKU → pedido).",
     "A RTP pode ser desenhada direto na nota, por SKU, sem reembolso posterior."),
    ("Apuração meta x realizado será manual, com prévia uma semana antes do fechamento.",
     "Reduz o risco de desconto indevido e protege o recebimento; calendário entra na Governança."),
    ("Início do piloto mantido em janeiro/2027.",
     "Entregas de out–nov seguem dimensionadas para esse marco."),
]
EM_CURSO = ("Base de descontos (01/10) e pesquisa de preços (02/10) recebidas e em análise; "
            "conclusões entram no próximo status.")

# Pendencias criticas: todos os campos, em destaque
CRITICAS = [
    {"o_que": "Base de apuração da remuneração VI via distribuidor", "quem": "Gisele",
     "prazo": "23/09 → sem nova data", "entrega": "1. Política Comercial",
     "impacto": "Metas e percentuais calibrados só por premissa; entrega parcial em 13/10.",
     "acao": "Reunião com a Gisele até 09/10; sem data firme, escalonar.", "status": "Atrasado"},
    {"o_que": "Base de informações dos clientes do piloto", "quem": "PremieRpet (a indicar)",
     "prazo": "não definido", "entrega": "5. Business Case e Protocolo",
     "impacto": "Sem baseline não há incrementalidade, break-even nem grupo de comparação.",
     "acao": "Indicar responsável e data até 09/10*.", "status": "Em atenção"},
    {"o_que": "Governança preliminar (macrofluxo + RACI)", "quem": "DOC",
     "prazo": "06/11 → 23/10*", "entrega": "5. Business Case (capacidade)",
     "impacto": "O Business Case de 30/10 depende de um insumo previsto para depois dele.",
     "acao": "Antecipar uma versão preliminar para 23/10*.", "status": "Em atenção"},
]
# Pendencias em dia: prazo original = atual
EM_DIA = [
    ("Critério de apuração (100%, amostra ou média)", "Gisele", "09/10", "Governança; Banda/RTP"),
    ("Fluxo mapeado e possibilidades de automação", "Henrique (TI)", "16/10", "Banda/RTP; Governança"),
    ("Fluxo e alternativas avaliados", "Yves (IC) e Henrique (TI)", "16/10", "Banda/RTP; Governança"),
    ("Validação da abertura das metas nos distribuidores", "Fábio Marconi (DOC)", "06–07/10", "Política; Economia"),
    ("Consistência da base de descontos", "DOC", "09/10", "Política Comercial"),
    ("Validação da pesquisa de preços", "DOC", "07/10", "Banda/RTP"),
]

# Protocolo do piloto: acompanhamento semanal
PROTOCOLO = [
    ("Hipótese", "Não iniciado"), ("Baseline", "Em atenção"),
    ("Grupo / contrafactual", "Não iniciado"), ("Mecânica", "Em andamento"),
    ("Investimento", "Não iniciado"), ("KPIs", "Não iniciado"),
    ("Critérios de sucesso", "Não iniciado"), ("Regra de decisão", "Não iniciado"),
]
PROTOCOLO_NOTA = ("Mecânica já tem RTP on-invoice e apuração manual definidas. Baseline depende da base de "
                  "clientes do piloto. Investimento e critério de sucesso saem do Business Case.")

# Cronograma por frente: Atividade | Owner | Prazo | Status | Dependencia/Bloqueio | Proximo marco
CRONOGRAMA = [
    ("1. Política Comercial", [
        ("Tabela, camadas e pocket price", "DOC", "13/10", "Em andamento", "Base de descontos em análise", "09/10 análise"),
        ("Metas, percentuais e elegibilidade", "DOC", "13/10", "Em atenção", "<b>Base VI (Gisele) vencida 23/09</b>", "09/10 reunião"),
        ("Simulação por atingimento", "DOC", "13/10", "Em andamento", "Itens acima", "13/10 entrega"),
    ]),
    ("2. Economia dos Canais", [
        ("Economia do distribuidor", "DOC", "14/10", "Em andamento", "Visita distribuidor GO", "06–07/10 visita"),
    ]),
    ("3. Banda e RTP", [
        ("Cenários quantitativos", "DOC", "21/10", "Em andamento", "Pesquisa de preços em validação", "07/10 validação"),
        ("Mecânica na governança", "DOC", "21/10", "Em andamento", "Decisão TI + IC", "16/10 decisão"),
    ]),
    ("5. Business Case <i>ex ante</i>", [
        ("Lógica econômica, ROI e break-even", "DOC", "30/10", "Não iniciado", "<b>Base clientes piloto sem dono</b>", "09/10* dono"),
        ("As Is x To Be e transição", "DOC", "30/10", "Não iniciado", "Entregas 1–3", "21/10 insumos"),
        ("Capacidade, treinamento, sustentação", "DOC", "30/10", "Em atenção", "<b>Governança só em 06/11</b>", "23/10* prévia"),
    ]),
    ("4. Governança", [
        ("Apuração, pagamento e exceções", "DOC", "06/11", "Em andamento", "Trade, RGM, IC e TI", "09/10 critério"),
        ("Guardrails e trava de complexidade", "DOC", "06/11", "Não iniciado", "Decisão TI + IC", "16/10 decisão"),
    ]),
    ("5.1 Piloto", [
        ("Protocolo do piloto", "DOC", "30/10* · 30/11", "Não iniciado", "Business Case; base clientes", "30/10* v0"),
        ("Campo, dados e validações", "DOC", "30/11", "Em andamento", "Visita campo GO", "06–07/10 visita"),
        ("Medição <i>ex post</i> (ROI realizado)", "DOC", "jan–abr/27", "Não iniciado", "Protocolo aprovado", "30/11 protocolo"),
    ]),
    ("6. Implementação", [
        ("Treinamento equipe comercial", "DOC", "a definir", "Não iniciado", "Política piloto validada", "30/10 data"),
        ("Rollout Brasil (4 meses)", "PremieRpet", "abr–ago/27", "Não iniciado", "Resultado do piloto", "02/04/27 decisão"),
    ]),
]

AGENDA = [
    ("06–07/10", "Campo GO: visita ao distribuidor"),
    ("07/10", "Reunião prévia: Política Comercial"),
    ("09/10", "Gisele: critério de apuração e base VI"),
    ("13/10", "<b>Entrega 1</b> · Política Comercial"),
    ("14/10", "<b>Entrega 2</b> · Economia dos Canais"),
    ("16/10", "TI + IC: apuração manual x semiautomatizada"),
    ("21/10", "<b>Entrega 3</b> · Banda, RTP e incentivo ao shopper"),
    ("30/10", "<b>Entrega 5</b> · Business Case <i>ex ante</i> + Protocolo v0*"),
    ("06/11", "<b>Entrega 4</b> · Governança"),
]


# ---------------------------------------------------------------- render
def st(status, size=12):
    c = STATUS[status][0]
    return (f'<span style="color:{c};font-size:{size}px;font-weight:600;white-space:nowrap">'
            f'&#9679;&nbsp;{status}</span>')


def label(text, color):
    return (f'<p style="margin:0 0 12px 0;font-family:{FONT};font-size:10.5px;font-weight:700;'
            f'letter-spacing:1.6px;text-transform:uppercase;color:{color}">{text}</p>')


def box(title, body, kind="cinza"):
    bg, bd, tc = BOX[kind]
    return (f'<tr><td style="padding:0 32px 18px 32px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{bg};border:1px solid {bd}"><tr><td style="padding:18px 20px">'
            f'{label(title, tc)}{body}</td></tr></table></td></tr>')


def p(text, size=13, color=INK, mb=10, lh=1.55):
    return (f'<p style="margin:0 0 {mb}px 0;font-family:{FONT};font-size:{size}px;line-height:{lh};'
            f'color:{color}">{text}</p>')


def rows(cells_list, widths, size=12.5, pad="9px 0", sep=True, valign="top"):
    out = []
    for i, cells in enumerate(cells_list):
        b = f"border-top:1px solid {LINE};" if (sep and i) else ""
        tds = "".join(
            f'<td valign="{valign}" width="{w}" style="padding:{pad};{b}font-family:{FONT};font-size:{size}px;'
            f'line-height:1.45;color:{INK}">{c}</td>' for c, w in zip(cells, widths))
        out.append(f"<tr>{tds}</tr>")
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{"".join(out)}</table>')


def head(cells, widths):
    return "".join(
        f'<td width="{w}" style="padding:0 0 6px 0;border-bottom:1px solid #CBD5E1;font-family:{FONT};'
        f'font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:{SUB}">{c}</td>'
        for c, w in zip(cells, widths))


def small(t, color=SUB):
    return f'<span style="font-size:11.5px;color:{color}">{t}</span>'


def build():
    o = []
    # cabecalho (igual ao template)
    o.append(
        f'<tr><td style="background:{NAVY};padding:26px 32px">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
        f'<td valign="bottom" style="font-family:{FONT};font-size:10.5px;letter-spacing:2.4px;color:#94A3B8">'
        f'<span style="font-size:15px;letter-spacing:0;color:#FFFFFF;font-weight:700">DOC</span>'
        f'<span style="font-size:15px;letter-spacing:0;color:#94A3B8"> Consulting</span><br><br>'
        f'STATUS REPORT SEMANAL</td>'
        f'<td align="right" valign="top" style="font-family:{FONT};color:#FFFFFF">'
        f'<div style="font-size:16px;font-weight:700">{META["titulo"]}</div>'
        f'<div style="font-size:16px;font-weight:700;margin-top:6px">{META["numero"]}</div>'
        f'<div style="font-size:11.5px;color:#CBD5E1;margin-top:6px">{META["data"]} · {META["versao"]}</div>'
        f'</td></tr></table></td></tr>')

    # saude do projeto
    c = STATUS[META["saude"]][0]
    o.append(
        f'<tr><td style="padding:24px 32px 18px 32px">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
        f'<td width="4" style="background:{c}"></td>'
        f'<td style="padding:4px 0 4px 16px;font-family:{FONT}">'
        f'<div style="font-size:10.5px;font-weight:700;letter-spacing:1.6px;color:{SUB}">SAÚDE DO PROJETO</div>'
        f'<div style="font-size:20px;font-weight:700;color:{c};margin:4px 0 4px 0">{META["saude"]}</div>'
        f'<div style="font-size:13px;line-height:1.5;color:{INK}">{META["saude_txt"]}</div>'
        f'</td></tr></table></td></tr>')

    # sumario
    o.append(box("Sumário executivo",
                 "".join(p(f"<b>{k}</b> {v}", mb=8 if i < len(SUMARIO) - 1 else 0)
                         for i, (k, v) in enumerate(SUMARIO))))

    # decisoes
    body = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
            f'<tr>{head(["O que precisamos", "De quem", "Até"], [440, 150, 56])}</tr></table>')
    body += rows([[
        (f'<span style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;'
         f'color:{"#B91C1C" if t == "Escalonamento" else SUB}">{t}</span><br>'
         f'<b>{q}</b><br>{small(why)}'),
        quem, f"<b>{ate}</b>"] for t, q, why, quem, ate in DECISOES], [440, 150, 56], pad="10px 0")
    o.append(box("Decisões necessárias / Escalonamentos", body, "vermelho"))

    # entregas + criterio de conclusao
    body = ""
    for i, (nome, prazo, s, why, crit) in enumerate(ENTREGAS):
        b = f"border-top:1px solid {LINE};" if i else ""
        body += (
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td style="padding:12px 0 2px 0;{b}font-family:{FONT};font-size:13.5px;color:{NAVY}">'
            f'<b>{nome}</b>&nbsp;&nbsp;<span style="color:{SUB};font-size:12.5px">{prazo}</span></td>'
            f'<td align="right" style="padding:12px 0 2px 0;{b}font-family:{FONT}">{st(s)}</td></tr>'
            f'<tr><td colspan="2" style="padding:0 0 12px 0;font-family:{FONT};font-size:12.5px;line-height:1.5;'
            f'color:{INK}">{why}<br>{small("<b>Concluída quando:</b> " + crit)}</td></tr></table>')
    o.append(box("Entregas e critério de conclusão", body, "branco"))

    # avancos
    body = rows([[f"<b>{r}</b><br>{small(i)}"] for r, i in AVANCOS], [None], pad="8px 0")
    body += p(f"<b>Em curso, sem resultado ainda:</b> {EM_CURSO}", size=11.5, color=SUB, mb=0, lh=1.45)
    o.append(box("Avanços do ciclo · o que foi decidido ou validado", body, "verde"))

    # pendencias
    body = ""
    for i, x in enumerate(CRITICAS):
        b = f"border-top:1px solid {LINE};" if i else ""
        body += (
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td style="padding:12px 0 4px 0;{b}font-family:{FONT};font-size:13.5px;color:{INK}"><b>{x["o_que"]}</b></td>'
            f'<td align="right" style="padding:12px 0 4px 0;{b}font-family:{FONT}">{st(x["status"])}</td></tr>'
            f'<tr><td colspan="2" style="padding:0 0 12px 0;font-family:{FONT};font-size:12.5px;line-height:1.6;color:{INK}">'
            f'{small("De quem")} {x["quem"]} &nbsp;·&nbsp; {small("Prazo")} {x["prazo"]} &nbsp;·&nbsp; '
            f'{small("Impacta")} {x["entrega"]}<br>'
            f'{small("Impacto")} {x["impacto"]}<br>'
            f'{small("Próxima ação")} <b>{x["acao"]}</b></td></tr></table>')
    body += (f'<p style="margin:14px 0 6px 0;font-family:{FONT};font-size:10.5px;font-weight:700;letter-spacing:1px;'
             f'color:{SUB}">EM DIA (PRAZO ORIGINAL MANTIDO)</p>')
    ws = [270, 150, 64, 160]
    body += (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
             f'<tr>{head(["Pendência", "De quem", "Prazo", "Impacta"], ws)}</tr></table>')
    body += rows([list(r) for r in EM_DIA], ws, size=12, pad="7px 0")
    o.append(box("Pendências e dependências", body, "cinza"))

    # protocolo
    half = len(PROTOCOLO) // 2
    grid = rows([[f"{PROTOCOLO[i][0]}", st(PROTOCOLO[i][1], 11.5),
                  f"{PROTOCOLO[i + half][0]}", st(PROTOCOLO[i + half][1], 11.5)] for i in range(half)],
                [170, 150, 170, 150], size=12.5, pad="6px 0")
    o.append(box("Protocolo do piloto · evolução semanal",
                 grid + p(PROTOCOLO_NOTA, size=11.5, color=SUB, mb=0, lh=1.45).replace("margin:0 0 0px 0",
                                                                                     "margin:10px 0 0 0"),
                 "branco"))

    # cronograma
    ws = [190, 70, 78, 104, 150, 104]
    tr = []
    for frente, ativs in CRONOGRAMA:
        tr.append(f'<tr><td colspan="6" style="padding:12px 0 4px 0;font-family:{FONT};font-size:12px;'
                  f'font-weight:700;color:{NAVY}">{frente}</td></tr>')
        for a, ow, pz, s, dep, mk in ativs:
            tr.append("<tr>" + "".join(
                f'<td valign="top" width="{w}" style="padding:6px 8px 6px 0;border-top:1px solid {LINE};'
                f'font-family:{FONT};font-size:11.5px;line-height:1.4;color:{INK}">{c}</td>'
                for c, w in zip([a, ow, pz, st(s, 11), dep, mk], ws)) + "</tr>")
    body = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
            f'<tr>{head(["Atividade", "Owner", "Prazo", "Status", "Dependência / bloqueio", "Próximo marco"], ws)}</tr>'
            f'{"".join(tr)}</table>')
    o.append(box("Cronograma por frente", body, "branco"))

    # agenda
    body = rows([[f"<b>{d}</b>", m] for d, m in AGENDA], [90, None], size=12.5, pad="6px 0", sep=False)
    o.append(box("Próximos marcos", body, "azul"))

    # legenda
    leg = "".join(f'{st(k, 11)} {small(v[1], MUTE)}<br>' for k, v in STATUS.items())
    o.append(
        f'<tr><td style="padding:4px 32px 0 32px;font-family:{FONT};font-size:11px;line-height:1.7;color:{MUTE}">'
        f'{leg}<br>A entrega herda o pior status das suas dependências. '
        f'* Data proposta pela DOC, a confirmar com a PremieRpet. '
        f'Nesta edição: ROI e break-even do piloto passam ao Business Case <i>ex ante</i> (30/10); a medição de '
        f'jan–abr/27 fica só para o resultado realizado. Protocolo do piloto vira entrega própria.</td></tr>')

    o.append(f'<tr><td style="padding:24px 32px 28px 32px"><table role="presentation" width="100%" '
             f'cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid {LINE};padding-top:14px;'
             f'font-family:{FONT};font-size:10.5px;line-height:1.6;color:{MUTE};text-align:center">'
             f'DOC Consulting | Status report semanal<br>© 2026 DOC Consulting. Todos os direitos reservados.'
             f'</td></tr></table></td></tr>')

    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Status Report #2 – PremieRpet</title></head>'
        f'<body style="margin:0;padding:0;background:#F1F5F9">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F1F5F9">'
        f'<tr><td align="center" style="padding:24px 8px">'
        f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" '
        f'style="width:{W}px;max-width:100%;background:#FFFFFF">'
        + "".join(o) +
        '</table></td></tr></table></body></html>')


if __name__ == "__main__":
    dst = Path(__file__).with_name("status-report-02-premierpet.html")
    dst.write_text(build(), encoding="utf-8")
    print(f"ok -> {dst}")

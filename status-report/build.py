"""Status Report semanal PremieRpet | Projeto Politica Comercial.

Gera um HTML compativel com e-mail (Outlook/Gmail): tabelas, estilos inline,
sem CSS externo. Visual DOC (cabecalho navy, caixas arredondadas, etiquetas
de status) com estrutura executiva:
  - o titulo do documento e a resposta da semana;
  - cada secao abre com um titulo-acao (a frase que diz o "e dai?");
  - visao por pilar no corpo; detalhe por atividade so no anexo.
Todo o conteudo fica nos dados abaixo; para a proxima semana, atualize os
dados e rode:  python3 build.py
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
    "Concluído":    ("#15803D", "#DCFCE7", "Critério de conclusão atendido e validado pela PremieRpet."),
    "Em andamento": (BLUE,      "#DBEAFE", "Iniciado, dependências em dia, prazo preservado."),
    "Em atenção":   ("#B45309", "#FEF3C7", "Prazo preservado, mas com dependência pendente, sem dono/data ou fora de sequência."),
    "Atrasado":     ("#B91C1C", "#FEE2E2", "Prazo vencido, ou dependência vencida que já compromete a data."),
    "Não iniciado": ("#4B5563", "#F3F4F6", "Início previsto para data futura."),
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
    ("4. Governança", "06/11", "Em andamento",
     "Plano de ação com TI, IC e Gisele em curso.",
     "macrofluxo de apuração, pagamento e exceções com RACI; critério e calendário de apuração; guardrails; "
     "validação de Trade, RGM, IC e TI."),
    ("5. Business Case <i>ex ante</i>", "30/10", "Em atenção",
     "Base de clientes do piloto sem responsável; capacidade depende da Governança (06/11).",
     "investimento previsto; impacto em volume, mix e margem; incrementalidade necessária; ROI esperado e "
     "break-even em três cenários; premissas e sensibilidades. <b>A decisão de implementar o piloto é tomada "
     "com ele aprovado</b>; jan–abr/27 mede só o resultado realizado."),
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
    ("4. Governança", [
        ("Apuração, pagamento e exceções", "DOC", "06/11", "Em andamento", "Trade, RGM, IC e TI", "09/10 critério"),
        ("Guardrails e trava de complexidade", "DOC", "06/11", "Não iniciado", "Decisão TI + IC", "16/10 decisão"),
    ]),
    ("5. Business Case <i>ex ante</i>", [
        ("Lógica econômica, ROI e break-even", "DOC", "30/10", "Não iniciado", "<b>Base clientes piloto sem dono</b>", "09/10* dono"),
        ("As Is x To Be e transição", "DOC", "30/10", "Não iniciado", "Entregas 1–3", "21/10 insumos"),
        ("Capacidade, treinamento, sustentação", "DOC", "30/10", "Em atenção", "<b>Governança só em 06/11</b>", "23/10* prévia"),
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


# Estrutura executiva --------------------------------------------------------
TITULO = ("Piloto de jan/27 mantido, mas a Política Comercial (13/10) pode sair parcial. "
          "Precisamos de 1 escalonamento e 3 decisões até 16/10.")

ACAO = {
    "decisoes": "Quatro definições até 16/10 protegem as entregas de outubro",
    "pilares": "3 de 7 pilares em atenção, explicados por só duas causas: a base VI vencida e a base de "
               "clientes do piloto sem dono",
    "criterios": "Cada entrega tem um critério objetivo de conclusão, contra o qual reportaremos avanço",
    "avancos": "As definições da semana tiram a nova ferramenta do caminho crítico do piloto",
    "pendencias": "Uma dependência vencida desde 23/09 concentra o principal risco do projeto",
    "protocolo": "O protocolo do piloto passa a ser entrega própria; 1 de 8 componentes em andamento",
    "anexo": "Atividades por frente, com dono, status e próximo marco",
}

# Visao por pilar: uma linha por pilar
# (pilar, entrega final, prazo, status, bloqueio, proximo marco, semana da entrega na linha do tempo)
SEMANAS = ["28/09", "05/10", "12/10", "19/10", "26/10", "02/11", "09/11", "16/11", "23/11", "30/11"]
PILARES = [
    ("1. Política Comercial", "Tabela, camadas e parâmetros", "13/10", "Em atenção",
     "<b>Base VI (Gisele) vencida desde 23/09</b>", "09/10 · reunião ou escalonamento", 2),
    ("2. Economia dos Canais", "DRE do distribuidor e economia por canal", "14/10", "Em andamento",
     "Nenhum", "06–07/10 · visita ao distribuidor GO", 2),
    ("3. Banda e RTP", "Banda por SKU, RTP on-invoice e cenários", "21/10", "Em andamento",
     "Decisão TI + IC em 16/10 (folga de 5 dias)", "07/10 · pesquisa de preços validada", 3),
    ("4. Governança", "Macrofluxo, RACI, apuração e guardrails", "06/11", "Em andamento",
     "Critério da Gisele (09/10) e TI + IC (16/10)", "09/10 · critério de apuração", 5),
    ("5. Business Case <i>ex ante</i>", "Investimento, incrementalidade, ROI e break-even", "30/10", "Em atenção",
     "<b>Base de clientes do piloto sem dono</b>; governança só em 06/11", "09/10* · dono da base", 4),
    ("5.1 Piloto", "Protocolo (v0 30/10*) e campo", "30/11", "Em atenção",
     "<b>Mesma base de clientes</b> (baseline)", "30/10* · protocolo v0", 9),
    ("6. Implementação", "Treinamento e rollout Brasil", "jan–ago/27", "Não iniciado",
     "Política piloto validada", "30/10 · data do treinamento", None),
]
DECISOES_SEMANA = {1: "09/10", 2: "16/10"}


# ---------------------------------------------------------------- render
def st(status, size=11.5):
    c, bg, _ = STATUS[status]
    return (f'<span style="display:inline-block;padding:3px 10px;border-radius:999px;background:{bg};'
            f'color:{c};font-family:{FONT};font-size:{size}px;font-weight:600;line-height:1.4;white-space:nowrap">'
            f'{status}</span>')


def tbl(inner):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{inner}</table>'


def box(kicker, acao, body, kind="branco", nota=""):
    bg, bd, tc = BOX[kind]
    nt = (f'<p style="margin:12px 0 0 0;font-family:{FONT};font-size:11px;line-height:1.5;color:{MUTE}">'
          f'{nota}</p>') if nota else ""
    return (f'<tr><td style="padding:0 32px 18px 32px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{bg};border:1px solid {bd};border-radius:14px;border-collapse:separate">'
            f'<tr><td style="padding:20px 22px">'
            f'<p style="margin:0 0 4px 0;font-family:{FONT};font-size:10.5px;font-weight:700;letter-spacing:1.6px;'
            f'text-transform:uppercase;color:{tc}">{kicker}</p>'
            f'<p style="margin:0 0 14px 0;font-family:{FONT};font-size:16px;font-weight:700;line-height:1.35;'
            f'color:{NAVY}">{acao}</p>{body}{nt}</td></tr></table></td></tr>')


def small(t, color=SUB):
    return f'<span style="font-size:11.5px;color:{color}">{t}</span>'


def head(cells, widths):
    return "<tr>" + "".join(
        f'<td width="{w}" style="padding:0 8px 6px 0;border-bottom:1px solid #CBD5E1;font-family:{FONT};'
        f'font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:{SUB}">{c}</td>'
        for c, w in zip(cells, widths)) + "</tr>"


def row(cells, widths, size=12.5, pad="9px 8px 9px 0", first=False, aligns=None):
    b = "" if first else f"border-top:1px solid {LINE};"
    aligns = aligns or ["left"] * len(cells)
    return "<tr>" + "".join(
        f'<td valign="top" align="{a}" width="{w}" style="padding:{pad};{b}font-family:{FONT};font-size:{size}px;'
        f'line-height:1.45;color:{INK}">{c}</td>' for c, w, a in zip(cells, widths, aligns)) + "</tr>"


def timeline():
    lw, cw = 168, 50
    hdr = (f'<td width="{lw}" style="padding:0 0 6px 0;border-bottom:1px solid #CBD5E1"></td>' + "".join(
        f'<td width="{cw}" align="center" style="padding:0 0 6px 0;border-bottom:1px solid #CBD5E1;font-family:{FONT};'
        f'font-size:9.5px;font-weight:700;color:{BLUE if i == 0 else SUB}">{"Hoje" if i == 0 else s}</td>'
        for i, s in enumerate(SEMANAS)))
    out = [f"<tr>{hdr}</tr>"]

    def cell(inner, i):
        hoje = f"border-left:2px solid {BLUE};" if i == 0 else ""
        return (f'<td width="{cw}" align="center" valign="middle" style="padding:7px 0;{hoje}'
                f'border-bottom:1px solid {LINE}">{inner}</td>')

    for pilar, _, prazo, s, _, _, due in PILARES:
        cor, tint, _ = STATUS[s]
        barc = tint if s in ("Em atenção", "Atrasado") else "#E5E7EB"
        bar = f'<div style="height:8px;background:{barc};font-size:0">&nbsp;</div>'
        cells = []
        for i in range(len(SEMANAS)):
            if due is None:
                inner = (f'<span style="font-family:{FONT};font-size:9.5px;font-weight:700;color:{SUB}">2027 &rarr;</span>'
                         if i == len(SEMANAS) - 1 else "&nbsp;")
            elif i < due:
                inner = bar
            elif i == due:
                inner = (f'<span style="font-family:{FONT};font-size:14px;color:{cor}">&#9670;</span><br>'
                         f'<span style="font-family:{FONT};font-size:9.5px;font-weight:700;color:{cor}">{prazo}</span>')
            else:
                inner = "&nbsp;"
            cells.append(cell(inner, i))
        out.append(f'<tr><td width="{lw}" valign="middle" style="padding:7px 8px 7px 0;border-bottom:1px solid {LINE};'
                   f'font-family:{FONT};font-size:12px;font-weight:600;color:{INK}">{pilar}</td>{"".join(cells)}</tr>')
    red = STATUS["Atrasado"][0]
    cells = "".join(cell(
        (f'<span style="font-family:{FONT};font-size:12px;color:{red}">&#9650;</span><br>'
         f'<span style="font-family:{FONT};font-size:9.5px;font-weight:700;color:{red}">{DECISOES_SEMANA[i]}</span>')
        if i in DECISOES_SEMANA else "&nbsp;", i) for i in range(len(SEMANAS)))
    out.append(f'<tr><td width="{lw}" valign="middle" style="padding:7px 8px 7px 0;border-bottom:1px solid {LINE};'
               f'font-family:{FONT};font-size:12px;font-weight:600;color:{red}">Decisões necessárias</td>{cells}</tr>')
    leg = (f'<p style="margin:8px 0 0 0;font-family:{FONT};font-size:10.5px;color:{SUB}">&#9670; data da entrega, '
           f'na cor do status &nbsp;·&nbsp; <span style="color:{red}">&#9650;</span> decisão / escalonamento</p>')
    return tbl("".join(out)) + leg


def build():
    o = []
    # cabecalho DOC
    o.append(
        f'<tr><td style="background:{NAVY};padding:26px 32px;border-radius:16px 16px 0 0">' + tbl(
            f'<tr><td valign="bottom" style="font-family:{FONT};font-size:10.5px;letter-spacing:2.4px;color:#94A3B8">'
            f'<span style="font-size:15px;letter-spacing:0;color:#FFFFFF;font-weight:700">DOC</span>'
            f'<span style="font-size:15px;letter-spacing:0;color:#94A3B8"> Consulting</span><br><br>'
            f'STATUS REPORT SEMANAL</td>'
            f'<td align="right" valign="top" style="font-family:{FONT};color:#FFFFFF">'
            f'<div style="font-size:16px;font-weight:700">{META["titulo"]}</div>'
            f'<div style="font-size:16px;font-weight:700;margin-top:6px">{META["numero"]}</div>'
            f'<div style="font-size:11.5px;color:#CBD5E1;margin-top:6px">{META["data"]} · {META["versao"]}</div>'
            f'</td></tr>') + '</td></tr>')

    # titulo-resposta + tres numeros
    c, cbg, _ = STATUS[META["saude"]]
    n = {k: sum(1 for p in PILARES if p[3] == k) for k in STATUS}
    kpis = [
        ("Saúde do projeto", f'<span style="font-size:20px;font-weight:700;color:{c}">{META["saude"]}</span>',
         "piloto de jan/27 mantido"),
        ("Pilares", f'<span style="font-size:22px;font-weight:700;color:{c}">{n["Em atenção"]}</span>'
                    f'<span style="font-size:13px;color:{SUB}"> de {len(PILARES)} em atenção</span>',
         f'{n["Em andamento"]} em andamento · {n["Não iniciado"]} não iniciado'),
        ("Ações necessárias", f'<span style="font-size:22px;font-weight:700;color:{STATUS["Atrasado"][0]}">'
                              f'{len(DECISOES)}</span><span style="font-size:13px;color:{SUB}"> até 16/10</span>',
         "1 escalonamento · 3 decisões"),
    ]
    cells = "".join(
        f'<td width="33%" valign="top" style="padding:12px {0 if i == 2 else 14}px 0 {0 if i == 0 else 14}px;'
        f'{"border-left:1px solid #FDE68A;" if i else ""}font-family:{FONT}">'
        f'<div style="font-size:10px;font-weight:700;letter-spacing:1.2px;color:{c}">{k.upper()}</div>'
        f'<div style="margin:6px 0 2px 0;line-height:1.2">{v}</div>'
        f'<div style="font-size:11.5px;color:{SUB}">{s_}</div></td>' for i, (k, v, s_) in enumerate(kpis))
    o.append(
        f'<tr><td style="padding:24px 32px 18px 32px">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="background:{cbg};border-radius:14px;border-collapse:separate"><tr><td style="padding:20px 22px">'
        f'<p style="margin:0;font-family:{FONT};font-size:20px;font-weight:700;line-height:1.35;color:{NAVY}">{TITULO}</p>'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;'
        f'border-top:1px solid #FDE68A"><tr>{cells}</tr></table>'
        f'</td></tr></table></td></tr>')

    # 1 decisoes
    ws = [440, 150, 56]
    rws = "".join(row([
        (f'<span style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;'
         f'color:{STATUS["Atrasado"][0] if t == "Escalonamento" else SUB}">{t}</span><br>'
         f'<b>{q}</b><br>{small(why)}'), quem, f"<b>{ate}</b>"], ws, pad="10px 8px 10px 0", first=i == 0,
        aligns=["left", "left", "right"]) for i, (t, q, why, quem, ate) in enumerate(DECISOES))
    o.append(box("1 · Decisões necessárias / Escalonamentos", ACAO["decisoes"],
                 tbl(head(["O que precisamos", "De quem", "Até"], ws) + rws), "vermelho"))

    # 2 visao por pilar
    ws = [150, 64, 100, 200, 132]
    rws = "".join(row([f"<b>{p}</b><br>{small(e)}", pz, st(s, 10.5), blq, mk], ws, size=12, first=i == 0)
                  for i, (p, e, pz, s, blq, mk, _) in enumerate(PILARES))
    o.append(box("2 · Visão por pilar", ACAO["pilares"],
                 timeline() + '<div style="height:18px;font-size:0">&nbsp;</div>'
                 + tbl(head(["Pilar / entrega", "Prazo", "Status", "Bloqueio", "Próximo marco"], ws) + rws)))

    # 3 criterios de conclusao
    rws = "".join(row([f'<b style="color:{NAVY}">{nome}</b> <span style="color:{SUB}">· {prazo}</span><br>'
                       f'{small("Concluída quando: " + crit, INK)}'], [None], size=12.5, pad="9px 0", first=i == 0)
                  for i, (nome, prazo, _, _, crit) in enumerate(ENTREGAS))
    o.append(box("3 · Critério de conclusão por entrega", ACAO["criterios"], tbl(rws)))

    # 4 avancos
    rws = "".join(row([f"<b>{r}</b><br>{small(i)}"], [None], pad="8px 0", first=k == 0)
                  for k, (r, i) in enumerate(AVANCOS))
    o.append(box("4 · Avanços do ciclo", ACAO["avancos"], tbl(rws), "verde",
                 f"Em curso, sem resultado ainda: {EM_CURSO}"))

    # 5 pendencias
    body = ""
    for i, x in enumerate(CRITICAS):
        b = f"border-top:1px solid {LINE};" if i else ""
        body += tbl(
            f'<tr><td style="padding:12px 0 4px 0;{b}font-family:{FONT};font-size:13.5px;color:{INK}"><b>{x["o_que"]}</b></td>'
            f'<td align="right" style="padding:12px 0 4px 0;{b}font-family:{FONT}">{st(x["status"])}</td></tr>'
            f'<tr><td colspan="2" style="padding:0 0 12px 0;font-family:{FONT};font-size:12.5px;line-height:1.6;color:{INK}">'
            f'{small("De quem")} {x["quem"]} &nbsp;·&nbsp; {small("Prazo")} {x["prazo"]} &nbsp;·&nbsp; '
            f'{small("Impacta")} {x["entrega"]}<br>{small("Impacto")} {x["impacto"]}<br>'
            f'{small("Próxima ação")} <b>{x["acao"]}</b></td></tr>')
    ws = [270, 150, 64, 160]
    body += (f'<p style="margin:14px 0 6px 0;font-family:{FONT};font-size:10.5px;font-weight:700;letter-spacing:1px;'
             f'color:{SUB}">EM DIA (PRAZO ORIGINAL MANTIDO)</p>'
             + tbl(head(["Pendência", "De quem", "Prazo", "Impacta"], ws)
                   + "".join(row(list(r), ws, size=12, pad="7px 8px 7px 0", first=i == 0) for i, r in enumerate(EM_DIA))))
    o.append(box("5 · Pendências e dependências", ACAO["pendencias"], body, "cinza"))

    # 6 protocolo
    nomes = "".join(f'<td width="12.5%" align="center" valign="bottom" style="padding:0 3px 8px 3px;font-family:{FONT};'
                    f'font-size:11px;line-height:1.3;font-weight:600;color:{INK}">{c_}</td>' for c_, _ in PROTOCOLO)
    tags = "".join(f'<td align="center" style="padding:0 3px">{st(s, 9.5)}</td>' for _, s in PROTOCOLO)
    o.append(box("6 · Protocolo do piloto · evolução semanal", ACAO["protocolo"],
                 tbl(f"<tr>{nomes}</tr><tr>{tags}</tr>"), nota=PROTOCOLO_NOTA))

    # anexo
    ws = [186, 66, 78, 100, 150, 100]
    rws = []
    for frente, ativs in CRONOGRAMA:
        rws.append(f'<tr><td colspan="6" style="padding:12px 0 4px 0;font-family:{FONT};font-size:12px;'
                   f'font-weight:700;color:{NAVY}">{frente}</td></tr>')
        rws += [row([a, ow, pz, st(s, 10), dep, mk], ws, size=11.5, pad="6px 8px 6px 0")
                for a, ow, pz, s, dep, mk in ativs]
    leg = " · ".join(f"<b>{k}</b>: {v[2][0].lower() + v[2][1:].rstrip('.')}" for k, v in STATUS.items())
    o.append(box("Anexo · Cronograma por frente", ACAO["anexo"],
                 tbl(head(["Atividade", "Owner", "Prazo", "Status", "Dependência / bloqueio", "Próximo marco"], ws)
                     + "".join(rws)), "cinza",
                 f"{leg}. A entrega herda o pior status das suas dependências. "
                 f"* Data proposta pela DOC, a confirmar com a PremieRpet."))

    o.append(f'<tr><td style="padding:8px 32px 28px 32px">' + tbl(
        f'<tr><td style="border-top:1px solid {LINE};padding-top:14px;font-family:{FONT};font-size:10.5px;'
        f'line-height:1.6;color:{MUTE};text-align:center">DOC Consulting | Status report semanal<br>'
        f'© 2026 DOC Consulting. Todos os direitos reservados.</td></tr>') + '</td></tr>')

    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Status Report #2 – PremieRpet</title></head>'
        '<body style="margin:0;padding:0;background:#F1F5F9">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F1F5F9">'
        '<tr><td align="center" style="padding:24px 8px">'
        f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" '
        f'style="width:{W}px;max-width:100%;background:#FFFFFF;border-radius:16px;border-collapse:separate">'
        + "".join(o) + '</table></td></tr></table></body></html>')


if __name__ == "__main__":
    dst = Path(__file__).with_name("status-report-02-premierpet.html")
    dst.write_text(build(), encoding="utf-8")
    print(f"ok -> {dst}")

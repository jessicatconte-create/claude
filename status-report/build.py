"""Status Report semanal PremieRpet | Projeto Politica Comercial.

Gera dois HTMLs compativeis com e-mail (Outlook/Gmail): tabelas e estilos
inline, sem CSS externo.
  - status-report-02-premierpet.html        corpo executivo
  - status-report-02-premierpet-anexo.html  cronograma por atividade

Estrutura executiva: o titulo e a resposta da semana; cada secao abre com um
titulo-acao; visao por pilar no corpo, detalhe por atividade so no anexo.
Visual no sistema DOC: tokens da marca, Geist, escala 11 / 13 / 16 / 24,
respiros em multiplos de 8 (24 dentro do bloco, 32 entre blocos), cor so
para status.

Todo o conteudo fica nos dados abaixo; para a proxima semana, atualize os
dados e rode:  python3 build.py
"""
from pathlib import Path

# ---------------------------------------------------------------- sistema DOC
BG = "#F5F5F3"; BLOCO = "#FFFFFF"; APOIO = "#F2F3F4"
INK = "#1E2125"; SUB = "#5C6066"; ROTULO = "#8D9092"
LINHA = "#E7E7E5"; LINHA2 = "#D4D4D2"
DESTAQUE = "#1565C0"; NAVY = "#0E1A5C"; CLARO = "#8FC9FF"
FONT = "Geist, Arial, Helvetica, sans-serif"
T_ROT, T_CORPO, T_SECAO, T_TITULO = 11, 13, 16, 24
W = 760
PAD = 24          # respiro interno do bloco
GAP = 32          # espaco entre blocos
MARGEM = 32       # margem lateral da peca
CONTEUDO = W - 2 * MARGEM - 2 * PAD   # 648

# Criterios objetivos de status (mesma escala para atividade e entrega).
# Cor so onde ha significado: atencao, atraso e conclusao.
STATUS = {
    "Concluído":    ("#166534", "#E8F5EC", "critério de conclusão atendido e validado pela PremieRpet"),
    "Em andamento": (INK,       APOIO,     "iniciado, dependências em dia, prazo preservado"),
    "Em atenção":   ("#92400E", "#FEF3C7", "prazo preservado, mas com dependência pendente, sem dono/data ou fora de sequência"),
    "Atrasado":     ("#B42318", "#FDECEA", "prazo vencido, ou dependência vencida que já compromete a data"),
    "Não iniciado": (SUB,       BLOCO,     "início previsto para data futura"),
}
VERMELHO = STATUS["Atrasado"][0]; AMBAR = STATUS["Em atenção"][0]

META = {
    "numero": "#2", "data": "02/10/2026", "versao": "versão revisada",
    "titulo": "PremieRpet | Projeto Política Comercial",
    "saude": "Em atenção",
}

TITULO = ("Piloto de jan/27 mantido, mas a Política Comercial (13/10) pode sair parcial. "
          "Precisamos de 1 escalonamento e 3 decisões até 16/10.")

ACAO = {
    "decisoes": "Quatro definições até 16/10 protegem as entregas de outubro",
    "pilares": "3 de 7 pilares em atenção, explicados por só duas causas: a base VI vencida e a base de "
               "clientes do piloto sem dono",
    "avancos": "As definições da semana tiram a nova ferramenta do caminho crítico do piloto",
    "pendencias": "Uma dependência vencida desde 23/09 concentra o principal risco do projeto",
    "protocolo": "O protocolo do piloto passa a ser entrega própria; 1 de 8 componentes em andamento",
}

# Decisoes necessarias / escalonamentos: (tipo, o que, se nao acontecer, de quem, ate)
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

# Visao por pilar: (pilar, entrega, prazo, status, bloqueio, proximo marco,
#                   semana da entrega na linha do tempo, criterio de conclusao)
SEMANAS = ["28/09", "05/10", "12/10", "19/10", "26/10", "02/11", "09/11", "16/11", "23/11", "30/11"]
PILARES = [
    ("1. Política Comercial", "Tabela, camadas e parâmetros", "13/10", "Em atenção",
     "<b>Base VI (Gisele) vencida desde 23/09</b>", "09/10 · reunião ou escalonamento", 2,
     "tabela e camadas por canal com pocket price; metas, percentuais e elegibilidade por alavanca; "
     "simulação do investimento por faixa de atingimento; validação com RGM/Comercial."),
    ("2. Economia dos Canais", "DRE do distribuidor e economia por canal", "14/10", "Em andamento",
     "Nenhum", "06–07/10 · visita ao distribuidor GO", 2,
     "DRE do distribuidor GO validada com dados de campo; economia de cada canal, modelo atual x proposto."),
    ("3. Banda e RTP", "Banda por SKU, RTP on-invoice e cenários", "21/10", "Em andamento",
     "Decisão TI + IC em 16/10 (folga de 5 dias)", "07/10 · pesquisa de preços validada", 3,
     "banda de preço por SKU/canal; mecânica da RTP on-invoice (SKU → pedido); cenários de impacto em "
     "preço, volume e margem."),
    ("4. Governança", "Macrofluxo, RACI, apuração e guardrails", "06/11", "Em andamento",
     "Critério da Gisele (09/10) e TI + IC (16/10)", "09/10 · critério de apuração", 5,
     "macrofluxo de apuração, pagamento e exceções com RACI; critério e calendário de apuração; "
     "guardrails; validação de Trade, RGM, IC e TI."),
    ("5. Business Case <i>ex ante</i>", "Investimento, incrementalidade, ROI e break-even", "30/10", "Em atenção",
     "<b>Base de clientes do piloto sem dono</b>; governança só em 06/11", "09/10* · dono da base", 4,
     "investimento previsto; impacto em volume, mix e margem; incrementalidade necessária; ROI esperado e "
     "break-even em três cenários; premissas e sensibilidades. <b>A decisão de implementar o piloto é tomada "
     "com ele aprovado</b>; jan–abr/27 mede só o resultado realizado."),
    ("5.1 Piloto", "Protocolo (v0 30/10*) e campo", "30/11", "Em atenção",
     "<b>Mesma base de clientes</b> (baseline)", "30/10* · protocolo v0", 9,
     "os oito componentes do protocolo aprovados e os dados de campo validados."),
    ("6. Implementação", "Treinamento e rollout Brasil", "jan–ago/27", "Não iniciado",
     "Política piloto validada", "30/10 · data do treinamento", None,
     "equipe comercial do piloto treinada antes de jan/27*; rollout decidido pela regra do protocolo."),
]
DECISOES_SEMANA = (1, 2)  # semanas com decisoes (09/10 e 16/10)

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
# Dependencias em dia (prazo original = atual): ficam no anexo
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

# Anexo: cronograma por frente (Atividade | Owner | Prazo | Status | Dependencia | Proximo marco)
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

NOTA_DATAS = "* Data proposta pela DOC, a confirmar com a PremieRpet."


# ---------------------------------------------------------------- componentes
def txt(t, size=T_CORPO, color=INK, weight=400, extra=""):
    return (f'<span style="font-family:{FONT};font-size:{size}px;line-height:1.5;color:{color};'
            f'font-weight:{weight};{extra}">{t}</span>')


def rot(t, color=ROTULO):
    """Rotulo curto em caixa alta (nunca texto corrido)."""
    return txt(t, T_ROT, color, 600, "letter-spacing:1px;text-transform:uppercase")


def st(status):
    c, bg, _ = STATUS[status]
    borda = LINHA2 if bg == BLOCO else bg
    return (f'<span style="display:inline-block;padding:2px 8px;border:1px solid {borda};border-radius:999px;'
            f'background:{bg};color:{c};font-family:{FONT};font-size:{T_ROT}px;font-weight:600;line-height:1.5;'
            f'white-space:nowrap">{status}</span>')


def tbl(inner, extra=""):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="{extra}">{inner}</table>'


def bloco(kicker, acao, body, nota="", ultimo=False):
    nt = f'<p style="margin:16px 0 0 0">{txt(nota, T_ROT, SUB)}</p>' if nota else ""
    return (f'<tr><td style="padding:0 {MARGEM}px {0 if ultimo else GAP}px {MARGEM}px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{BLOCO};border:1px solid {LINHA2};border-radius:16px;border-collapse:separate">'
            f'<tr><td style="padding:{PAD}px">'
            f'<p style="margin:0 0 8px 0">{rot(kicker, DESTAQUE)}</p>'
            f'<p style="margin:0 0 16px 0;font-family:{FONT};font-size:{T_SECAO}px;font-weight:600;line-height:1.4;'
            f'color:{NAVY}">{acao}</p>{body}{nt}</td></tr></table></td></tr>')


def head(cells, widths, aligns=None):
    aligns = aligns or ["left"] * len(cells)
    return "<tr>" + "".join(
        f'<td width="{w}" align="{a}" style="padding:0 8px 8px 0;border-bottom:1px solid {LINHA2}">{rot(c)}</td>'
        for c, w, a in zip(cells, widths, aligns)) + "</tr>"


def row(cells, widths, first=False, aligns=None, pad="16px 8px 16px 0"):
    b = "" if first else f"border-top:1px solid {LINHA};"
    aligns = aligns or ["left"] * len(cells)
    return "<tr>" + "".join(
        f'<td valign="top" align="{a}" width="{w}" style="padding:{pad};{b}font-family:{FONT};'
        f'font-size:{T_CORPO}px;line-height:1.5;color:{INK}">{c}</td>'
        for c, w, a in zip(cells, widths, aligns)) + "</tr>"


def cabecalho(subtitulo):
    return (
        f'<tr><td style="padding:0 {MARGEM}px {GAP}px {MARGEM}px">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="background:{NAVY};border-radius:16px;border-collapse:separate"><tr>'
        f'<td valign="middle" style="padding:{PAD}px">'
        f'{txt("DOC", T_SECAO, "#FFFFFF", 700)}{txt(" Consulting", T_SECAO, CLARO)}<br>'
        f'{rot(subtitulo, CLARO)}</td>'
        f'<td align="right" valign="middle" style="padding:{PAD}px">'
        f'{txt(META["titulo"], T_SECAO, "#FFFFFF", 600)}<br>'
        f'{txt(META["numero"] + " · " + META["data"] + " · " + META["versao"], T_ROT, CLARO)}'
        f'</td></tr></table></td></tr>')


def rodape():
    return (f'<tr><td align="center" style="padding:{GAP}px {MARGEM}px 0 {MARGEM}px">'
            f'{txt("DOC Consulting | Status report semanal · © 2026 DOC Consulting. Todos os direitos reservados.", T_ROT, SUB)}'
            f'</td></tr>')


def pagina(titulo_html, linhas):
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600;700&display=swap" rel="stylesheet">'
        f'<title>{titulo_html}</title></head>'
        f'<body style="margin:0;padding:0;background:{BG}">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{BG}">'
        f'<tr><td align="center" style="padding:{GAP}px 8px">'
        f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" style="width:{W}px;max-width:100%">'
        + "".join(linhas) + '</table></td></tr></table></body></html>')


def legenda_status():
    return " · ".join(f"<b>{k}</b>: {v[2]}" for k, v in STATUS.items()) + \
        ". A entrega herda o pior status das suas dependências."


# ---------------------------------------------------------------- secoes
def topo():
    c = STATUS[META["saude"]][0]
    n = {k: sum(1 for p in PILARES if p[3] == k) for k in STATUS}
    kpis = [
        ("Saúde do projeto", txt(META["saude"], T_SECAO, c, 700), "piloto de jan/27 mantido"),
        ("Pilares", txt(f'{n["Em atenção"]} de {len(PILARES)} em atenção', T_SECAO, c, 700),
         f'{n["Em andamento"]} em andamento · {n["Não iniciado"]} não iniciado'),
        ("Ações necessárias", txt(f"{len(DECISOES)} até 16/10", T_SECAO, VERMELHO, 700),
         "1 escalonamento · 3 decisões"),
    ]
    cells = "".join(
        f'<td width="33%" valign="top" style="padding:16px {0 if i == 2 else 16}px 0 {0 if i == 0 else 16}px;'
        f'{"border-left:1px solid " + LINHA + ";" if i else ""}">'
        f'{rot(k)}<br>{v}<br>{txt(s, T_ROT, SUB)}</td>' for i, (k, v, s) in enumerate(kpis))
    return (f'<tr><td style="padding:0 {MARGEM}px {GAP}px {MARGEM}px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{BLOCO};border:1px solid {LINHA2};border-radius:16px;border-collapse:separate">'
            f'<tr><td style="padding:{PAD}px">'
            f'<p style="margin:0;font-family:{FONT};font-size:{T_TITULO}px;font-weight:700;line-height:1.3;'
            f'letter-spacing:-0.02em;color:{NAVY}">{TITULO}</p>'
            + tbl(f"<tr>{cells}</tr>", f"margin-top:16px;border-top:1px solid {LINHA}") +
            '</td></tr></table></td></tr>')


def decisoes():
    ws = [424, 160, 64]
    rws = "".join(row([
        f'{rot(t, VERMELHO if t == "Escalonamento" else ROTULO)}<br><b>{q}</b><br>{txt(why, T_CORPO, SUB)}',
        quem, f"<b>{ate}</b>"], ws, first=i == 0, aligns=["left", "left", "right"])
        for i, (t, q, why, quem, ate) in enumerate(DECISOES))
    return bloco("1 · Decisões necessárias / Escalonamentos", ACAO["decisoes"],
                 tbl(head(["O que precisamos", "De quem", "Até"], ws, ["left", "left", "right"]) + rws))


def timeline():
    lw, cw = 168, 48
    hdr = (f'<td width="{lw}" style="padding:0 0 8px 0;border-bottom:1px solid {LINHA2}"></td>' + "".join(
        f'<td width="{cw}" align="center" style="padding:0 0 8px 0;border-bottom:1px solid {LINHA2}">'
        f'{txt("Hoje" if i == 0 else s, T_ROT, DESTAQUE if i == 0 else ROTULO, 600)}</td>'
        for i, s in enumerate(SEMANAS)))
    out = [f"<tr>{hdr}</tr>"]

    def cell(inner, i):
        hoje = f"border-left:2px solid {DESTAQUE};" if i == 0 else ""
        return (f'<td width="{cw}" align="center" valign="middle" style="padding:8px 0;{hoje}'
                f'border-bottom:1px solid {LINHA}">{inner}</td>')

    def losango(cor):
        return f'<span style="font-family:Arial,sans-serif;font-size:{T_CORPO}px;line-height:1;color:{cor}">&#9670;</span>'

    for pilar, _, _, s, _, _, due, _ in PILARES:
        alerta = s in ("Em atenção", "Atrasado")
        cor = STATUS[s][0] if alerta else (ROTULO if s == "Não iniciado" else NAVY)
        barra = (f'<div style="height:8px;background:{"#FDE7C2" if alerta else LINHA};font-size:0;'
                 f'line-height:0">&nbsp;</div>')
        cells = []
        for i in range(len(SEMANAS)):
            if due is None:
                inner = txt("2027 →", T_ROT, SUB, 600) if i == len(SEMANAS) - 1 else "&nbsp;"
            else:
                inner = barra if i < due else (losango(cor) if i == due else "&nbsp;")
            cells.append(cell(inner, i))
        out.append(f'<tr><td width="{lw}" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {LINHA}">'
                   f'{txt(pilar, T_CORPO, INK, 600)}</td>{"".join(cells)}</tr>')
    tri = f'<span style="font-family:Arial,sans-serif;font-size:{T_ROT}px;line-height:1;color:{VERMELHO}">&#9650;</span>'
    out.append(f'<tr><td width="{lw}" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {LINHA}">'
               f'{txt("Decisões necessárias", T_CORPO, VERMELHO, 600)}</td>'
               + "".join(cell(tri if i in DECISOES_SEMANA else "&nbsp;", i) for i in range(len(SEMANAS))) + "</tr>")
    leg = (f'<p style="margin:8px 0 0 0">{txt("&#9670; entrega (cor do status: navy no prazo, âmbar em atenção, cinza não iniciada) · ", T_ROT, SUB)}'
           f'{txt("&#9650; decisão / escalonamento (09/10 e 16/10)", T_ROT, VERMELHO)}</p>')
    return tbl("".join(out)) + leg


def pilares():
    ws = [192, 88, 104, 264]
    rws = ""
    for i, (p, e, pz, s, blq, mk, _, crit) in enumerate(PILARES):
        b = "" if i == 0 else f"border-top:1px solid {LINHA};"
        rws += "<tr>" + "".join(
            f'<td valign="top" width="{w}" style="padding:16px 8px 8px 0;{b}">{c}</td>' for c, w in zip([
                f'{txt(p, T_CORPO, INK, 600)}<br>{txt(e, T_ROT, SUB)}',
                txt(pz, extra="white-space:nowrap"), st(s),
                f'{txt(blq)}<br>{txt("Próximo: " + mk, T_ROT, SUB)}'], ws)) + "</tr>"
        rws += (f'<tr><td colspan="4" style="padding:0 0 16px 0">'
                f'{txt("<b>Concluída quando:</b> " + crit, T_CORPO, SUB)}</td></tr>')
    return bloco("2 · Visão por pilar", ACAO["pilares"],
                 timeline() + f'<div style="height:{GAP}px;font-size:0;line-height:0">&nbsp;</div>'
                 + tbl(head(["Pilar / entrega", "Prazo", "Status", "Bloqueio e próximo marco"], ws) + rws))


def avancos():
    rws = "".join(row([f"<b>{r}</b><br>{txt(i, T_CORPO, SUB)}"], [None], first=k == 0, pad="8px 0")
                  for k, (r, i) in enumerate(AVANCOS))
    return bloco("3 · Avanços do ciclo", ACAO["avancos"], tbl(rws), f"Em curso, sem resultado ainda: {EM_CURSO}")


def pendencias():
    body = ""
    for i, x in enumerate(CRITICAS):
        b = "" if i == 0 else f"border-top:1px solid {LINHA};"
        campos = (f'{rot("De quem")} {txt(x["quem"])} &nbsp;·&nbsp; {rot("Prazo")} {txt(x["prazo"])} &nbsp;·&nbsp; '
                  f'{rot("Impacta")} {txt(x["entrega"])}<br>'
                  f'{rot("Impacto")} {txt(x["impacto"])}<br>'
                  f'{rot("Próxima ação")} {txt(x["acao"], weight=600)}')
        body += tbl(
            f'<tr><td style="padding:16px 0 8px 0;{b}">{txt(x["o_que"], T_CORPO, INK, 700)}</td>'
            f'<td align="right" style="padding:16px 0 8px 0;{b}">{st(x["status"])}</td></tr>'
            f'<tr><td colspan="2" style="padding:0 0 16px 0;line-height:1.9">{campos}</td></tr>')
    return bloco("4 · Pendências e dependências", ACAO["pendencias"], body,
                 f"As demais {len(EM_DIA)} dependências estão em dia, com prazo original mantido; "
                 f"detalhe no anexo.")


def protocolo():
    linhas = ""
    for k in range(0, len(PROTOCOLO), 4):
        grupo = PROTOCOLO[k:k + 4]
        b = "" if k == 0 else f"border-top:1px solid {LINHA};"
        linhas += "<tr>" + "".join(
            f'<td width="25%" valign="top" style="padding:16px 8px 16px 0;{b}">'
            f'{txt(c, T_CORPO, INK, 600)}<br><span style="display:inline-block;margin-top:8px">{st(s)}</span></td>'
            for c, s in grupo) + "</tr>"
    return bloco("5 · Protocolo do piloto · evolução semanal", ACAO["protocolo"], tbl(linhas), PROTOCOLO_NOTA,
                 ultimo=True)


def notas():
    return (f'<tr><td style="padding:{GAP}px {MARGEM}px 0 {MARGEM}px">'
            f'<p style="margin:0">{txt("<b>Critérios de status.</b> " + legenda_status(), T_ROT, SUB)}</p>'
            f'<p style="margin:8px 0 0 0">{txt(NOTA_DATAS + " Anexo: cronograma por atividade e dependências em dia "
                                              "(arquivo separado).", T_ROT, SUB)}</p></td></tr>')


def build():
    return pagina(f"Status Report {META['numero']} – PremieRpet",
                  [cabecalho("Status report semanal"), topo(), decisoes(), pilares(), avancos(),
                   pendencias(), protocolo(), notas(), rodape()])


# ---------------------------------------------------------------- anexo
def build_anexo():
    ws = [184, 72, 80, 104, 120, 88]
    rws = []
    for frente, ativs in CRONOGRAMA:
        rws.append(f'<tr><td colspan="6" style="padding:16px 0 8px 0">{txt(frente, T_CORPO, NAVY, 700)}</td></tr>')
        for j, (a, ow, pz, s, dep, mk) in enumerate(ativs):
            b = f"border-top:1px solid {LINHA};"
            rws.append("<tr>" + "".join(
                f'<td valign="top" width="{w}" style="padding:8px 8px 8px 0;{b}">{c}</td>'
                for c, w in zip([txt(a, T_ROT, INK, 600), txt(ow, T_ROT), txt(pz, T_ROT), st(s),
                                 txt(dep, T_ROT), txt(mk, T_ROT)], ws)) + "</tr>")
    crono = bloco("Anexo A · Cronograma por frente", "Atividades por frente, com dono, status e próximo marco",
                  tbl(head(["Atividade", "Owner", "Prazo", "Status", "Dependência", "Próximo marco"], ws)
                      + "".join(rws)))
    ws2 = [272, 168, 72, 136]
    em_dia = bloco("Anexo B · Dependências em dia", "Prazo original mantido; nenhuma ação adicional necessária",
                   tbl(head(["Dependência", "De quem", "Prazo", "Impacta"], ws2)
                       + "".join(row(list(r), ws2, first=i == 0, pad="8px 8px 8px 0") for i, r in enumerate(EM_DIA))),
                   ultimo=True)
    leg = (f'<tr><td style="padding:{GAP}px {MARGEM}px 0 {MARGEM}px">'
           f'{txt("<b>Critérios de status.</b> " + legenda_status() + " " + NOTA_DATAS, T_ROT, SUB)}</td></tr>')
    return pagina(f"Status Report {META['numero']} – Anexo",
                  [cabecalho("Status report semanal · anexo"), crono, em_dia, leg, rodape()])


if __name__ == "__main__":
    base = Path(__file__).parent
    for nome, html in (("status-report-02-premierpet.html", build()),
                       ("status-report-02-premierpet-anexo.html", build_anexo())):
        (base / nome).write_text(html, encoding="utf-8")
        print(f"ok -> {base / nome}")

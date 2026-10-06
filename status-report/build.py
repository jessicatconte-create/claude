"""Status Report semanal PremieRpet | Projeto Politica Comercial.

Gera dois HTMLs compativeis com e-mail (Outlook/Gmail): tabelas e estilos
inline, sem CSS externo.
  - status-report-02-premierpet.html        corpo executivo
  - status-report-02-premierpet-anexo.html  cronograma por atividade

Estrutura executiva: o titulo e a resposta da semana; cada secao abre com um
titulo-acao; visao por pilar no corpo, detalhe por atividade so no anexo.
Visual no sistema DOC: tokens da marca, Geist, escala 11 / 13 / 16 / 24,
respiros em multiplos de 8 (24 dentro do bloco, 24 entre blocos), cor so
para status. Uma coluna de 640px com larguras fluidas: le bem no celular.

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
W = 640
PAD = 24          # respiro interno do bloco
GAP = 24          # espaco entre blocos
MARGEM = 16       # margem lateral da peca

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

# Pendencias criticas: todos os campos, em destaque.
# Impedimento = ja trava uma entrega; Risco = pode travar se nao for tratado.
CRITICAS = [
    {"o_que": "Base de apuração da remuneração VI via distribuidor", "quem": "Gisele",
     "prazo": "23/09 → sem nova data", "entrega": "1. Política Comercial",
     "impacto": "Metas e percentuais calibrados só por premissa; entrega parcial em 13/10.",
     "acao": "Reunião com a Gisele até 09/10; sem data firme, escalonar.", "status": "Atrasado",
     "tipo": "Impedimento", "nivel": "Alto"},
    {"o_que": "Base de informações dos clientes do piloto", "quem": "PremieRpet (a indicar)",
     "prazo": "não definido", "entrega": "5. Business Case e Protocolo",
     "impacto": "Sem baseline não há incrementalidade, break-even nem grupo de comparação.",
     "acao": "Indicar responsável e data até 09/10*.", "status": "Em atenção",
     "tipo": "Risco", "nivel": "Alto"},
    {"o_que": "Governança preliminar (macrofluxo + RACI)", "quem": "DOC",
     "prazo": "06/11 → 23/10*", "entrega": "5. Business Case (capacidade)",
     "impacto": "O Business Case de 30/10 depende de um insumo previsto para depois dele.",
     "acao": "Antecipar uma versão preliminar para 23/10*.", "status": "Em atenção",
     "tipo": "Risco", "nivel": "Médio"},
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

RESPONSAVEL = {
    "nome": "Fábio Marconi",
    "empresa": "DOC Consulting",
    "email": "fabio.marconi@doc-consulting.com.br",
}




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


def p(inner, mt=0):
    return f'<p style="margin:{mt}px 0 0 0">{inner}</p>'


def sep(i, cor=LINHA):
    return "" if i == 0 else f"border-top:1px solid {cor};"


def card(inner, ultimo=False):
    return (f'<tr><td style="padding:0 {MARGEM}px {0 if ultimo else GAP}px {MARGEM}px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{BLOCO};border:1px solid {LINHA2};border-radius:16px;border-collapse:separate">'
            f'<tr><td style="padding:{PAD}px">{inner}</td></tr></table></td></tr>')


def bloco(kicker, acao, body, nota="", ultimo=False):
    nt = p(txt(nota, T_ROT, SUB), 16) if nota else ""
    return card(f'<p style="margin:0 0 8px 0">{rot(kicker, DESTAQUE)}</p>'
                f'<p style="margin:0 0 16px 0;font-family:{FONT};font-size:{T_SECAO}px;font-weight:600;'
                f'line-height:1.4;color:{NAVY}">{acao}</p>{body}{nt}', ultimo)


def item(titulo, direita, linhas, i):
    """Linha empilhada: titulo + etiqueta a direita, depois linhas de detalhe. Le bem em qualquer largura."""
    det = "".join(p(l, 4) for l in linhas)
    return tbl(f'<tr><td valign="top" style="padding:16px 8px 0 0;{sep(i)}">{titulo}</td>'
               f'<td valign="top" align="right" style="padding:16px 0 0 0;{sep(i)}">{direita}</td></tr>'
               f'<tr><td colspan="2" style="padding:0 0 16px 0">{det}</td></tr>')


def cabecalho(subtitulo):
    return (f'<tr><td style="padding:0 {MARGEM}px {GAP}px {MARGEM}px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{NAVY};border-radius:16px;border-collapse:separate"><tr>'
            f'<td style="padding:{PAD}px">'
            f'{txt("DOC", T_CORPO, "#FFFFFF", 700)}{txt(" Consulting", T_CORPO, CLARO)}'
            f'{txt(" &nbsp;·&nbsp; ", T_CORPO, CLARO)}{rot(subtitulo, CLARO)}'
            f'{p(txt(META["titulo"], T_SECAO, "#FFFFFF", 600), 8)}'
            f'{p(txt(META["numero"] + " · " + META["data"] + " · " + META["versao"], T_ROT, CLARO))}'
            f'</td></tr></table></td></tr>')


def rodape():
    return (f'<tr><td align="center" style="padding:{GAP}px {MARGEM}px 0 {MARGEM}px">'
            f'{txt("DOC Consulting | Status report semanal · © 2026 DOC Consulting. Todos os direitos reservados.", T_ROT, SUB)}'
            f'</td></tr>')


def pagina(titulo_html, linhas):
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="x-apple-disable-message-reformatting">'
        '<meta name="format-detection" content="telephone=no,address=no,email=no,date=no,url=no">'
        '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600;700&display=swap" rel="stylesheet">'
        f'<title>{titulo_html}</title></head>'
        f'<body style="margin:0;padding:0;background:{BG}">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{BG}">'
        f'<tr><td align="center" style="padding:{GAP}px 0">'
        f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" style="width:100%;max-width:{W}px">'
        + "".join(linhas) + '</table></td></tr></table></body></html>')


def legenda_status():
    return " · ".join(f"<b>{k}</b>: {v[2]}" for k, v in STATUS.items()) + \
        ". A entrega herda o pior status das suas dependências."


# ---------------------------------------------------------------- secoes
def barra_avanco():
    """Uma faixa por pilar, na cor do status: mostra de uma vez o avanco e onde esta o problema."""
    cor = {"Concluído": "#2E7D4F", "Em andamento": NAVY, "Em atenção": "#E0A030",
           "Atrasado": VERMELHO, "Não iniciado": LINHA2}
    w = f"{100 / len(PILARES):.2f}%"
    segs = "".join(f'<td width="{w}" style="padding:0 2px 0 0"><div style="height:8px;border-radius:4px;'
                   f'background:{cor[x[3]]};font-size:0;line-height:0">&nbsp;</div></td>' for x in PILARES)
    return tbl(f"<tr>{segs}</tr>")


def topo():
    c = STATUS[META["saude"]][0]
    n = {k: sum(1 for x in PILARES if x[3] == k) for k in STATUS}
    proxima = min((x for x in PILARES if x[6] is not None), key=lambda x: x[6])
    kpis = [
        ("Saúde do projeto", txt(META["saude"], T_SECAO, c, 700), "piloto de jan/27 mantido"),
        ("Avanço", txt(f'{n["Concluído"]} de {len(PILARES)} entregas', T_SECAO, NAVY, 700),
         f"concluídas · próxima em {proxima[2]}"),
        ("Pilares", txt(f'{n["Em atenção"] + n["Atrasado"]} de {len(PILARES)} em atenção', T_SECAO, c, 700),
         f'{n["Em andamento"]} em andamento · {n["Não iniciado"]} não iniciado'),
        ("Ações necessárias", txt(f"{len(DECISOES)} até 16/10", T_SECAO, VERMELHO, 700),
         "1 escalonamento · 3 decisões"),
    ]

    def kpi(k, v, s_, left):
        return (f'<td width="50%" valign="top" style="padding:16px 0 0 {16 if left else 0}px;'
                f'{"border-left:1px solid " + LINHA + ";" if left else ""}">'
                f'{rot(k)}<br>{v}<br>{txt(s_, T_ROT, SUB)}</td>')
    grade = (f'<tr>{kpi(*kpis[0], False)}{kpi(*kpis[1], True)}</tr>'
             f'<tr>{kpi(*kpis[2], False)}{kpi(*kpis[3], True)}</tr>')
    return card(
        f'<p style="margin:0;font-family:{FONT};font-size:{T_TITULO}px;font-weight:700;line-height:1.3;'
        f'letter-spacing:-0.02em;color:{NAVY}">{TITULO}</p>'
        + tbl(grade, f"margin-top:16px;border-top:1px solid {LINHA}")
        + f'<div style="height:16px;font-size:0;line-height:0">&nbsp;</div>{barra_avanco()}'
        + p(txt("Uma faixa por pilar, na cor do status: navy em andamento, âmbar em atenção, "
                "cinza não iniciado, verde concluído.", T_ROT, SUB), 8))


def decisoes():
    body = "".join(item(
        f'{rot(t, VERMELHO if t == "Escalonamento" else ROTULO)}<br>{txt(q, T_CORPO, INK, 700)}',
        txt(ate, T_CORPO, INK, 700, "white-space:nowrap"),
        [txt(why, T_CORPO, SUB), f'{rot("De quem")} {txt(quem)}'], i)
        for i, (t, q, why, quem, ate) in enumerate(DECISOES))
    return bloco("1 · Decisões necessárias / Escalonamentos", ACAO["decisoes"], body)


def timeline():
    n = len(SEMANAS)
    lw = 30                      # % da largura para o nome do pilar
    cw = f"{(100 - lw) / n:.2f}%"
    meses = [("Hoje", 1, DESTAQUE), ("outubro", 4, ROTULO), ("novembro", 5, ROTULO)]
    hdr = (f'<td width="{lw}%" style="padding:0 0 8px 0;border-bottom:1px solid {LINHA2}"></td>' + "".join(
        f'<td colspan="{span}" align="{"center" if span == 1 else "left"}" style="padding:0 0 8px 4px;'
        f'border-bottom:1px solid {LINHA2}">{txt(m, T_ROT, cor, 600)}</td>' for m, span, cor in meses))
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
        for i in range(n):
            if due is None:
                inner = txt("2027&rarr;", T_ROT, SUB, 600) if i == n - 1 else "&nbsp;"
            else:
                inner = barra if i < due else (losango(cor) if i == due else "&nbsp;")
            cells.append(cell(inner, i))
        out.append(f'<tr><td width="{lw}%" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {LINHA}">'
                   f'{txt(pilar, T_ROT, INK, 600)}</td>{"".join(cells)}</tr>')
    tri = f'<span style="font-family:Arial,sans-serif;font-size:{T_ROT}px;line-height:1;color:{VERMELHO}">&#9650;</span>'
    out.append(f'<tr><td width="{lw}%" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {LINHA}">'
               f'{txt("Decisões", T_ROT, VERMELHO, 600)}</td>'
               + "".join(cell(tri if i in DECISOES_SEMANA else "&nbsp;", i) for i in range(n)) + "</tr>")
    leg = p(txt("&#9670; entrega (navy no prazo, âmbar em atenção, cinza não iniciada) · ", T_ROT, SUB)
            + txt("&#9650; decisão (09/10 e 16/10)", T_ROT, VERMELHO), 8)
    return tbl("".join(out)) + leg


def pilares():
    body = "".join(item(
        txt(pl, T_CORPO, INK, 700), st(s),
        [f'{txt(e)} {txt("· " + pz, T_CORPO, SUB, extra="white-space:nowrap")}',
         f'{rot("Bloqueio")} {txt(blq)}',
         f'{rot("Próximo")} {txt(mk)}',
         txt("<b>Concluída quando:</b> " + crit, T_CORPO, SUB)], i)
        for i, (pl, e, pz, s, blq, mk, _, crit) in enumerate(PILARES))
    return bloco("2 · Visão por pilar", ACAO["pilares"],
                 timeline() + f'<div style="height:{GAP}px;font-size:0;line-height:0">&nbsp;</div>' + body)


def avancos():
    body = "".join(tbl(f'<tr><td style="padding:8px 0;{sep(k)}">{txt(r, T_CORPO, INK, 700)}<br>'
                       f'{txt(i, T_CORPO, SUB)}</td></tr>') for k, (r, i) in enumerate(AVANCOS))
    return bloco("3 · Avanços do ciclo", ACAO["avancos"], body, f"Em curso, sem resultado ainda: {EM_CURSO}")


def pendencias():
    nivel_cor = {"Alto": VERMELHO, "Médio": AMBAR}
    body = ""
    for tipo, titulo in (("Impedimento", "Impedimentos · já travam uma entrega"),
                         ("Risco", "Riscos · podem travar se não forem tratados")):
        itens = [x for x in CRITICAS if x["tipo"] == tipo]
        if not itens:
            continue
        body += p(rot(titulo, NAVY), 16 if body else 0)
        body += "".join(item(
            txt(x["o_que"], T_CORPO, INK, 700), st(x["status"]),
            [f'{rot("Impacto")} {txt(x["nivel"], T_CORPO, nivel_cor[x["nivel"]], 700)} '
             f'{txt("· " + x["impacto"])}',
             f'{rot("De quem")} {txt(x["quem"])} &nbsp;·&nbsp; {rot("Prazo")} {txt(x["prazo"])}',
             f'{rot("Impacta")} {txt(x["entrega"])}',
             f'{rot("Mitigação")} {txt(x["acao"], weight=600)}'], i)
            for i, x in enumerate(itens))
    return bloco("4 · Pendências e dependências", ACAO["pendencias"], body,
                 f"As demais {len(EM_DIA)} dependências estão em dia, com prazo original mantido; "
                 f"detalhe no anexo.")


def protocolo():
    linhas = ""
    for k in range(0, len(PROTOCOLO), 2):
        linhas += "<tr>" + "".join(
            f'<td width="50%" valign="top" style="padding:8px 8px 8px 0;{sep(k)}">'
            f'{txt(c, T_CORPO, INK, 600)}<br>{st(s)}</td>' for c, s in PROTOCOLO[k:k + 2]) + "</tr>"
    return bloco("5 · Protocolo do piloto · evolução semanal", ACAO["protocolo"], tbl(linhas), PROTOCOLO_NOTA)


def assinatura():
    r = RESPONSAVEL
    return card(
        f'{rot("Responsável pelo report")}'
        + p(txt(r["nome"], T_SECAO, NAVY, 700), 8)
        + p(txt(f'{r["empresa"]} · <a href="mailto:{r["email"]}" style="color:{DESTAQUE};text-decoration:none">'
                f'{r["email"]}</a>', T_CORPO, SUB))
        + p(txt("Dúvidas sobre qualquer ponto ou sobre as decisões pendentes: é só responder este e-mail.",
                T_CORPO, SUB), 8), ultimo=True)


def notas():
    return (f'<tr><td style="padding:{GAP}px {MARGEM}px 0 {MARGEM}px">'
            + p(txt("<b>Critérios de status.</b> " + legenda_status(), T_ROT, SUB))
            + p(txt(NOTA_DATAS + " Anexo: cronograma por atividade e dependências em dia (arquivo separado).",
                    T_ROT, SUB), 8) + '</td></tr>')


def build():
    return pagina(f"Status Report {META['numero']} – PremieRpet",
                  [cabecalho("Status report semanal"), topo(), decisoes(), pilares(), avancos(),
                   pendencias(), protocolo(), assinatura(), notas(), rodape()])


# ---------------------------------------------------------------- anexo
def build_anexo():
    ws = ["46%", "16%", "38%"]
    rws = []
    for frente, ativs in CRONOGRAMA:
        rws.append(f'<tr><td colspan="3" style="padding:16px 0 8px 0">{txt(frente, T_CORPO, NAVY, 700)}</td></tr>')
        for a, ow, pz, s, dep, mk in ativs:
            cells = [f'{txt(a, T_ROT, INK, 600)}<br>{txt(ow, T_ROT, SUB)}<br>{st(s)}',
                     txt(pz, T_ROT), f'{txt(dep, T_ROT)}<br>{txt("Próximo: " + mk, T_ROT, SUB)}']
            rws.append("<tr>" + "".join(
                f'<td valign="top" width="{w}" style="padding:8px 8px 8px 0;border-top:1px solid {LINHA}">{c}</td>'
                for c, w in zip(cells, ws)) + "</tr>")
    head = "<tr>" + "".join(
        f'<td width="{w}" style="padding:0 8px 8px 0;border-bottom:1px solid {LINHA2}">{rot(h)}</td>'
        for h, w in zip(["Atividade / owner / status", "Prazo", "Dependência / próximo"], ws)) + "</tr>"
    crono = bloco("Anexo A · Cronograma por frente", "Atividades por frente, com dono, status e próximo marco",
                  tbl(head + "".join(rws)))
    em_dia = bloco("Anexo B · Dependências em dia", "Prazo original mantido; nenhuma ação adicional necessária",
                   "".join(item(txt(d, T_CORPO, INK, 600), txt(pz, T_CORPO, INK, 700, "white-space:nowrap"),
                                [f'{rot("De quem")} {txt(q)} &nbsp;·&nbsp; {rot("Impacta")} {txt(imp)}'], i)
                           for i, (d, q, pz, imp) in enumerate(EM_DIA)), ultimo=True)
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

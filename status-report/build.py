"""Status Report semanal PremieRpet | Projeto RGM - Politica Comercial.

Gera um HTML compativel com e-mail (Outlook/Gmail): tabelas, estilos inline,
sem CSS externo. Todo o conteudo do report fica nos dados abaixo; para a
proxima semana, atualize os dados e rode:  python3 build.py
"""
from html import escape
from pathlib import Path

# ---------------------------------------------------------------- identidade
NAVY = "#0A1D5C"; BLUE = "#1A56DB"; INK = "#14171F"; SUB = "#5B6472"
LINE = "#E5E7EB"; PANEL = "#F4F7FD"; LB1 = "#EAF0FB"; G1 = "#888D97"
FONT = "Arial, Helvetica, sans-serif"
W = 900

# Criterios objetivos de status (mesma escala para atividade e entrega)
STATUS = {
    "Concluído":    ("#DCFCE7", "#166534", "Critério de conclusão atendido e validado pela PremieRpet."),
    "Em andamento": (LB1,       BLUE,      "Iniciado, dependências em dia e prazo preservado."),
    "Em atenção":   ("#FEF3C7", "#92400E", "Prazo ainda preservado, mas há dependência pendente, sem dono/data ou "
                                           "sequência que pode comprometer a entrega se não for destravada."),
    "Atrasado":     ("#FDE2E1", "#B42318", "Prazo vencido, ou dependência vencida que já compromete a data."),
    "Não iniciado": ("#F0F1F3", SUB,       "Início previsto para data futura; nada a cobrar ainda."),
}

META = {
    "numero": "#2 (versão revisada)",
    "semana": "Semana encerrada em 02/10/2026",
    "cliente": "PremieRpet",
    "projeto": "Projeto RGM | Política Comercial",
    "saude": "Em atenção",
}

SUMARIO = [
    ("Onde estamos",
     "Desenho da nova política comercial para o piloto GO/DF, com início do piloto mantido em janeiro/2027. "
     "Na semana fechamos três definições de desenho do piloto (detalhe em Avanços)."),
    ("Principal risco",
     "<b>Entrega 1 – Política Comercial (13/10) em atenção.</b> A base de apuração dos descontos de campanhas da "
     "remuneração VI via distribuidor (Gisele) venceu em 23/09 e ainda não foi recebida. Sem ela até 09/10, "
     "metas, percentuais e elegibilidade serão entregues com premissas não calibradas pelo histórico, ou seja, "
     "entrega parcial em 13/10."),
    ("Outros pontos de atenção",
     "<b>Business Case (30/10)</b>: a base de clientes do piloto, necessária para baseline e lógica econômica, "
     "ainda não tem responsável nem data; e o item de capacidade/treinamento depende do modelo de governança, "
     "hoje previsto só para 06/11. <b>Banda/RTP (21/10) e Governança (06/11)</b> dependem da decisão de TI + IC "
     "sobre apuração manual x semiautomatizada até 16/10."),
    ("Ajustes no plano",
     "O Business Case de 30/10 passa a trazer a lógica econômica <i>ex ante</i> do piloto (investimento, "
     "incrementalidade necessária, retorno esperado, break-even e sensibilidades) antes da decisão de "
     "implementação. O Protocolo do Piloto vira entrega própria, acompanhada semanalmente."),
]

# Decisoes necessarias / escalonamentos
DECISOES = [
    {"tipo": "Escalonamento",
     "o_que": "Priorizar a entrega da base de apuração dos descontos de campanhas da remuneração VI via "
              "distribuidor e fixar nova data. Vencida desde 23/09.",
     "quem": "Michelle Uema, junto à Gisele",
     "ate": "09/10",
     "senao": "Entrega 1 (13/10) sai parcial: metas e percentuais sem calibração histórica."},
    {"tipo": "Decisão",
     "o_que": "Critério de apuração: 100% dos clientes, amostra ou média, com requisitos mínimos.",
     "quem": "Gisele",
     "ate": "09/10",
     "senao": "Governança (06/11) e mecânica da Banda/RTP (21/10) ficam sem regra de apuração."},
    {"tipo": "Decisão",
     "o_que": "Apuração meta x realizado do piloto: manual ou semiautomatizada.",
     "quem": "Henrique (TI) e Yves (IC)",
     "ate": "16/10",
     "senao": "Item 6 da Banda/RTP (21/10) e guardrails da Governança ficam sem base. Folga de 5 dias até 21/10."},
    {"tipo": "Decisão",
     "o_que": "Definir responsável e data da base de informações dos clientes do piloto.",
     "quem": "PremieRpet (a indicar)",
     "ate": "09/10*",
     "senao": "Sem baseline: Business Case ex ante e Protocolo do Piloto não fecham em 30/10."},
]

# Painel de entregas (saude da ENTREGA, nao da atividade)
ENTREGAS = [
    ("1. Política Comercial: tabela, camadas e parâmetros", "DOC", "13/10", "Em atenção",
     "Dependência vencida desde 23/09 (base remuneração VI, Gisele)."),
    ("2. Economia dos Canais", "DOC", "14/10", "Em andamento",
     "Visita ao distribuidor GO em 06–07/10 alimenta a DRE do distribuidor."),
    ("3. Banda, RTP e incentivo ao shopper", "DOC", "21/10", "Em andamento",
     "Depende da decisão TI + IC (16/10); folga de 5 dias."),
    ("5. Business Case <i>ex ante</i> do piloto", "DOC", "30/10", "Em atenção",
     "Base de clientes do piloto sem responsável/data; capacidade depende da Governança (06/11)."),
    ("5.1 Protocolo do Piloto (v0)", "DOC", "30/10*", "Não iniciado",
     "Nova entrega. Versão final em 30/11. Acompanhamento semanal abaixo."),
    ("4. Governança", "DOC", "06/11", "Em andamento",
     "Plano de ação com TI, IC e Gisele em curso; decisões em 09/10 e 16/10."),
    ("5.1 Piloto: campo, dados e validações", "DOC", "30/11", "Em andamento",
     "Primeira visita de campo em GO em 06/10."),
    ("6. Implementação: treinamento e rollout", "DOC / PremieRpet", "jan–ago/27", "Não iniciado",
     "Data do treinamento a definir até 30/10."),
]

# Avancos: resultado (decidido / validado / aprendido) + implicacao
AVANCOS = [
    ("Decidido",
     "O piloto não depende da nova ferramenta: apuração manual ou semiautomatizada.",
     "Tira a ferramenta do caminho crítico de jan/27. A escolha entre manual e semiautomatizada fica com "
     "TI + IC até 16/10."),
    ("Validado",
     "A RTP pode ser aplicada on-invoice no menor nível (SKU → pedido).",
     "Permite desenhar a RTP direto na nota, por SKU, na Entrega 3 (21/10), sem mecanismo de reembolso posterior."),
    ("Decidido",
     "A apuração meta x realizado das novas alavancas (sell-in volume e sell-in mix) será manual, com "
     "apuração provisória uma semana antes do fechamento do mês.",
     "Reduz o risco de desconto indevido e protege o recebimento. Exige calendário e responsáveis definidos "
     "no modelo de Governança (Entrega 4)."),
    ("Mantido",
     "Início do piloto GO/DF em janeiro/2027.",
     "Todas as entregas de out–nov seguem dimensionadas para esse marco."),
]
EM_CURSO = ("Base de descontos recebida em 01/10 (análise de consistência até 09/10) e pesquisa de preços "
            "ao consumidor recebida em 02/10 (validação até 07/10). Ainda não há conclusão a reportar: os "
            "resultados entram no próximo status.")

# Pendencias e dependencias: todos os campos explicitos
PENDENCIAS = [
    {"o_que": "Base de apuração dos descontos de campanhas da remuneração VI via distribuidor",
     "quem": "Gisele (PremieRpet)", "orig": "23/09", "atual": "Sem nova data",
     "entrega": "1. Política Comercial: metas, percentuais e elegibilidade",
     "impacto": "Parâmetros calibrados só por premissa; entrega parcial em 13/10.",
     "acao": "DOC agenda reunião com Gisele até 09/10. Sem data firme, escalonar (Decisão 1).",
     "status": "Atrasado"},
    {"o_que": "Base de informações dos clientes do piloto",
     "quem": "PremieRpet (responsável a indicar)", "orig": "Não definido", "atual": "Não definido",
     "entrega": "5. Business Case e 5.1 Protocolo do Piloto (baseline)",
     "impacto": "Sem baseline não há incrementalidade, break-even nem grupo de comparação.",
     "acao": "Indicar responsável e data até 09/10* (Decisão 4).",
     "status": "Em atenção"},
    {"o_que": "Modelo de governança preliminar (macrofluxo + RACI) para o item de capacidade do Business Case",
     "quem": "DOC", "orig": "06/11", "atual": "23/10* (versão preliminar)",
     "entrega": "5. Business Case: capacidade, treinamento e sustentação",
     "impacto": "O Business Case de 30/10 depende de um insumo hoje previsto para depois dele.",
     "acao": "Antecipar versão preliminar do macrofluxo e RACI para 23/10*.",
     "status": "Em atenção"},
    {"o_que": "Critério de apuração: 100%, amostra ou média, com requisitos mínimos",
     "quem": "Gisele (PremieRpet)", "orig": "09/10", "atual": "09/10",
     "entrega": "4. Governança; 3. Banda/RTP (mecânica)",
     "impacto": "Define o esforço operacional da apuração manual.",
     "acao": "Follow-up na reunião de 07/10.",
     "status": "Em andamento"},
    {"o_que": "Fluxo mapeado e possibilidades de automação identificadas",
     "quem": "Henrique (TI)", "orig": "16/10", "atual": "16/10",
     "entrega": "3. Banda/RTP (item 6); 4. Governança",
     "impacto": "Sem ele não há decisão manual x semiautomatizada.",
     "acao": "Ponto de controle com TI em 09/10*.",
     "status": "Em andamento"},
    {"o_que": "Fluxo e alternativas avaliados (decisão manual x semiautomatizada)",
     "quem": "Yves (IC) e Henrique (TI)", "orig": "16/10", "atual": "16/10",
     "entrega": "3. Banda/RTP (item 6); 4. Governança (guardrails)",
     "impacto": "Folga de 5 dias até a Entrega 3 (21/10).",
     "acao": "Manter 16/10; qualquer deslize vira escalonamento.",
     "status": "Em andamento"},
    {"o_que": "Validação da abertura das metas pelos distribuidores (100% dos clientes)",
     "quem": "Fábio Marconi (DOC)", "orig": "06/10", "atual": "06–07/10",
     "entrega": "1. Política Comercial; 2. Economia dos Canais",
     "impacto": "Confirma se a meta por cliente é apurável no distribuidor.",
     "acao": "Visita de campo GO em 06–07/10.",
     "status": "Em andamento"},
    {"o_que": "Análise de consistência da base de descontos (recebida em 01/10)",
     "quem": "DOC", "orig": "09/10", "atual": "09/10",
     "entrega": "1. Política Comercial: tabela, camadas e pocket price",
     "impacto": "Base do pocket price atual por cliente.",
     "acao": "Concluir até 09/10.",
     "status": "Em andamento"},
    {"o_que": "Validação da pesquisa de preços ao consumidor, lojas físicas e marketplaces (recebida em 02/10)",
     "quem": "DOC", "orig": "07/10", "atual": "07/10",
     "entrega": "3. Banda, RTP e incentivo ao shopper",
     "impacto": "Base para a banda de preço por SKU/canal.",
     "acao": "Concluir até 07/10.",
     "status": "Em andamento"},
]

# Criterios de conclusao por entrega: o que estara fechado na data
CRITERIOS = [
    ("1. Política Comercial: tabela, camadas e parâmetros", "13/10", "Em atenção", [
        "Tabela de preço e camadas de remuneração definidas por canal/tipo de cliente, com pocket price calculado.",
        "Metas, percentuais e regras de elegibilidade parametrizados para cada alavanca (sell-in volume e sell-in mix).",
        "Simulação do investimento por faixa de atingimento, comparada ao investimento atual.",
        "Material validado com RGM/Comercial PremieRpet na reunião de 13/10.",
    ]),
    ("2. Economia dos Canais", "14/10", "Em andamento", [
        "DRE do distribuidor GO (margem, custo de servir) construída e validada com dados de campo.",
        "Economia de cada canal no modelo atual x proposto, com a remuneração que viabiliza a operação eficiente.",
    ]),
    ("3. Banda, RTP e incentivo ao shopper", "21/10", "Em andamento", [
        "Banda de preço (piso e teto) por SKU/canal, com base na pesquisa de preços.",
        "Mecânica da RTP on-invoice (SKU → pedido) e do incentivo ao shopper definida.",
        "Cenários quantitativos de impacto em preço, volume e margem.",
        "Mecânica encaixada no modelo de apuração escolhido por TI + IC.",
    ]),
    ("5. Business Case <i>ex ante</i> do piloto", "30/10", "Em atenção", [
        "Investimento previsto (descontos, RTP, incentivos e custo operacional).",
        "Impacto esperado em volume, mix e margem.",
        "Incrementalidade necessária para pagar o investimento (break-even em volume e margem).",
        "Retorno esperado (ROI) em cenários pessimista, base e otimista.",
        "Premissas explícitas e sensibilidades às principais variáveis.",
        "As Is x To Be, transição, capacidade, treinamento e sustentação.",
        "<b>Regra:</b> a decisão de implementar o piloto é tomada com este Business Case aprovado. "
        "Jan–abr/27 é só a medição do resultado <i>realizado</i> contra estas premissas.",
    ]),
    ("4. Governança", "06/11", "Em andamento", [
        "Macrofluxo de apuração, pagamento e exceções, com Matriz RACI.",
        "Critério de apuração (100%, amostra ou média) e calendário com apuração provisória.",
        "Guardrails e trava de complexidade.",
        "Validado por Trade, RGM, Inteligência Comercial e TI.",
    ]),
]

# Protocolo do piloto: acompanhamento semanal por componente
PROTOCOLO = [
    ("Hipótese a ser testada", "Não iniciado", "Derivada do Business Case; primeira versão em 30/10*."),
    ("Baseline", "Em atenção", "Depende da base de clientes do piloto, ainda sem responsável e data."),
    ("Grupo de controle / contrafactual", "Não iniciado", "Proposta de grupo de comparação fora de GO/DF em 30/10*."),
    ("Mecânica", "Em andamento", "Já definido: RTP on-invoice e apuração manual com prévia. Falta a decisão TI + IC (16/10)."),
    ("Investimento", "Não iniciado", "Vem do Business Case <i>ex ante</i> (30/10)."),
    ("KPIs", "Não iniciado", "Volume, mix, margem e pocket price por cliente (a validar)."),
    ("Critérios de sucesso", "Não iniciado", "Incrementalidade mínima = break-even do Business Case."),
    ("Regra de decisão ao final", "Não iniciado", "Expandir, ajustar ou encerrar; define o gatilho do rollout de abr/27."),
]

# Cronograma por frente: Atividade | Owner | Prazo | Status | Dependencia/Bloqueio | Proximo marco
CRONOGRAMA = [
    ("1. Política Comercial", [
        ("Tabela, camadas de remuneração e pocket price", "DOC", "13/10", "Em andamento",
         "Base de descontos (01/10) em análise pela DOC", "09/10: análise da base concluída"),
        ("Metas, percentuais e elegibilidade", "DOC", "13/10", "Em atenção",
         "<b>Base remuneração VI (Gisele): vencida desde 23/09</b>", "09/10: reunião com Gisele / escalonamento"),
        ("Simulação da economia por atingimento", "DOC", "13/10", "Em andamento",
         "Itens acima", "13/10: entrega"),
    ]),
    ("2. Economia dos Canais", [
        ("Economia do distribuidor e operação eficiente", "DOC", "14/10", "Em andamento",
         "Visita ao distribuidor GO (DRE)", "06–07/10: visita de campo"),
    ]),
    ("3. Banda e RTP", [
        ("Cenários quantitativos", "DOC", "21/10", "Em andamento",
         "Pesquisa de preços (02/10) em validação pela DOC", "07/10: validação concluída"),
        ("Mecânica nos modelos de governança", "DOC", "21/10", "Em andamento",
         "Decisão manual x semiautomatizada (TI + IC, 16/10)", "16/10: decisão TI + IC"),
    ]),
    ("5. Business Case <i>ex ante</i>", [
        ("Lógica econômica: investimento, impacto, incrementalidade, ROI, break-even e sensibilidades",
         "DOC", "30/10", "Não iniciado",
         "Entregas 1–3; <b>base de clientes do piloto (sem responsável/data)</b>", "09/10*: responsável e data da base"),
        ("As Is x To Be e transição", "DOC", "30/10", "Não iniciado", "Entregas 1–3", "21/10: insumos completos"),
        ("Capacidade, treinamento e sustentação", "DOC", "30/10", "Em atenção",
         "Macrofluxo + RACI previstos só para 06/11", "23/10*: versão preliminar da governança"),
    ]),
    ("4. Governança", [
        ("Governança, apuração, pagamento e exceções", "DOC", "06/11", "Em andamento",
         "Validação de Trade, RGM, IC e respostas de TI", "09/10: critério de apuração (Gisele)"),
        ("Guardrails e trava de complexidade", "DOC", "06/11", "Não iniciado",
         "Decisão TI + IC (16/10)", "16/10: decisão TI + IC"),
    ]),
    ("5.1 Piloto", [
        ("Protocolo: hipótese, baseline, contrafactual, mecânica, investimento, KPIs, critérios, regra de decisão",
         "DOC", "v0 30/10* · final 30/11", "Não iniciado",
         "Business Case <i>ex ante</i>; base de clientes do piloto", "30/10*: v0 junto com o Business Case"),
        ("Campo, dados e validações", "DOC", "30/11", "Em andamento",
         "Visita de campo e distribuidor GO", "06–07/10: visita"),
        ("Medição <i>ex post</i>: ROI realizado e break-even", "DOC", "02/01 a 02/04/27", "Não iniciado",
         "Protocolo aprovado e baseline", "30/11: protocolo final"),
    ]),
    ("6. Implementação", [
        ("Treinamento da equipe comercial do piloto", "DOC", "A definir", "Não iniciado",
         "Validação da política piloto", "30/10: data do treinamento definida"),
        ("Rollout Brasil (4 meses)", "PremieRpet", "04/04 a 03/08/27", "Não iniciado",
         "Resultado do piloto e regra de decisão do protocolo", "02/04/27: decisão de rollout"),
    ]),
]

AGENDA = [
    ("06–07/10", "Campo GO: visita ao distribuidor (Fábio Marconi)", "Marco"),
    ("07/10", "Reunião prévia (equipe do projeto): Política Comercial", "Reunião"),
    ("09/10", "Gisele: critério de apuração e reunião sobre a base VI · prazo do escalonamento", "Decisão"),
    ("13/10", "<b>Entrega 1</b>: Política Comercial: tabela, camadas e parâmetros", "Entrega"),
    ("14/10", "<b>Entrega 2</b>: Economia dos Canais", "Entrega"),
    ("16/10", "TI + IC: apuração manual x semiautomatizada", "Decisão"),
    ("21/10", "Reunião de RTP e <b>Entrega 3</b>: Banda, RTP e incentivo ao shopper", "Entrega"),
    ("30/10", "<b>Entrega 5</b>: Business Case <i>ex ante</i> + Protocolo do Piloto v0* + data do treinamento", "Entrega"),
    ("06/11", "<b>Entrega 4</b>: Governança", "Entrega"),
]

MUDANCAS = [
    "Business Case (30/10) ampliado para a lógica econômica <i>ex ante</i> do piloto. O antigo item “ROI e "
    "break-even: piloto” (jan–abr/27) passa a ser a medição <i>ex post</i>, dentro da frente 5.1 Piloto.",
    "Protocolo do Piloto passa a ser entrega própria: v0 em 30/10*, versão final em 30/11. Antes, só começava "
    "após a validação do Business Case.",
    "Status reclassificados pelos critérios objetivos da legenda: atividades que não começaram aparecem "
    "como “Não iniciado”.",
]


# ---------------------------------------------------------------- render
def pill(status, size=11):
    bg, fg, _ = STATUS[status]
    return (f'<span style="display:inline-block;padding:3px 9px;border-radius:10px;background:{bg};'
            f'color:{fg};font-family:{FONT};font-size:{size}px;font-weight:bold;white-space:nowrap">'
            f'{escape(status)}</span>')


def section(title, body, note=""):
    n = f'<span style="font-weight:normal;color:{G1};letter-spacing:0"> · {note}</span>' if note else ""
    return (f'<tr><td style="padding:26px 28px 0 28px">'
            f'<p style="margin:0 0 10px 0;font-family:{FONT};font-size:12px;font-weight:bold;color:{BLUE};'
            f'letter-spacing:1.2px;text-transform:uppercase;border-bottom:2px solid {BLUE};padding-bottom:6px">'
            f'{title}{n}</p>{body}</td></tr>')


def table(headers, rows, widths, zebra=True):
    th = "".join(
        f'<th align="left" width="{w}" style="padding:7px 8px;font-family:{FONT};font-size:10.5px;'
        f'color:{SUB};font-weight:bold;text-transform:uppercase;letter-spacing:.4px;background:{PANEL};'
        f'border-bottom:1px solid {LINE}">{h}</th>' for h, w in zip(headers, widths))
    trs = []
    for i, r in enumerate(rows):
        bg = "#FFFFFF" if (not zebra or i % 2 == 0) else "#FAFBFD"
        tds = "".join(
            f'<td valign="top" style="padding:8px;font-family:{FONT};font-size:12px;line-height:1.4;'
            f'color:{INK};border-bottom:1px solid {LINE};background:{bg}">{c}</td>' for c in r)
        trs.append(f"<tr>{tds}</tr>")
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse;border:1px solid {LINE}"><tr>{th}</tr>{"".join(trs)}</table>')


def small(t, color=SUB):
    return f'<span style="font-size:11px;color:{color}">{t}</span>'


def build():
    out = []
    # cabecalho
    out.append(
        f'<tr><td style="background:{NAVY};padding:22px 28px">'
        f'<p style="margin:0;font-family:{FONT};font-size:11px;letter-spacing:1.5px;color:#AFC1EE;font-weight:bold">'
        f'STATUS REPORT SEMANAL · {escape(META["numero"])}</p>'
        f'<p style="margin:6px 0 0 0;font-family:{FONT};font-size:22px;color:#FFFFFF;font-weight:bold">'
        f'{META["cliente"]} | {META["projeto"]}</p>'
        f'<p style="margin:4px 0 0 0;font-family:{FONT};font-size:12px;color:#AFC1EE">{META["semana"]}</p>'
        f'</td></tr>')

    # saude geral
    out.append(
        f'<tr><td style="padding:20px 28px 0 28px">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="background:#FFFBEB;border:1px solid #FCD34D;border-left:5px solid #D97706">'
        f'<tr><td style="padding:12px 16px;font-family:{FONT};font-size:13px;line-height:1.45;color:{INK}">'
        f'<b>Saúde do projeto:</b> {pill(META["saude"], 12)}&nbsp; Piloto de jan/27 mantido. '
        f'A Entrega 1 (13/10) corre risco de sair parcial por uma dependência vencida desde 23/09. '
        f'Há <b>1 escalonamento</b> e <b>3 decisões</b> necessárias até 16/10.</td></tr></table></td></tr>')

    # sumario
    rows = "".join(
        f'<tr><td valign="top" width="150" style="padding:6px 10px 6px 0;font-family:{FONT};font-size:12px;'
        f'font-weight:bold;color:{NAVY}">{k}</td><td valign="top" style="padding:6px 0;font-family:{FONT};'
        f'font-size:13px;line-height:1.5;color:{INK}">{v}</td></tr>' for k, v in SUMARIO)
    out.append(section("Sumário executivo",
                       f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{rows}</table>'))

    # decisoes
    out.append(section("Decisões necessárias / Escalonamentos", table(
        ["#", "Tipo", "O que precisamos", "De quem", "Até", "Se não acontecer"],
        [[str(i + 1),
          f'<b style="color:{"#B42318" if d["tipo"] == "Escalonamento" else NAVY}">{d["tipo"]}</b>',
          d["o_que"], d["quem"], f'<b>{d["ate"]}</b>', d["senao"]] for i, d in enumerate(DECISOES)],
        [22, 95, 290, 130, 50, 260])))

    # painel de entregas
    out.append(section("Painel de entregas", table(
        ["Entrega", "Owner", "Prazo", "Saúde", "Por quê"],
        [[f"<b>{n}</b>", o, p, pill(s), w] for n, o, p, s, w in ENTREGAS],
        [270, 80, 70, 100, 330])))

    # avancos
    out.append(section("Avanços do ciclo", table(
        ["", "Resultado", "Implicação para o projeto"],
        [[f'<b style="color:#166534">{t}</b>', r, i] for t, r, i in AVANCOS],
        [70, 380, 400]) +
        f'<p style="margin:8px 0 0 0;font-family:{FONT};font-size:11.5px;line-height:1.45;color:{SUB}">'
        f'<b>Em curso, sem resultado ainda:</b> {EM_CURSO}</p>', "decidido, validado ou aprendido"))

    # pendencias
    out.append(section("Pendências e dependências", table(
        ["O que está pendente / de quem", "Prazo original → atual", "Entrega impactada e impacto",
         "Próxima ação para destravar", "Status"],
        [[f'<b>{p["o_que"]}</b><br>{small("De quem: " + p["quem"])}',
          f'{p["orig"]} → <b>{p["atual"]}</b>',
          f'{p["entrega"]}<br>{small(p["impacto"])}',
          p["acao"], pill(p["status"])] for p in PENDENCIAS],
        [250, 105, 230, 180, 85])))

    # criterios de conclusao
    blocks = []
    for nome, prazo, st, itens in CRITERIOS:
        lis = "".join(f'<li style="margin:0 0 3px 0">{x}</li>' for x in itens)
        blocks.append(
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border:1px solid {LINE};margin:0 0 10px 0">'
            f'<tr><td style="background:{PANEL};padding:8px 12px;font-family:{FONT};font-size:12.5px;'
            f'color:{NAVY}"><b>{nome}</b> &nbsp;·&nbsp; {prazo} &nbsp; {pill(st)}</td></tr>'
            f'<tr><td style="padding:8px 12px 6px 12px;font-family:{FONT};font-size:12px;line-height:1.45;color:{INK}">'
            f'<ul style="margin:0;padding-left:18px">{lis}</ul></td></tr></table>')
    out.append(section("Critérios de conclusão por entrega", "".join(blocks),
                       "o que estará fechado na data para considerarmos entregue"))

    # protocolo
    out.append(section("Protocolo do Piloto: evolução semanal", table(
        ["Componente", "Status", "Situação nesta semana"],
        [[f"<b>{c}</b>", pill(s), t] for c, s, t in PROTOCOLO],
        [220, 100, 530]), "v0 em 30/10*, final em 30/11"))

    # cronograma por frente
    rows = []
    for frente, ativs in CRONOGRAMA:
        rows.append(f'<tr><td colspan="6" style="padding:7px 8px;background:{LB1};font-family:{FONT};'
                    f'font-size:12px;font-weight:bold;color:{NAVY};border-bottom:1px solid {LINE}">{frente}</td></tr>')
        for a, o, p, s, d, m in ativs:
            rows.append("<tr>" + "".join(
                f'<td valign="top" style="padding:7px 8px;font-family:{FONT};font-size:11.5px;line-height:1.4;'
                f'color:{INK};border-bottom:1px solid {LINE}">{c}</td>'
                for c in [a, o, p, pill(s, 10.5), d, m]) + "</tr>")
    hdr = "".join(
        f'<th align="left" width="{w}" style="padding:7px 8px;font-family:{FONT};font-size:10.5px;color:{SUB};'
        f'text-transform:uppercase;letter-spacing:.4px;background:{PANEL};border-bottom:1px solid {LINE}">{h}</th>'
        for h, w in zip(["Atividade", "Owner", "Prazo", "Status", "Dependência / bloqueio", "Próximo marco"],
                        [230, 70, 85, 95, 200, 170]))
    out.append(section("Cronograma por frente",
                       f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
                       f'style="border-collapse:collapse;border:1px solid {LINE}"><tr>{hdr}</tr>{"".join(rows)}</table>'))

    # agenda
    out.append(section("Próximos marcos", table(
        ["Data", "Marco", "Tipo"], [[f"<b>{d}</b>", m, t] for d, m, t in AGENDA], [80, 680, 90])))

    # legenda + mudancas
    leg = "".join(
        f'<tr><td valign="top" width="110" style="padding:4px 0">{pill(k, 10.5)}</td>'
        f'<td style="padding:4px 0;font-family:{FONT};font-size:11.5px;color:{SUB}">{v[2]}</td></tr>'
        for k, v in STATUS.items())
    mud = "".join(f'<li style="margin:0 0 3px 0">{m}</li>' for m in MUDANCAS)
    out.append(section("Critérios de status",
                       f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{leg}</table>'
                       f'<p style="margin:8px 0 0 0;font-family:{FONT};font-size:11.5px;color:{SUB}">'
                       f'Atividade e entrega usam a mesma escala. A entrega herda o pior status relevante das suas '
                       f'dependências: se depende de algo vencido, fica no mínimo “Em atenção”. '
                       f'<b>*</b> Data proposta pela DOC, a confirmar com a PremieRpet.</p>'))
    out.append(section("Mudanças no plano nesta edição",
                       f'<ul style="margin:0;padding-left:18px;font-family:{FONT};font-size:12px;'
                       f'line-height:1.45;color:{INK}">{mud}</ul>'))

    # rodape
    out.append(f'<tr><td style="padding:26px 28px 22px 28px;font-family:{FONT};font-size:10.5px;color:{G1}">'
               f'DOC Consulting | Status report semanal<br>© 2026 DOC Consulting. Todos os direitos reservados.'
               f'</td></tr>')

    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Status Report #2 – {META["cliente"]}</title></head>'
        f'<body style="margin:0;padding:0;background:#F3F4F6">'
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F3F4F6">'
        f'<tr><td align="center" style="padding:20px 8px">'
        f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" '
        f'style="width:{W}px;max-width:100%;background:#FFFFFF;border:1px solid {LINE}">'
        + "".join(out) +
        '</table></td></tr></table></body></html>')


if __name__ == "__main__":
    dst = Path(__file__).with_name("status-report-02-premierpet.html")
    dst.write_text(build(), encoding="utf-8")
    print(f"ok -> {dst}")

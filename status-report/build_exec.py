"""Versao "consultoria estrategica" do Status Report.

Mesmo conteudo de build.py, com outra linguagem visual:
- resposta primeiro: o titulo do documento e a conclusao da semana;
- cada secao abre com um titulo-acao (a frase que diz o "e dai?");
- cor so para excecao: o que esta no prazo fica em cinza, so atencao/atraso ganham cor;
- linhas finas no lugar de caixas; tipografia serifada nos titulos;
- Exhibit com a linha do tempo das entregas.
Rode:  python3 build_exec.py
"""
from pathlib import Path

from build import (AVANCOS, CRITICAS, CRONOGRAMA, DECISOES, EM_CURSO, EM_DIA, ENTREGAS, META,
                   PROTOCOLO, PROTOCOLO_NOTA)

NAVY = "#0A1D5C"; INK = "#111827"; SUB = "#6B7280"; MUTE = "#9CA3AF"
HAIR = "#E5E7EB"; RULE = "#111827"; BLUE = "#1A56DB"
RED = "#B91C1C"; AMBER = "#B45309"
SANS = "Arial, Helvetica, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
W = 760

# cor so para excecao
TAG = {
    "Atrasado":     ("#FFFFFF", RED,       RED),
    "Em atenção":   ("#FFFFFF", AMBER,     AMBER),
    "Em andamento": (INK,       "#FFFFFF", "#D1D5DB"),
    "Não iniciado": (MUTE,      "#FFFFFF", HAIR),
    "Concluído":    ("#FFFFFF", NAVY,      NAVY),
}

TITULO = ("Piloto de jan/27 mantido, mas a Política Comercial (13/10) pode sair parcial; "
          "precisamos de 1 escalonamento e 3 decisões até 16/10")

ACAO = {
    "decisoes": "Quatro definições até 16/10 protegem as entregas de outubro",
    "timeline": "Duas das seis entregas estão em atenção, ambas por dependências ainda não resolvidas",
    "entregas": "Cada entrega tem um critério objetivo de conclusão, contra o qual reportaremos avanço",
    "avancos": "As definições da semana tiram a nova ferramenta do caminho crítico do piloto",
    "pendencias": "Uma dependência vencida desde 23/09 concentra o principal risco do projeto",
    "protocolo": "O protocolo do piloto passa a ser entrega própria; 1 de 8 componentes em andamento",
}

# linha do tempo: semanas (segunda-feira) e posicao das entregas
SEMANAS = ["28/09", "05/10", "12/10", "19/10", "26/10", "02/11", "09/11", "16/11", "23/11", "30/11"]
TIMELINE = [  # (rotulo, nota, indice da semana de entrega, status, data)
    ("1. Política Comercial", "dependência vencida 23/09", 2, "Em atenção", "13/10"),
    ("2. Economia dos Canais", "", 2, "Em andamento", "14/10"),
    ("3. Banda, RTP e shopper", "", 3, "Em andamento", "21/10"),
    ("5. Business Case <i>ex ante</i>", "base de clientes sem dono", 4, "Em atenção", "30/10"),
    ("4. Governança", "", 5, "Em andamento", "06/11"),
    ("5.1 Protocolo do Piloto", "v0 30/10*", 9, "Não iniciado", "30/11"),
    ("5.1 Piloto: campo e dados", "", 9, "Em andamento", "30/11"),
]
MARCOS_DECISAO = {1: "09/10", 2: "16/10"}  # semana -> data das decisoes


def tag(s, size=10.5):
    fg, bg, bd = TAG[s]
    return (f'<span style="display:inline-block;padding:2px 8px;border:1px solid {bd};background:{bg};'
            f'color:{fg};border-radius:3px;font-family:{SANS};font-size:{size}px;font-weight:700;'
            f'letter-spacing:.2px;white-space:nowrap">{s}</span>')


def td(c, w=None, align="left", pad="9px 10px 9px 0", size=12.5, color=INK, top=True, extra=""):
    wa = f' width="{w}"' if w else ""
    b = f"border-top:1px solid {HAIR};" if top else ""
    return (f'<td valign="top" align="{align}"{wa} style="padding:{pad};{b}font-family:{SANS};'
            f'font-size:{size}px;line-height:1.45;color:{color};{extra}">{c}</td>')


def th(cells, widths):
    return "<tr>" + "".join(
        f'<td width="{w}" style="padding:0 10px 6px 0;border-bottom:1.5px solid {RULE};font-family:{SANS};'
        f'font-size:10px;font-weight:700;color:{INK};letter-spacing:.3px">{c}</td>'
        for c, w in zip(cells, widths)) + "</tr>"


def tbl(inner):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{inner}</table>'


def secao(n, kicker, acao, body, nota=""):
    nt = (f'<p style="margin:10px 0 0 0;font-family:{SANS};font-size:10.5px;line-height:1.5;color:{MUTE}">'
          f'{nota}</p>') if nota else ""
    return (f'<tr><td style="padding:34px 40px 0 40px">'
            f'<p style="margin:0 0 6px 0;font-family:{SANS};font-size:10.5px;font-weight:700;letter-spacing:1.4px;'
            f'color:{BLUE}">{n} &nbsp;{kicker.upper()}</p>'
            f'<p style="margin:0 0 16px 0;font-family:{SERIF};font-size:19px;line-height:1.3;color:{INK}">{acao}</p>'
            f'{body}{nt}</td></tr>')


def small(t, color=SUB):
    return f'<span style="font-size:11.5px;color:{color}">{t}</span>'


def timeline():
    lw, cw = 190, 50
    hdr = (f'<td width="{lw}" style="padding:0 0 6px 0;border-bottom:1.5px solid {RULE}"></td>' + "".join(
        f'<td width="{cw}" align="center" style="padding:0 0 6px 0;border-bottom:1.5px solid {RULE};'
        f'font-family:{SANS};font-size:9.5px;font-weight:700;color:{INK if i else BLUE}">'
        f'{"Hoje" if i == 0 else s}</td>' for i, s in enumerate(SEMANAS)))
    out = [f"<tr>{hdr}</tr>"]

    def cell(inner, i, last=False):
        today = f"border-left:2px solid {BLUE};" if i == 0 else ""
        return (f'<td width="{cw}" align="center" valign="middle" style="padding:8px 0;{today}'
                f'border-bottom:1px solid {HAIR}">{inner}</td>')

    for rot, nota, due, s, data in TIMELINE:
        cor = {"Em atenção": AMBER, "Atrasado": RED}.get(s, NAVY if s == "Em andamento" else MUTE)
        bar = f'<div style="height:6px;background:{"#FDE7C7" if cor == AMBER else "#E5E7EB"};font-size:0">&nbsp;</div>'
        cells = []
        for i in range(len(SEMANAS)):
            if i < due:
                cells.append(cell(bar, i))
            elif i == due:
                cells.append(cell(f'<span style="font-family:{SANS};font-size:14px;color:{cor}">&#9670;</span>'
                                  f'<br><span style="font-family:{SANS};font-size:9.5px;font-weight:700;'
                                  f'color:{cor}">{data}</span>', i))
            else:
                cells.append(cell("&nbsp;", i))
        nt = f'<br><span style="font-size:10.5px;color:{cor if cor in (AMBER, RED) else MUTE}">{nota}</span>' if nota else ""
        out.append(f'<tr><td width="{lw}" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {HAIR};'
                   f'font-family:{SANS};font-size:12px;color:{INK}"><b>{rot}</b>{nt}</td>{"".join(cells)}</tr>')
    # linha de decisoes
    cells = []
    for i in range(len(SEMANAS)):
        inner = (f'<span style="font-family:{SANS};font-size:12px;color:{RED}">&#9650;</span><br>'
                 f'<span style="font-family:{SANS};font-size:9.5px;font-weight:700;color:{RED}">{MARCOS_DECISAO[i]}</span>'
                 if i in MARCOS_DECISAO else "&nbsp;")
        cells.append(cell(inner, i))
    out.append(f'<tr><td width="{lw}" valign="middle" style="padding:8px 8px 8px 0;border-bottom:1px solid {HAIR};'
               f'font-family:{SANS};font-size:12px;color:{RED}"><b>Decisões necessárias</b></td>{"".join(cells)}</tr>')
    legenda = (f'<p style="margin:8px 0 0 0;font-family:{SANS};font-size:10.5px;color:{SUB}">'
               f'<span style="color:{NAVY}">&#9670;</span> entrega no prazo &nbsp;&nbsp;'
               f'<span style="color:{AMBER}">&#9670;</span> entrega em atenção &nbsp;&nbsp;'
               f'<span style="color:{MUTE}">&#9670;</span> não iniciada &nbsp;&nbsp;'
               f'<span style="color:{RED}">&#9650;</span> decisão / escalonamento</p>')
    return tbl("".join(out)) + legenda


def build():
    o = []
    # faixa superior fina
    o.append(
        f'<tr><td style="padding:28px 40px 0 40px">' + tbl(
            f'<tr><td style="padding-bottom:10px;border-bottom:3px solid {NAVY};font-family:{SANS};font-size:11px;'
            f'color:{INK}"><b style="color:{NAVY}">DOC</b> Consulting &nbsp;<span style="color:{MUTE}">|</span>&nbsp; '
            f'Status Report Semanal {META["numero"]}</td>'
            f'<td align="right" style="padding-bottom:10px;border-bottom:3px solid {NAVY};font-family:{SANS};'
            f'font-size:11px;color:{SUB}">{META["titulo"]} &nbsp;·&nbsp; {META["data"]}</td></tr>') + '</td></tr>')

    # titulo-resposta
    o.append(f'<tr><td style="padding:26px 40px 0 40px"><p style="margin:0;font-family:{SERIF};font-size:27px;'
             f'line-height:1.25;color:{INK}">{TITULO}</p></td></tr>')

    # tres numeros
    n_at = sum(1 for e in ENTREGAS if e[2] == "Em atenção")
    n_ok = sum(1 for e in ENTREGAS if e[2] == "Em andamento")
    n_ni = sum(1 for e in ENTREGAS if e[2] == "Não iniciado")
    kpis = [
        ("Saúde do projeto", f'<span style="color:{AMBER}">Em atenção</span>', "piloto jan/27 mantido"),
        ("Entregas", f'<span style="color:{AMBER}">{n_at}</span> <span style="font-size:15px;color:{SUB}">em atenção</span>',
         f"{n_ok} no prazo · {n_ni} não iniciada"),
        ("Ações necessárias", f'<span style="color:{RED}">4</span> <span style="font-size:15px;color:{SUB}">até 16/10</span>',
         "1 escalonamento · 3 decisões"),
    ]
    cells = "".join(
        f'<td width="33%" valign="top" style="padding:14px 16px 0 {0 if i == 0 else 16}px;'
        f'{"border-left:1px solid " + HAIR + ";" if i else ""}font-family:{SANS}">'
        f'<div style="font-size:10px;font-weight:700;letter-spacing:1px;color:{SUB}">{k.upper()}</div>'
        f'<div style="font-family:{SERIF};font-size:24px;line-height:1.3;margin-top:4px">{v}</div>'
        f'<div style="font-size:11.5px;color:{SUB}">{s}</div></td>' for i, (k, v, s) in enumerate(kpis))
    o.append(f'<tr><td style="padding:20px 40px 0 40px">' + tbl(
        f'<tr><td colspan="3" style="border-top:1px solid {HAIR};font-size:0">&nbsp;</td></tr><tr>{cells}</tr>')
        + '</td></tr>')

    # 1 decisoes
    ws = [26, 400, 160, 60]
    rows = "".join(
        "<tr>" + td(f'<span style="font-family:{SERIF};font-size:18px;color:{RED if t == "Escalonamento" else NAVY}">{i + 1}</span>', ws[0])
        + td(f'<span style="font-size:10px;font-weight:700;letter-spacing:.8px;color:{RED if t == "Escalonamento" else SUB}">'
             f'{t.upper()}</span><br><b>{q}</b><br>{small(why)}', ws[1])
        + td(quem, ws[2]) + td(f"<b>{ate}</b>", ws[3], align="right", pad="9px 0") + "</tr>"
        for i, (t, q, why, quem, ate) in enumerate(DECISOES))
    o.append(secao("1", "Decisões necessárias / escalonamentos", ACAO["decisoes"],
                   tbl(th(["", "O que precisamos", "De quem", "Até"], ws) + rows)))

    # 2 timeline
    o.append(secao("2", "Exhibit · linha do tempo das entregas", ACAO["timeline"], timeline()))

    # 3 entregas
    ws = [170, 64, 96, 366]
    rows = "".join(
        "<tr>" + td(f"<b>{n}</b>", ws[0]) + td(p, ws[1]) + td(tag(s), ws[2])
        + td(f"{why}<br>{small('Concluída quando: ' + c)}", ws[3], pad="9px 0") + "</tr>"
        for n, p, s, why, c in ENTREGAS)
    o.append(secao("3", "Entregas e critério de conclusão", ACAO["entregas"],
                   tbl(th(["Entrega", "Prazo", "Status", "Situação e critério de conclusão"], ws) + rows)))

    # 4 avancos
    ws = [300, 396]
    rows = "".join("<tr>" + td(f"<b>{r}</b>", ws[0]) + td(i, ws[1], color=SUB, pad="9px 0") + "</tr>"
                   for r, i in AVANCOS)
    o.append(secao("4", "Avanços do ciclo", ACAO["avancos"],
                   tbl(th(["O que foi decidido ou validado", "Implicação para o projeto"], ws) + rows),
                   f"Em curso, sem resultado ainda: {EM_CURSO}"))

    # 5 pendencias
    ws = [196, 110, 100, 200, 90]
    rows = "".join(
        "<tr>" + td(f'<b>{x["o_que"]}</b><br>{small(x["quem"])}', ws[0]) + td(x["prazo"], ws[1])
        + td(x["entrega"], ws[2]) + td(f'{x["impacto"]}<br>{small("→ " + x["acao"], INK)}', ws[3])
        + td(tag(x["status"]), ws[4], align="right", pad="9px 0") + "</tr>" for x in CRITICAS)
    body = tbl(th(["Pendência / de quem", "Prazo orig. → atual", "Impacta", "Impacto e próxima ação", ""], ws) + rows)
    ws2 = [300, 170, 80, 146]
    rows2 = "".join("<tr>" + "".join(td(c, w, size=11.5, pad="6px 10px 6px 0") for c, w in zip(r, ws2)) + "</tr>"
                    for r in EM_DIA)
    body += (f'<p style="margin:22px 0 8px 0;font-family:{SANS};font-size:10.5px;font-weight:700;color:{SUB}">'
             f'Em dia, prazo original mantido</p>' + tbl(th(["Pendência", "De quem", "Prazo", "Impacta"], ws2) + rows2))
    o.append(secao("5", "Pendências e dependências", ACAO["pendencias"], body))

    # 6 protocolo
    nomes = "".join(
        f'<td width="12.5%" align="center" valign="bottom" style="padding:10px 4px 8px 4px;border-top:1.5px solid {RULE};'
        f'font-family:{SANS};font-size:11px;line-height:1.3;color:{INK}"><b>{c}</b></td>' for c, _ in PROTOCOLO)
    tags = "".join(f'<td align="center" style="padding:0 4px 10px 4px">{tag(s, 9.5)}</td>' for _, s in PROTOCOLO)
    o.append(secao("6", "Protocolo do piloto · evolução semanal", ACAO["protocolo"],
                   tbl(f"<tr>{nomes}</tr><tr>{tags}</tr>"), PROTOCOLO_NOTA))

    # anexo: cronograma
    ws = [200, 70, 82, 96, 150, 98]
    rows = []
    for frente, ativs in CRONOGRAMA:
        rows.append(f'<tr><td colspan="6" style="padding:14px 0 4px 0;font-family:{SANS};font-size:11.5px;'
                    f'font-weight:700;color:{NAVY}">{frente}</td></tr>')
        for a, ow, pz, s, dep, mk in ativs:
            rows.append("<tr>" + "".join(td(c, w, size=11.5, pad="6px 8px 6px 0")
                                         for c, w in zip([a, ow, pz, tag(s, 9.5), dep, mk], ws)) + "</tr>")
    o.append(secao("A", "Anexo · cronograma por frente", "Atividades por frente, com dono, status e próximo marco",
                   tbl(th(["Atividade", "Owner", "Prazo", "Status", "Dependência / bloqueio", "Próximo marco"], ws)
                       + "".join(rows)),
                   "Status: Não iniciado (início futuro) · Em andamento (dependências em dia) · Em atenção (dependência "
                   "pendente, sem dono ou fora de sequência) · Atrasado (prazo ou dependência vencida que compromete a "
                   "data) · Concluído (critério atendido e validado). A entrega herda o pior status das suas "
                   "dependências. * Data proposta pela DOC, a confirmar com a PremieRpet."))

    o.append(f'<tr><td style="padding:36px 40px 32px 40px">' + tbl(
        f'<tr><td style="border-top:1px solid {HAIR};padding-top:12px;font-family:{SANS};font-size:10px;color:{MUTE}">'
        f'DOC Consulting | Status report semanal</td><td align="right" style="border-top:1px solid {HAIR};'
        f'padding-top:12px;font-family:{SANS};font-size:10px;color:{MUTE}">© 2026 DOC Consulting</td></tr>')
        + '</td></tr>')

    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Status Report #2 – PremieRpet</title></head>'
            '<body style="margin:0;padding:0;background:#FFFFFF">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">'
            f'<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" style="width:{W}px;max-width:100%">'
            + "".join(o) + '</table></td></tr></table></body></html>')


if __name__ == "__main__":
    dst = Path(__file__).with_name("status-report-02-premierpet-executivo.html")
    dst.write_text(build(), encoding="utf-8")
    print(f"ok -> {dst}")

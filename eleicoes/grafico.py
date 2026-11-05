"""Compara a evolução da apuração do 1º turno: 2022 x 2026.
Uso: python grafico.py   (lê dados_2022.csv e dados_2026.csv; gera comparacao_2022_2026.png)
Colunas: pct_secoes (% das seções totalizadas), hora, lula, bolsonaro (% dos votos válidos).
Em 2026 a coluna 'bolsonaro' é o candidato do campo bolsonarista (Flávio Bolsonaro)."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d22, d26 = pd.read_csv("dados_2022.csv"), pd.read_csv("dados_2026.csv")
VERM, AZUL = "#B5173A", "#1F4E8C"
fig, ax = plt.subplots(figsize=(13, 7), dpi=150)
for d, ano, ls, a, lw in [(d22, 2022, "--", .55, 2), (d26, 2026, "-", 1, 3)]:
    if d.empty: continue
    ax.plot(d.pct_secoes, d.lula, ls, color=VERM, alpha=a, lw=lw, marker="o", ms=5, label=f"Lula {ano}")
    ax.plot(d.pct_secoes, d.bolsonaro, ls, color=AZUL, alpha=a, lw=lw, marker="o", ms=5,
            label=f"{'Bolsonaro' if ano == 2022 else 'Flávio Bolsonaro'} {ano}")
    ax.annotate(f"{d.lula.iloc[-1]:.2f}%".replace(".", ","), (d.pct_secoes.iloc[-1], d.lula.iloc[-1]),
                xytext=(6, 0), textcoords="offset points", fontsize=9, color="#333", va="center")
    ax.annotate(f"{d.bolsonaro.iloc[-1]:.2f}%".replace(".", ","), (d.pct_secoes.iloc[-1], d.bolsonaro.iloc[-1]),
                xytext=(6, 0), textcoords="offset points", fontsize=9, color="#333", va="center")
ax.set_xlim(0, 104); ax.set_ylim(35, 53)
ax.set_xlabel("% das seções totalizadas"); ax.set_ylabel("% dos votos válidos")
ax.set_title("1º turno: evolução da apuração, 2022 x 2026", loc="left", fontweight="bold", fontsize=14)
ax.axhline(50, color="#999", lw=1, ls=":"); ax.text(60, 50.15, "50% (vence no 1º turno)", fontsize=8, color="#777")
ax.grid(alpha=.25); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="lower right", ncol=2)
if d26.empty:
    ax.text(.5, .5, "Dados de 2026 ainda não preenchidos\n(dados_2026.csv)", transform=ax.transAxes,
            ha="center", color="#888", fontsize=14)
fig.text(.01, .005, "Fonte: parciais do TSE. 2022: Bloomberg Línea (02/10/2022). 2026: InfoMoney, Agenda do Poder, Mix Vale, Latin Times (04/10/2026), apuração em andamento.", fontsize=8, color="#777")
fig.tight_layout(); fig.savefig("comparacao_2022_2026.png")

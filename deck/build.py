"""Gera project/deck.json e project/slides/*.html (formato do tipo Slides) e preview/*.html para conferência local."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from slides_a import SLIDES_A
try:
    from slides_b import SLIDES_B
except ImportError:
    SLIDES_B = []
try:
    from annex import SLIDES_C
except ImportError:
    SLIDES_C = []

ROOT = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(ROOT, "project", "slides")
PV = os.path.join(ROOT, "preview")
os.makedirs(SL, exist_ok=True); os.makedirs(PV, exist_ok=True)

order = []
for fn in SLIDES_A + SLIDES_B + SLIDES_C:
    html = fn()
    sid = fn.__name__
    order.append(sid)
    with open(os.path.join(SL, sid + ".html"), "w") as f:
        f.write(html)
    with open(os.path.join(PV, sid + ".html"), "w") as f:
        f.write('<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0;box-sizing:border-box}'
                'body{width:1920px;height:1080px;overflow:hidden}section{position:relative;width:1920px;height:1080px;overflow:hidden}'
                'aside{display:none}</style></head><body>' + html + '</body></html>')

sections = {
    "abertura": {"description": "Abertura: capa, sumário e fundamentos dos dados.", "start": "s01"},
    "etapa1": {"description": "Etapa 1, a base recebida: sell-out em todas as redes e o Atacadão por loja.", "start": "s04"},
    "etapa2": {"description": "Etapa 2, por que a regressão direta não conclui.", "start": "s06"},
    "etapa3": {"description": "Etapa 3, o tratamento: agrupamento nacional em 10 faixas.", "start": "s09"},
    "etapa4": {"description": "Etapa 4, a sensibilidade e o grau de confiança.", "start": "s10"},
    "etapa5": {"description": "Etapa 5, a pergunta de negócio: volume, margem e decisão.", "start": "s13"},
    "encerramento": {"description": "Encerramento: o que aprovar hoje.", "start": "s17"},
    "anexo": {"description": "Anexo: faixas, robustez, recortes, fórmulas, sell-through e bases.", "start": "a1"},
}
sections = {k: v for k, v in sections.items() if v["start"] in order}
deck = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-02T12:00:00Z"}, "lists": "css",
        "title": "Preço, volume e margem · Nadir", "order": order, "sections": sections, "faces": {}, "designSystems": []}
with open(os.path.join(ROOT, "project", "deck.json"), "w") as f:
    json.dump(deck, f, ensure_ascii=False, indent=1)
print(len(order), "slides:", " ".join(order))

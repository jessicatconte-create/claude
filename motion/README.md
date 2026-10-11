# Motion studio

Estúdio de motion design renderizado por código, no padrão "route A" do
artigo do @0xMovez: o modelo escreve um programa, não um vídeo.

```
index.html (seek(t))  →  Chromium headless (Playwright)  →  frames  →  ffmpeg  →  MP4
timeline.js (BPM, shots) ─┬─ imagem
                          └─ audio.mjs (synth no mesmo grid) → WAV → mux
```

## Rodar

```bash
cd motion
npm install                      # só o Playwright (usa o Chromium já instalado)
npm run demo                     # out/demo/demo_1920x1080.mp4 com áudio
npm run demo:vertical            # 1080x1920 da mesma timeline
npm run demo:sheet               # folha de contato para crítica
node render.mjs scenes/demo --stills 0.5,3,8   # frames específicos
node render.mjs scenes/demo --draft            # preview rápido
```

Para ver no navegador com scrub, sirva a pasta (`npx serve .`) e abra
`scenes/demo/index.html` sem parâmetros: clique para pausar e use o slider.

Precisa de `ffmpeg` no PATH.

## Estrutura

| Arquivo | O que faz |
|---|---|
| `render.mjs` | Servidor local + Playwright + ffmpeg. Modos: vídeo, `--stills`, `--sheet`, `--draft`, `--size`, `--from/--to` |
| `lib/motion.js` | Springs de forma fechada (`snappy`, `default`, `heavy`, `playful`), `track()`, `beatGrid()`, `sequence()`, `rng()`, `layout()` |
| `lib/audio.mjs` | Synth sem dependências: kick, hat, clap, pad, pluck, whoosh, impact → WAV |
| `scenes/demo/` | Exemplo de 10 s a 120 BPM: tipografia cinética, uma forma que vira botão → loader → player → card guiada por cursor, grade de pontos no beat, gráfico com springs, lockup em loop |
| `CLAUDE.md` | Regras da casa que o Claude Code lê em toda execução |
| `../.claude/skills/motion-reel/` | Skill `/motion-reel for <URL>, 20s, vertical` que roda o pipeline inteiro |

## Usando com o Claude Code

```
/motion-reel for https://seuproduto.com, 20s, vertical, reference ./motion/refs/frame.png
```

A skill faz brief → referência → plano → build → som → loop de crítica
(o Claude olha os próprios frames e corrige até nota 8+) → render em todos os formatos.

Dicas do artigo: use esforço `xhigh` para filmes novos, `max` quando os primeiros
3 s precisam carregar um lançamento, `medium` para ajustes. Dê uma referência
(frame, vídeo ou pasta), senão o resultado cai no padrão "texto centralizado em
gradiente com fade".

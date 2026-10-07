# PremieRpet · 3 Camadas — rebranding

`PremieRpet_3_Camadas_v15_rebrand.pptx` é a `PremieRpet_3_Camadas_v14` com o branding da
`[PremieRpet] Piloto [Revisão] v2 - 29-09-2026`:

- fundo cinza-claro `F5F5F3`, cards brancos arredondados com borda `E5E7EB`;
- logos PremieRpet | DOC Consulting no canto superior direito (versão branca na capa e no divisor);
- títulos em Arial bold tinta `14171F`, subtítulos em itálico `888D97`, sem filete sob o título;
- rodapé com fonte em `888D97` e "Página NN" à direita;
- cabeçalhos de tabela no estilo da referência (texto cinza, sem faixa navy, filete `D1D5DB`);
- família navy → rampa de azul royal da referência (`1A56DB` / `7BA0EA` / `C3D3F5`), inclusive
  nos gráficos em imagem; o laranja PremieRpet foi mantido como cor de destaque;
- capa e divisor do Apêndice com o gradiente navy da referência;
- slide 3 ("Objetivo da reunião") reconstruído como tabela nativa (era um print de planilha).

Para regerar (com os dois decks descompactados):

```bash
python3 tools/rebrand.py <3_camadas_unpacked> <piloto_unpacked>
```

# FIAP — Faculdade de Informática e Administração Paulista

![FIAP](../../assets/logo-fiap.png)

# ReciclaBairro

## Nome do grupo

[Preencher] · Turma [preencher]

## Integrantes

- Camila - RM 569629
- João - RM 571052
- Lucas - RM 569580
- Gabriel - RM 569179
- Darlyton - RM 572143

## Professores

- Tutor(a) — [preencher]
- Coordenador — André Godoi Chiovato

## Descrição

POC CitizenTech para recomendar pontos de descarte por material, bairro e atendimento aos sábados. Os dados são fictícios. O projeto se relaciona à meta 12.5 do ODS 12.

## Estrutura de pastas

- `data/` — catálogo CSV simulado.
- `src/` — interface Streamlit e recomendador SQLite.
- `tests/` — testes das regras, dos dados e da interface.
- `docs/` — roteiro da demonstração.

## Links e observações

- Vídeo demonstrativo — [inserir link não listado].
- GitHub — [inserir URL privada com acesso para fiap-tutoria].
- Participação na competição — [confirmar com o grupo].

### Decisões técnicas

O recomendador baseado em conhecimento aplica restrições de material e horário, depois prioriza o bairro escolhido. As regras são verificáveis sem histórico de usuários. Empates são ordenados por nome e ID. O CSV alimenta um SQLite em memória. A interface dispensa cadastro e geolocalização.

## Como executar o código

Abra esta pasta no terminal. Ambiente usado nos testes: Python 3.13 e Streamlit 1.57.0.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run src/app.py
```

No Windows, também é possível abrir `INICIAR.bat` com Python instalado. Para rodar os testes:

```powershell
python -m unittest discover -s tests -v
```

## Licença

Estrutura adaptada do [template da FIAP](https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI), sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

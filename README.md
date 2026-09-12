# Trabalho 2 — Matemática Computacional

Análise estatística de uma base sintética de clientes (800 registros), com
estatísticas descritivas, correlação, detecção de outliers pelo método IQR
e visualização de dados.

## Estrutura do projeto

```
math_computacional/
├── src/
│   ├── codigo.py        # leitura, tratamento, estatísticas, correlação e IQR
│   └── graficos.py       # visualização (barras, pizza, boxplot, heatmap)
├── data/
│   └── dados_sinteticos.csv
├── outputs/
│   └── graficos/          # PNGs gerados por graficos.py (300 dpi)
├── tests/
│   └── test_codigo.py
├── requirements.txt
└── README.md
```

## Divisão do grupo

- **José Paulo** — leitura da base, tratamento, estatísticas obrigatórias,
  métricas extras, correlação, IQR e módulo automático de outliers
  (`src/codigo.py`).
- **Victor Seixas** — visualização dos dados com Matplotlib e Seaborn
  (`src/graficos.py`).
- **Ana Clara** — coleta/contextualização dos dados, dicionário de dados e
  construção dos slides.
- **José Iderlan** — análise crítica, interpretação dos resultados e
  redação do relatório em PDF.

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Estatísticas, correlação e outliers (José Paulo):

```bash
python -m src.codigo
```

Gráficos para relatório e slides (Victor Seixas):

```bash
python -m src.graficos
```

Os PNGs são gerados em `outputs/graficos/`.

Testes:

```bash
python -m unittest discover -v
```

## Uso programático

```python
from src.codigo import executar_analise

resultado = executar_analise("data/dados_sinteticos.csv")
print(resultado["estatisticas"])
print(resultado["outliers"])
```

As chaves retornadas são `dados_brutos`, `dados_tratados`, `estatisticas`,
`outliers`, `correlacao` e `dados_filtrados`.

A base `data/dados_sinteticos.csv` tem 800 registros e foi gerada de forma
reprodutível, com três registros extremos intencionais para a demonstração
do módulo de outliers.

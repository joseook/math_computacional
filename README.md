# Trabalho 2 — Matemática Computacional

Análise estatística de uma base de dados reais do mercado imobiliário brasileiro (>500 registros), com estatísticas descritivas, correlação, detecção de outliers pelo método IQR e visualização de dados.

## Contextualização e Fonte de Dados

- **Tema:** Análise de preços de imóveis no Brasil.
- **Problema Investigado:** Como características físicas (área) e localização influenciam o preço final de venda das propriedades, e qual o impacto dos valores atípicos (outliers) nas estatísticas de mercado.
- **Fonte dos Dados:** Kaggle (Brasil real estate Data)[cite: 1].
- **Dimensão da Base:** Mais de 500 registros e 8 colunas[cite: 1].

## Dicionário de Dados

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Numérico | Identificador único do registro do imóvel. |
| `property_type` | Categórico | Tipo da propriedade (ex: apartamento, casa). |
| `state` | Categórico | Estado brasileiro onde o imóvel está localizado. |
| `region` | Categórico | Cidade, bairro ou região específica do estado. |
| `lat` | Numérico | Latitude (coordenada geográfica). |
| `lon` | Numérico | Longitude (coordenada geográfica). |
| `area_m2` | Numérico | Área total do imóvel em metros quadrados. |
| `price_brl` | Numérico | Preço do imóvel em Reais (R$). |

## Estrutura do projeto

```text
math_computacional/
├── src/
│   ├── codigo.py        # leitura, tratamento, estatísticas, correlação e IQR
│   └── graficos.py       # visualização (barras, pizza, boxplot, heatmap)
├── data/
│   └── dados.csv        # Base de dados reais (Imóveis Brasil)
├── outputs/
│   └── graficos/          # PNGs gerados por graficos.py (300 dpi)
├── tests/
│   └── test_codigo.py
├── requirements.txt
└── README.md
```
## Divisão do grupo

- **José Paulo** — leitura da base, tratamento, estatísticas obrigatórias, métricas extras, correlação, IQR e módulo automático de outliers (src/codigo.py).
- **Victor Seixas** — visualização dos dados com Matplotlib e Seaborn (src/graficos.py).
- **Ana Clara** — coleta/contextualização dos dados reais, dicionário de dados e construção dos slides.
- **José Iderlan** — análise crítica, interpretação dos resultados e redação do relatório em PDF.

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

Os PNGs são gerados em outputs/graficos/.

Testes:

```bash
python -m unittest discover -v
```

Uso programático
```python
from src.codigo import executar_analise

resultado = executar_analise("data/dados.csv")
print(resultado["estatisticas"])
print(resultado["outliers"])
```

As chaves retornadas são `dados_brutos`, `dados_tratados`, `estatisticas`, `outliers`, `correlacao` e `dados_filtrados`.

A base `data/dados.csv` reflete dados do mercado real com mais de 500 registros, garantindo a viabilidade para a demonstração do módulo de outliers e análises estatísticas exigidas no edital.

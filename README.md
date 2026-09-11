# Trabalho 2 — Matemática Computacional

## Parte do José Paulo

Este diretório contém o núcleo em Python/Pandas para:

- leitura de CSV e XLSX;
- tratamento de duplicatas e valores ausentes;
- média, mediana, moda, amplitude e quartis;
- desvio padrão, variância, correlação e IQR;
- cálculo dos limites inferior/superior e filtragem de outliers pelo IQR.

A base `dados_sinteticos.csv` tem 800 registros e foi gerada de forma reprodutível,
com três registros extremos intencionais para a demonstração do módulo de outliers.

## Como executar

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python codigo.py
```

Para validar as funções:

```bash
.venv/bin/python -m unittest discover -v
```

O módulo pode ser importado pelo restante do grupo:

```python
from codigo import executar_analise

resultado = executar_analise("dados_sinteticos.csv")
print(resultado["estatisticas"])
print(resultado["outliers"])
```

As chaves retornadas são `dados_brutos`, `dados_tratados`, `estatisticas`,
`outliers`, `correlacao` e `dados_filtrados`.

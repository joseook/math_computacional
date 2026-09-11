"""Núcleo da análise estatística do Trabalho 2.

Este módulo concentra leitura, tratamento, estatísticas descritivas e
detecção/remoção de outliers pelo método do intervalo interquartil (IQR).
"""

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


COLUNAS_NUMERICAS_PADRAO = [
    "idade",
    "renda_mensal",
    "gastos_mensais",
    "satisfacao",
]


def carregar_dados(caminho: str | Path) -> pd.DataFrame:
    """Lê um arquivo CSV ou XLSX e devolve um DataFrame."""
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    extensao = caminho.suffix.lower()
    if extensao == ".csv":
        return pd.read_csv(caminho)
    if extensao in {".xlsx", ".xls"}:
        return pd.read_excel(caminho)
    raise ValueError("Formato não suportado. Use .csv, .xlsx ou .xls.")


def tratar_dados(
    dados: pd.DataFrame,
    colunas_numericas: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Remove duplicatas, converte números e preenche ausências pela mediana."""
    tratados = dados.copy()
    tratados = tratados.drop_duplicates().reset_index(drop=True)

    colunas_numericas = list(colunas_numericas or COLUNAS_NUMERICAS_PADRAO)
    colunas_numericas = [coluna for coluna in colunas_numericas if coluna in tratados]
    for coluna in colunas_numericas:
        tratados[coluna] = pd.to_numeric(tratados[coluna], errors="coerce")
        if tratados[coluna].isna().any():
            mediana = tratados[coluna].median()
            tratados[coluna] = tratados[coluna].fillna(mediana)

    return tratados


def _validar_colunas_numericas(
    dados: pd.DataFrame, colunas: Iterable[str]
) -> list[str]:
    colunas = list(colunas)
    ausentes = [coluna for coluna in colunas if coluna not in dados.columns]
    if ausentes:
        raise KeyError(f"Colunas não encontradas: {', '.join(ausentes)}")
    nao_numericas = [coluna for coluna in colunas if not pd.api.types.is_numeric_dtype(dados[coluna])]
    if nao_numericas:
        raise TypeError(f"As colunas precisam ser numéricas: {', '.join(nao_numericas)}")
    return colunas


def calcular_estatisticas(
    dados: pd.DataFrame, colunas_numericas: Iterable[str]
) -> pd.DataFrame:
    """Calcula estatísticas obrigatórias e métricas extras por coluna."""
    colunas = _validar_colunas_numericas(dados, colunas_numericas)
    resultados = {}

    for coluna in colunas:
        serie = dados[coluna].dropna()
        modas = serie.mode()
        resultados[coluna] = {
            "contagem": int(serie.count()),
            "media": float(serie.mean()),
            "mediana": float(serie.median()),
            "moda": float(modas.iloc[0]) if not modas.empty else np.nan,
            "minimo": float(serie.min()),
            "maximo": float(serie.max()),
            "amplitude": float(serie.max() - serie.min()),
            "q1": float(serie.quantile(0.25)),
            "q3": float(serie.quantile(0.75)),
            "desvio_padrao": float(serie.std()),
            "variancia": float(serie.var()),
            "iqr": float(serie.quantile(0.75) - serie.quantile(0.25)),
        }

    return pd.DataFrame.from_dict(resultados, orient="index")


def calcular_correlacao(
    dados: pd.DataFrame, colunas_numericas: Iterable[str]
) -> pd.DataFrame:
    """Retorna a matriz de correlação de Pearson das colunas selecionadas."""
    colunas = _validar_colunas_numericas(dados, colunas_numericas)
    return dados[colunas].corr(method="pearson")


def calcular_outliers(
    dados: pd.DataFrame, colunas_numericas: Iterable[str]
) -> pd.DataFrame:
    """Calcula Q1, Q3, IQR, limites e quantidade de outliers pelo método IQR."""
    colunas = _validar_colunas_numericas(dados, colunas_numericas)
    resultados = {}

    for coluna in colunas:
        serie = dados[coluna].dropna()
        q1 = float(serie.quantile(0.25))
        q3 = float(serie.quantile(0.75))
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        mascara = (dados[coluna] < limite_inferior) | (dados[coluna] > limite_superior)
        resultados[coluna] = {
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior,
            "quantidade_outliers": int(mascara.sum()),
            "percentual_outliers": float(mascara.mean() * 100),
        }

    return pd.DataFrame.from_dict(resultados, orient="index")


def filtrar_outliers(
    dados: pd.DataFrame,
    resumo_outliers: pd.DataFrame,
) -> pd.DataFrame:
    """Remove linhas que sejam atípicas em pelo menos uma coluna numérica."""
    mascara_outlier = pd.Series(False, index=dados.index)
    for coluna in resumo_outliers.index:
        if coluna not in dados.columns:
            raise KeyError(f"Coluna do resumo não encontrada nos dados: {coluna}")
        limites = resumo_outliers.loc[coluna]
        mascara_outlier |= (dados[coluna] < limites["limite_inferior"]) | (
            dados[coluna] > limites["limite_superior"]
        )
    return dados.loc[~mascara_outlier].reset_index(drop=True)


def executar_analise(
    caminho: str | Path,
    colunas_numericas: Iterable[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Executa o fluxo completo e devolve resultados para relatório/gráficos."""
    colunas = list(colunas_numericas or COLUNAS_NUMERICAS_PADRAO)
    dados_brutos = carregar_dados(caminho)
    dados_tratados = tratar_dados(dados_brutos, colunas)
    estatisticas = calcular_estatisticas(dados_tratados, colunas)
    outliers = calcular_outliers(dados_tratados, colunas)
    dados_filtrados = filtrar_outliers(dados_tratados, outliers)
    return {
        "dados_brutos": dados_brutos,
        "dados_tratados": dados_tratados,
        "estatisticas": estatisticas,
        "outliers": outliers,
        "correlacao": calcular_correlacao(dados_tratados, colunas),
        "dados_filtrados": dados_filtrados,
    }


def gerar_dados_sinteticos(
    quantidade: int = 800, semente: int = 42
) -> pd.DataFrame:
    """Gera uma base sintética reprodutível para o trabalho acadêmico."""
    if quantidade < 1:
        raise ValueError("A quantidade de registros deve ser positiva.")

    rng = np.random.default_rng(semente)
    regioes = np.array(["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])
    categorias = np.array(["Básico", "Intermediário", "Premium"])
    dados = pd.DataFrame(
        {
            "id_cliente": np.arange(1, quantidade + 1),
            "idade": rng.integers(18, 71, quantidade),
            "regiao": rng.choice(regioes, quantidade),
            "categoria": rng.choice(categorias, quantidade, p=[0.45, 0.35, 0.20]),
            "renda_mensal": np.round(rng.normal(4200, 1500, quantidade).clip(1200, 15000), 2),
            "gastos_mensais": np.round(rng.normal(1800, 700, quantidade).clip(300, 8000), 2),
            "satisfacao": np.round(rng.normal(7.2, 1.4, quantidade).clip(1, 10), 1),
        }
    )

    # Valores extremos intencionais para demonstrar a identificação por IQR.
    indices_outliers = [0, 1, 2]
    if quantidade > 3:
        dados.loc[indices_outliers, "renda_mensal"] = [28000, 32000, 35000]
        dados.loc[indices_outliers, "gastos_mensais"] = [12000, 15000, 18000]
    return dados


def main() -> None:
    """Executa uma análise local e imprime os resultados principais."""
    base = Path(__file__).with_name("dados_sinteticos.csv")
    resultados = executar_analise(base)
    print(f"Registros brutos: {len(resultados['dados_brutos'])}")
    print(f"Registros após tratamento: {len(resultados['dados_tratados'])}")
    print(f"Registros sem outliers: {len(resultados['dados_filtrados'])}")
    print("\nEstatísticas descritivas:")
    print(resultados["estatisticas"].round(2).to_string())
    print("\nResumo de outliers:")
    print(resultados["outliers"].round(2).to_string())


if __name__ == "__main__":
    main()

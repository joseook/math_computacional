"""Visualização de dados do Trabalho 2 de Matemática Computacional.

Gera os quatro gráficos exigidos (barras, pizza, boxplot com detecção de
outliers via IQR e heatmap de correlação) a partir de ``dados_sinteticos.csv``
e salva as imagens em ``outputs/graficos/`` prontas para uso no relatório
em PDF e nos slides.

Este módulo é independente de ``codigo.py`` e não o importa, modifica ou
substitui — cuida apenas da etapa de visualização.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ_PROJETO / "data" / "dados_sinteticos.csv"
PASTA_SAIDA = RAIZ_PROJETO / "outputs" / "graficos"

COLUNAS_NUMERICAS_CORRELACAO = ["idade", "renda_mensal", "gastos_mensais", "satisfacao"]

COR_DESTAQUE = "#1f4e79"
COR_OUTLIER = "#c0392b"


def configurar_estilo() -> None:
    """Define o tema visual usado em todos os gráficos do trabalho."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.titlesize": 15,
            "axes.titleweight": "bold",
            "axes.labelsize": 12,
            "figure.dpi": 100,
        }
    )


def carregar_dados(caminho: Path = CAMINHO_CSV) -> pd.DataFrame:
    """Lê o CSV da base de dados e devolve o DataFrame original, sem alterações."""
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    return pd.read_csv(caminho)


def criar_pasta_saida(pasta: Path = PASTA_SAIDA) -> Path:
    """Cria a pasta de saída dos gráficos caso ela ainda não exista."""
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def exibir_resumo_base(df: pd.DataFrame) -> None:
    """Imprime no terminal um resumo básico da base carregada."""
    print("=" * 60)
    print("RESUMO DA BASE DE DADOS")
    print("=" * 60)
    print(f"Total de registros: {len(df)}")
    print(f"Total de colunas: {df.shape[1]}")
    print(f"Colunas: {list(df.columns)}")
    print("\nValores ausentes por coluna:")
    print(df.isna().sum().to_string())
    print(f"\nQuantidade de duplicatas: {df.duplicated().sum()}")
    print("=" * 60)


def _confirmar_arquivo(caminho: Path) -> None:
    print(f"[OK] Gráfico salvo em: {caminho}")


def grafico_barras_categoria(df: pd.DataFrame, pasta_saida: Path = PASTA_SAIDA) -> Path:
    """Gera o gráfico de barras com a quantidade de clientes por categoria."""
    dados = df.dropna(subset=["categoria"])
    contagem = dados["categoria"].value_counts().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    paleta = sns.color_palette("Blues_d", n_colors=len(contagem))
    barras = sns.barplot(
        x=contagem.index,
        y=contagem.values,
        hue=contagem.index,
        palette=paleta,
        legend=False,
        ax=ax,
    )

    for barra in barras.patches:
        altura = barra.get_height()
        ax.annotate(
            f"{int(altura)}",
            (barra.get_x() + barra.get_width() / 2, altura),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            xytext=(0, 3),
            textcoords="offset points",
        )

    ax.set_title("Distribuição de clientes por categoria")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Quantidade de clientes")
    ax.margins(y=0.1)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    caminho = pasta_saida / "01_barras_categoria.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    _confirmar_arquivo(caminho)
    return caminho


def grafico_pizza_regiao(
    df: pd.DataFrame, pasta_saida: Path = PASTA_SAIDA, limite_outros: int = 8
) -> Path:
    """Gera o gráfico de pizza com a participação percentual por região."""
    dados = df.dropna(subset=["regiao"])
    contagem = dados["regiao"].value_counts()

    if len(contagem) > limite_outros:
        principais = contagem.iloc[: limite_outros - 1]
        outros = pd.Series({"Outros": contagem.iloc[limite_outros - 1 :].sum()})
        contagem = pd.concat([principais, outros])

    cores = sns.color_palette("Blues_d", n_colors=len(contagem))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        contagem.values,
        labels=contagem.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 11},
        pctdistance=0.75,
    )
    ax.set_title("Distribuição percentual de clientes por região")
    ax.axis("equal")
    plt.tight_layout()

    caminho = pasta_saida / "02_pizza_regiao.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    _confirmar_arquivo(caminho)
    return caminho


def calcular_iqr_outliers(serie: pd.Series) -> dict:
    """Calcula limites do método IQR e identifica outliers de uma série numérica.

    Retorna um dicionário com: q1, q3, iqr, limite_inferior, limite_superior,
    outliers (Series com os valores atípicos) e quantidade_outliers.
    """
    serie_numerica = pd.to_numeric(serie, errors="coerce").dropna()

    q1 = serie_numerica.quantile(0.25)
    q3 = serie_numerica.quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = serie_numerica[
        (serie_numerica < limite_inferior) | (serie_numerica > limite_superior)
    ]

    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "outliers": outliers,
        "quantidade_outliers": int(outliers.shape[0]),
    }


def grafico_boxplot_gastos(df: pd.DataFrame, pasta_saida: Path = PASTA_SAIDA) -> Path:
    """Gera o boxplot de gastos_mensais destacando outliers pelo método IQR."""
    serie = pd.to_numeric(df["gastos_mensais"], errors="coerce").dropna()
    resultado = calcular_iqr_outliers(serie)

    mediana = serie.median()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x=serie,
        ax=ax,
        color="#a6c8e8",
        flierprops={
            "marker": "o",
            "markerfacecolor": COR_OUTLIER,
            "markeredgecolor": COR_OUTLIER,
            "markersize": 6,
        },
        width=0.4,
    )

    linhas_referencia = [
        (resultado["q1"], "Q1", "#2c3e50"),
        (mediana, "Mediana", "#000000"),
        (resultado["q3"], "Q3", "#2c3e50"),
        (resultado["limite_inferior"], "Lim. inferior", "#7f8c8d"),
        (resultado["limite_superior"], "Lim. superior", "#7f8c8d"),
    ]
    for valor, _rotulo, cor in linhas_referencia:
        ax.axvline(valor, color=cor, linestyle="--", linewidth=1, alpha=0.7)

    texto_info = (
        f"Q1 = {resultado['q1']:.2f}\n"
        f"Mediana = {mediana:.2f}\n"
        f"Q3 = {resultado['q3']:.2f}\n"
        f"IQR = {resultado['iqr']:.2f}\n"
        f"Limite inferior = {resultado['limite_inferior']:.2f}\n"
        f"Limite superior = {resultado['limite_superior']:.2f}\n"
        f"Outliers = {resultado['quantidade_outliers']}"
    )
    ax.text(
        0.98,
        0.95,
        texto_info,
        transform=ax.transAxes,
        fontsize=10,
        va="top",
        ha="right",
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "white",
            "edgecolor": "#7f8c8d",
            "alpha": 0.9,
        },
    )

    ax.set_title("Distribuição dos gastos mensais e detecção de outliers pelo IQR")
    ax.set_xlabel("Gastos mensais")
    ax.set_yticks([])
    plt.tight_layout()

    caminho = pasta_saida / "03_boxplot_gastos_outliers.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    _confirmar_arquivo(caminho)
    return caminho


def grafico_heatmap_correlacao(df: pd.DataFrame, pasta_saida: Path = PASTA_SAIDA) -> Path:
    """Gera o heatmap de correlação de Pearson entre as variáveis numéricas."""
    dados_numericos = df[COLUNAS_NUMERICAS_CORRELACAO].apply(
        pd.to_numeric, errors="coerce"
    )
    matriz_correlacao = dados_numericos.corr(method="pearson")

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        matriz_correlacao,
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor="white",
        square=True,
        cbar_kws={"label": "Coeficiente de correlação"},
        ax=ax,
    )
    ax.set_title("Matriz de correlação das variáveis numéricas")
    plt.tight_layout()

    caminho = pasta_saida / "04_heatmap_correlacao.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    _confirmar_arquivo(caminho)
    return caminho


def main() -> None:
    configurar_estilo()
    pasta_saida = criar_pasta_saida()
    df = carregar_dados()
    exibir_resumo_base(df)

    grafico_barras_categoria(df, pasta_saida)
    grafico_pizza_regiao(df, pasta_saida)
    grafico_boxplot_gastos(df, pasta_saida)
    grafico_heatmap_correlacao(df, pasta_saida)

    print("\nTodos os gráficos foram gerados com sucesso em:", pasta_saida.resolve())


if __name__ == "__main__":
    main()

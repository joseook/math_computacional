import unittest

import pandas as pd

from src.codigo import (
    calcular_estatisticas,
    calcular_outliers,
    filtrar_outliers,
    tratar_dados,
)


class TestCodigo(unittest.TestCase):
    def test_tratar_dados_remove_duplicatas_e_converte_nulos(self):
        dados = pd.DataFrame(
            {
                "id_cliente": [1, 1, 2],
                "idade": [30, 30, None],
                "renda_mensal": [2000, 2000, 3000],
            }
        )

        resultado = tratar_dados(dados)

        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado["idade"].isna().sum(), 0)
        self.assertIn(resultado["idade"].dtype.kind, "fi")

    def test_calcular_estatisticas_retorna_medidas_obrigatorias_e_extras(self):
        dados = pd.DataFrame({"valor": [1, 2, 2, 3, 4]})

        resultado = calcular_estatisticas(dados, ["valor"])

        self.assertEqual(resultado.loc["valor", "media"], 2.4)
        self.assertEqual(resultado.loc["valor", "mediana"], 2)
        self.assertEqual(resultado.loc["valor", "moda"], 2)
        self.assertEqual(resultado.loc["valor", "amplitude"], 3)
        self.assertEqual(resultado.loc["valor", "q1"], 2)
        self.assertEqual(resultado.loc["valor", "q3"], 3)
        self.assertGreater(resultado.loc["valor", "desvio_padrao"], 0)
        self.assertGreater(resultado.loc["valor", "variancia"], 0)
        self.assertEqual(resultado.loc["valor", "iqr"], 1)

    def test_calcular_e_filtrar_outliers_pelo_iqr(self):
        dados = pd.DataFrame({"valor": [1, 2, 3, 4, 5, 100]})

        resultado = calcular_outliers(dados, ["valor"])
        filtrado = filtrar_outliers(dados, resultado)

        self.assertEqual(resultado.loc["valor", "limite_superior"], 8.5)
        self.assertEqual(resultado.loc["valor", "quantidade_outliers"], 1)
        self.assertNotIn(100, filtrado["valor"].tolist())
        self.assertEqual(len(filtrado), 5)


if __name__ == "__main__":
    unittest.main()

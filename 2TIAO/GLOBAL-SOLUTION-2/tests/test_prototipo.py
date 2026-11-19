import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.recomendador import catalogo, cobertura, recomendar

APP = Path(__file__).resolve().parents[1] / "src" / "app.py"

class TestRecomendador(unittest.TestCase):
    def test_bairro_tem_prioridade(self):
        with catalogo() as db:
            linhas = recomendar(db, "Vila Cedro", "Papel")
        self.assertEqual([p["id"] for p in linhas], [2, 1, 4])

    def test_sabado_restringe_resultado(self):
        with catalogo() as db:
            linhas = recomendar(db, "Vila Cedro", "Papel", True)
        self.assertEqual([p["id"] for p in linhas], [2, 4])

    def test_alternativas_em_outro_bairro(self):
        with catalogo() as db:
            linhas = recomendar(db, "Vila Cedro", "Eletrônicos")
        self.assertEqual([(p["id"], p["no_bairro"]) for p in linhas], [(6, 0)])

    def test_sem_cobertura(self):
        with catalogo() as db:
            self.assertEqual(recomendar(db, "Vila Cedro", "Óleo de cozinha"), [])

    def test_cobertura_da_base(self):
        with catalogo() as db:
            totais = dict(cobertura(db))
        self.assertEqual(totais, {"Papel": 3, "Plástico": 3, "Vidro": 3,
                                 "Metal": 2, "Eletrônicos": 1})

    def test_fluxo_na_interface(self):
        app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        app.selectbox[0].set_value("Vila Cedro")
        app.selectbox[1].set_value("Papel")
        app.checkbox[0].check().run()
        self.assertEqual(app.subheader[0].value, "Pontos compatíveis (2)")
        self.assertIn("Cooperativa Ipê", [item.value for item in app.markdown if item.value.startswith("**")][0])
        app.selectbox[1].set_value("Óleo de cozinha").run()
        self.assertIn("Nenhum ponto", app.warning[0].value)

if __name__ == "__main__":
    unittest.main()

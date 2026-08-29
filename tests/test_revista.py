import unittest

from src.modulos.revista.revista import Revista


class TestRevista(unittest.TestCase):

    def test_atualizar_revista(self):
        revista = Revista(
            titulo="Revista Antiga",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            tipo="revista",
            issn="12345678",
            edicao=1,
            is_active=True
        )

        revista.atualizar_material(
            "Revista Nova",
            2026,
            2,
            3,
            "87654321",
            10
        )

        self.assertEqual(revista.titulo, "Revista Nova")
        self.assertEqual(revista.ano_publi, 2026)
        self.assertEqual(revista.categoria_id, 2)
        self.assertEqual(revista.editora_id, 3)
        self.assertEqual(revista.issn, "87654321")
        self.assertEqual(revista.edicao, 10)

if __name__ == "__main__":
    unittest.main()

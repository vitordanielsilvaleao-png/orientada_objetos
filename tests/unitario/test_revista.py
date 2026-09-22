import unittest

from src.modulos.revista.revista import Revista


class TestRevista(unittest.TestCase):

    def test_atualizar_revista(self):
        revista = Revista(
            titulo="Revista Antiga",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            issn="12345678",
            edicao=1,
        )

        revista.atualizar(
            "Revista Nova",
            2026,
            2,
            3,
            10
        )

        self.assertEqual(revista.titulo, "revista nova")
        self.assertEqual(revista.ano_publi, 2026)
        self.assertEqual(revista.categoria_id, 2)
        self.assertEqual(revista.editora_id, 3)
        self.assertEqual(revista.issn, "12345678")
        self.assertEqual(revista.edicao, 10)

    def test_criar_revista_normaliza_issn(self):
        revista = Revista(
            titulo="Revista Teste",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            issn="1234-5678",
            edicao=1
        )

        self.assertEqual(
            revista.issn,
            "12345678"
        )

    def test_criar_revista_issn_invalido(self):
        with self.assertRaises(ValueError):
            Revista(
                titulo="Revista Teste",
                ano_publi=2020,
                categoria_id=1,
                editora_id=1,
                issn="1234567",
                edicao=1
            )

    def test_criar_revista_issn_com_letras(self):
        with self.assertRaises(ValueError):
            Revista(
                titulo="Revista Teste",
                ano_publi=2020,
                categoria_id=1,
                editora_id=1,
                issn="1234ABCD",
                edicao=1
            )

    def test_criar_revista_edicao_zero(self):
        with self.assertRaises(ValueError):
            Revista(
                titulo="Revista Teste",
                ano_publi=2025,
                categoria_id=1,
                editora_id=1,
                issn="12345678",
                edicao=0
            )

    def test_criar_revista_edicao_negativa(self):
        with self.assertRaises(ValueError):
            Revista(
                titulo="Revista Teste",
                ano_publi=2025,
                categoria_id=1,
                editora_id=1,
                issn="12345678",
                edicao=-1
            )

if __name__ == "__main__":
    unittest.main()

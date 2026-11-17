import unittest

from src.modulos.material.entidades.categoria import Categoria


class TestCategoria(unittest.TestCase):

    def test_criar_categoria_normaliza_nome(self):
        categoria = Categoria(
            nome="   FICÇÃO CIENTÍFICA   "
        )

        self.assertEqual(
            categoria.nome,
            "ficção científica"
        )

    def test_criar_categoria_nome_vazio(self):
        with self.assertRaises(ValueError):
            Categoria(
                nome="   "
            )

    def test_criar_categoria_nome_invalido(self):
        with self.assertRaises(ValueError):
            Categoria(
                nome=None
            )

    def test_renomear_categoria_normaliza_nome(self):
        categoria = Categoria(
            nome="Romance"
        )

        categoria.renomear(
            "   FICÇÃO CIENTÍFICA   "
        )

        self.assertEqual(
            categoria.nome,
            "ficção científica"
        )

    def test_renomear_categoria_nome_vazio(self):
        categoria = Categoria(
            nome="Romance"
        )

        with self.assertRaises(ValueError):
            categoria.renomear(
                "   "
            )


if __name__ == "__main__":
    unittest.main()

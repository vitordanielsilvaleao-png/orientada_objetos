import unittest

from src.modulos.material.entidades.categoria import Categoria


class TestCategoria(unittest.TestCase):

    def test_criar_categoria_normaliza_nome(self):
        categoria = Categoria(
            nome="   FICÇÃO CIENTÍFICA   "
        )

        self.assertEqual(
            categoria.nome,
            "ficcao cientifica"
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

    def test_atualizar_categoria_normaliza_nome(self):
        categoria = Categoria(
            nome="Romance"
        )

        categoria.atualizar(
            "   FICÇÃO CIENTÍFICA   "
        )

        self.assertEqual(
            categoria.nome,
            "ficcao cientifica"
        )

    def test_atualizar_categoria_nome_vazio(self):
        categoria = Categoria(
            nome="Romance"
        )

        with self.assertRaises(ValueError):
            categoria.atualizar(
                "   "
            )


if __name__ == "__main__":
    unittest.main()

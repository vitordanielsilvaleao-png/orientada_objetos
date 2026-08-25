import unittest

from src.modulos.livro.entidades.livro import Livro


class TestLivro(unittest.TestCase):

    def test_atualizar_livro(self):
        livro = Livro(
            titulo="Livro Antigo",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            tipo="livro",
            isbn="1234567890",
            autor_id=1,
            is_active=True
        )

        livro.atualizar_livro(
            "Livro Novo",
            2026,
            2,
            3,
            "9876543210",
            4
        )

        self.assertEqual(livro.titulo, "Livro Novo")
        self.assertEqual(livro.ano_publi, 2026)
        self.assertEqual(livro.categoria_id, 2)
        self.assertEqual(livro.editora_id, 3)
        self.assertEqual(livro.isbn, "9876543210")
        self.assertEqual(livro.autor_id, 4)

    def test_descricao_livro(self):
        livro = Livro(
            titulo="Python POO",
            ano_publi=2026,
            categoria_id=1,
            editora_id=1,
            tipo="livro",
            isbn="1234567890",
            autor_id=2,
            is_active=True
        )

        resultado = livro.descricao()

        self.assertIn("Python POO", resultado)
        self.assertIn("2", resultado)
        self.assertIn("1234567890", resultado)


if __name__ == "__main__":
    unittest.main()

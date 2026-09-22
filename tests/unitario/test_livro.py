import unittest

from src.modulos.livro.entidades.livro import Livro


class TestLivro(unittest.TestCase):

    def test_atualizar_livro(self):
        livro = Livro(
            titulo="Livro Antigo",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            isbn="1234567891234",
            autor_id=1,
        )

        livro.atualizar(
            "Livro Novo",
            2026,
            2,
            3,
            4
        )

        self.assertEqual(livro.titulo, "livro novo")
        self.assertEqual(livro.ano_publi, 2026)
        self.assertEqual(livro.categoria_id, 2)
        self.assertEqual(livro.editora_id, 3)
        self.assertEqual(livro.isbn, "1234567891234")
        self.assertEqual(livro.autor_id, 4)

    def test_atualizar_livro_inativo(self):
        livro = Livro(
            titulo="Livro Antigo",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            isbn="1234567891234",
            autor_id=1,
        )

        livro.is_active = False

        with self.assertRaises(ValueError):
            livro.atualizar(
                "Livro Novo",
                2026,
                2,
                3,
                4
            )

    def test_criar_livro_normaliza_isbn(self):
        livro = Livro(
            titulo="Livro Antigo",
            ano_publi=2020,
            categoria_id=1,
            editora_id=1,
            isbn="123.456.789-1234",
            autor_id=1,
        )

        self.assertEqual(
            livro.isbn,
            "1234567891234"
        )

    def test_criar_livro_isbn_invalido(self):
        with self.assertRaises(ValueError):
            Livro(
                titulo="Livro Teste",
                ano_publi=2020,
                categoria_id=1,
                editora_id=1,
                isbn="123456789",
                autor_id=1,
            )

    def test_criar_livro_isbn_com_letras(self):
        with self.assertRaises(ValueError):
            Livro(
                titulo="Livro Teste",
                ano_publi=2020,
                categoria_id=1,
                editora_id=1,
                isbn="123ABC4567890",
                autor_id=1
            )

if __name__ == "__main__":
    unittest.main()

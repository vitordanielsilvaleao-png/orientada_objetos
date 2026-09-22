import unittest
from src.modulos.material.entidades.material import Material

class TestMaterial(unittest.TestCase):
    def test_criar_material_normaliza_titulo(self):
        material = Material(
            titulo="   ORIENTAÇÃO A OBJETOS   ",
            ano_publi=2026,
            categoria_id=1,
            editora_id=1
        )

        self.assertEqual(
            material.titulo,
            "orientação a objetos"
        )

    def test_criar_material_ano_invalido(self):
        with self.assertRaises(ValueError):
            Material(
                titulo="Livro Teste",
                ano_publi=0,
                categoria_id=1,
                editora_id=1
            )

    def test_criar_material_ano_negativo(self):
        with self.assertRaises(ValueError):
            Material(
                titulo="Livro Teste",
                ano_publi=-1,
                categoria_id=1,
                editora_id=1
            )

    def test_atualizar_material_ativo (self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True

        material.atualizar("Orientação a Objetos", 2026, 1, 1)

        self.assertEqual(material.titulo, "orientação a objetos")
        self.assertEqual(material.ano_publi, 2026)
        self.assertEqual(material.categoria_id, 1)
        self.assertEqual(material.editora_id, 1)

    def test_atualizar_material_inativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = False

        with self.assertRaises(ValueError):
            material.atualizar("Orientação a Objetos", 2026, 1, 1)

    def test_atualizar_material_ano_invalido(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        with self.assertRaises(ValueError):
            material.atualizar(
                ano_publi=0
            )

    def test_atualizar_material_ano_negativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        with self.assertRaises(ValueError):
            material.atualizar(
                ano_publi=-1
            )

    def test_atualizar_material_normaliza_titulo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.atualizar(
            titulo="   ORIENTAÇÃO A OBJETOS   "
        )

        self.assertEqual(
            material.titulo,
            "orientação a objetos"
        )

    def test_inativar_material_ativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True

        material.inativar()

        self.assertFalse(material.is_active)

    def test_inativar_material_inativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = False

        with self.assertRaises(ValueError):
            material.inativar()

    def test_ativar_material_inativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = False

        material.ativar()

        self.assertTrue(material.is_active)

    def test_ativar_material_ativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True

        with self.assertRaises(ValueError):
            material.ativar()

    def test_validar_material_ativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True

        resultado = material.esta_ativo()

        self.assertTrue(resultado)

    def test_validar_material_inativo(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = False

        resultado = material.esta_ativo()

        self.assertFalse(resultado)

    def test_validar_material_ativo_disponivel(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True
        material.status = "DISPONIVEL"

        resultado = material.esta_disponivel()

        self.assertTrue(resultado)

    def test_validar_material_ativo_indisponivel(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = True
        material.status = "EMPRESTADO"

        resultado = material.esta_disponivel()

        self.assertFalse(resultado)

    def test_validar_material_inativo_disponivel(self):
        material = Material(
            titulo="Livro Teste",
            ano_publi=1954,
            categoria_id=1,
            editora_id=1
        )

        material.is_active = False
        material.status = "DISPONIVEL"

        resultado = material.esta_disponivel()

        self.assertFalse(resultado)
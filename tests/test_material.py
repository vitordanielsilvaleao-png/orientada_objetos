import unittest
from src.modulos.material.entidades.material import Material

class TestMaterial(unittest.TestCase):
    def test_atualizar_material_ativo (self):
        material = Material()

        material.is_active = True

        material.atualizar_material(
            "Orientação a Objetos",
            2026,
            1,
            1
        )

        self.assertEqual(material.titulo, "Orientação a Objetos")
        self.assertEqual(material.ano_publi, 2026)
        self.assertEqual(material.categoria_id, 1)
        self.assertEqual(material.editora_id, 1)

    def test_atualizar_material_inativo(self):
        material = Material()

        material.is_active = False

        with self.assertRaises(ValueError):
            material.atualizar_material(
                "Orientação a Objetos",
                2026,
                1,
                1
            )

    def test_inativar_material_ativo(self):
        material = Material()

        material.is_active = True

        material.inativar_material()

        self.assertFalse(material.is_active)

    def test_inativar_material_inativo(self):
        material = Material()

        material.is_active = False

        with self.assertRaises(ValueError):
            material.inativar_material()

    def test_ativar_material_inativo(self):
        material = Material()

        material.is_active = False

        material.ativar_material()

        self.assertTrue(material.is_active)

    def test_ativar_material_ativo(self):
        material = Material()

        material.is_active = True

        with self.assertRaises(ValueError):
            material.ativar_material()

    def test_validar_material_ativo(self):
        material = Material()

        material.is_active = True

        resultado = material.esta_ativo()

        self.assertTrue(resultado)

    def test_validar_material_inativo(self):
        material = Material()

        material.is_active = False

        resultado = material.esta_ativo()

        self.assertFalse(resultado)

    def test_validar_material_ativo_disponivel(self):
        material = Material()

        material.is_active = True
        material.status = "DISPONIVEL"

        resultado = material.esta_disponivel()

        self.assertTrue(resultado)

    def test_validar_material_ativo_indisponivel(self):
        material = Material()

        material.is_active = True
        material.status = "EMPRESTADO"

        resultado = material.esta_disponivel()

        self.assertFalse(resultado)

    def test_validar_material_inativo_disponivel(self):
        material = Material()

        material.is_active = False
        material.status = "DISPONIVEL"

        resultado = material.esta_disponivel()

        self.assertFalse(resultado)
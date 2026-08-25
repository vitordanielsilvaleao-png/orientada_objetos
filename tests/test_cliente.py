import unittest

from src.modulos.cliente.cliente import Cliente


class TestCliente(unittest.TestCase):
    def test_atualizar_cliente(self):
        cliente = Cliente()

        cliente.is_active = True

        cliente.atualizar_cliente(
            "Maria Silva",
            "Centro",
            "Rua A",
            100,
            "Apto 2",
            "34999999999"
        )

        self.assertEqual(cliente.nome, "Maria Silva")
        self.assertEqual(cliente.bairro, "Centro")
        self.assertEqual(cliente.rua, "Rua A")
        self.assertEqual(cliente.numero, 100)
        self.assertEqual(cliente.complemento, "Apto 2")
        self.assertEqual(cliente.telefone, "34999999999")

    def test_atualizar_cliente_inativo(self):
        cliente = Cliente()

        cliente.is_active = False

        with self.assertRaises(ValueError):
            cliente.atualizar_cliente(
                "Maria Silva",
                "Centro",
                "Rua A",
                100,
                "Apto 2",
                "34999999999"
            )

    def test_inativar_cliente(self):
        cliente = Cliente()

        cliente.is_active = True

        cliente.inativar_cliente()

        self.assertFalse(cliente.is_active)

    def test_inativar_cliente_ja_inativo(self):
        cliente = Cliente()

        cliente.is_active = False

        with self.assertRaises(ValueError):
            cliente.inativar_cliente()

    def test_ativar_cliente(self):
        cliente = Cliente()

        cliente.is_active = False

        cliente.ativar_cliente()

        self.assertTrue(cliente.is_active)

    def test_ativar_cliente_ja_ativo(self):
        cliente = Cliente()

        cliente.is_active = True

        with self.assertRaises(ValueError):
            cliente.ativar_cliente()

    def test_validar_cliente_ativo(self):
        cliente = Cliente()

        cliente.is_active = True

        resultado = cliente.validar_cliente_ativo()

        self.assertTrue(resultado)

    def test_validar_cliente_inativo(self):
        cliente = Cliente()

        cliente.is_active = False

        resultado = cliente.validar_cliente_ativo()

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
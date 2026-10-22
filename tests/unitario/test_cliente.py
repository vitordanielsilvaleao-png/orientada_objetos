import unittest

from src.modulos.cliente.cliente import Cliente


class TestCliente(unittest.TestCase):
    def test_criar_cliente_corretamente(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        self.assertEqual(cliente.cpf, "00000000000")
        self.assertEqual(cliente.nome, "Ana Gabriela")
        self.assertEqual(cliente.bairro, "Aves")
        self.assertEqual(cliente.rua, "Rua B")
        self.assertEqual(cliente.numero, 200)
        self.assertEqual(cliente.complemento, "Casa")
        self.assertEqual(cliente.telefone, "34888888888")

    def test_criar_cliente_com_cpf_sem_formatacao(self):
        cliente = Cliente("000.000.000-00",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        self.assertEqual(cliente.cpf, "00000000000")
        self.assertEqual(cliente.nome, "Ana Gabriela")
        self.assertEqual(cliente.bairro, "Aves")
        self.assertEqual(cliente.rua, "Rua B")
        self.assertEqual(cliente.numero, 200)
        self.assertEqual(cliente.complemento, "Casa")
        self.assertEqual(cliente.telefone, "34888888888")

    def test_criar_cliente_sem_cpf(self):

        with self.assertRaises(ValueError):
            cliente = Cliente("",
                "Ana Gabriela",
                "Aves",
                "Rua B",
                200,
                "34888888888",
                "Casa")

    def test_criar_cliente_com_cpf_espacos(self):

        with self.assertRaises(ValueError):
            cliente = Cliente("     ",
                "Ana Gabriela",
                "Aves",
                "Rua B",
                200,
                "34888888888",
                "Casa")

    def test_criar_cliente_cpf_com_letras(self):

        with self.assertRaises(ValueError):
            cliente = Cliente("000AA000000",
                "Ana Gabriela",
                "Aves",
                "Rua B",
                200,
                "34888888888",
                "Casa")


    def test_atualizar_cliente_corretamente(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = True

        cliente.atualizar_cliente(
            "Maria Silva",
            "Centro",
            "Rua A",
            100,
            "Apto 2",
            "34999999999"
        )

        self.assertEqual(cliente.cpf, "00000000000")
        self.assertEqual(cliente.nome, "Maria Silva")
        self.assertEqual(cliente.bairro, "Centro")
        self.assertEqual(cliente.rua, "Rua A")
        self.assertEqual(cliente.numero, 100)
        self.assertEqual(cliente.complemento, "Apto 2")
        self.assertEqual(cliente.telefone, "34999999999")

    def test_atualizar_cliente_inativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

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
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = True

        cliente.inativar_cliente()

        self.assertFalse(cliente.is_active)

    def test_inativar_cliente_ja_inativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = False

        with self.assertRaises(ValueError):
            cliente.inativar_cliente()

    def test_ativar_cliente(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = False

        cliente.ativar_cliente()

        self.assertTrue(cliente.is_active)

    def test_ativar_cliente_ja_ativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = True

        with self.assertRaises(ValueError):
            cliente.ativar_cliente()

    def test_validar_cliente_ativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = True

        resultado = cliente.validar_cliente_ativo()

        self.assertTrue(resultado)

    def test_validar_cliente_inativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "Casa",
            "34888888888")

        cliente.is_active = False

        resultado = cliente.validar_cliente_ativo()

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
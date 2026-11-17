import unittest

from src.modulos.cliente.entidade.cliente import Cliente


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

    def test_criar_cliente_com_cpf_formatado(self):
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
            Cliente("",
                "Ana Gabriela",
                "Aves",
                "Rua B",
                200,
                "34888888888",
                "Casa")

    def test_criar_cliente_com_cpf_espacos(self):

        with self.assertRaises(ValueError):
            Cliente("     ",
                "Ana Gabriela",
                "Aves",
                "Rua B",
                200,
                "34888888888",
                "Casa")

    def test_criar_cliente_cpf_com_letras(self):

        with self.assertRaises(ValueError):
            Cliente("000AA000000",
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
            "34888888888",
            "Casa")

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
            "34888888888",
            "Casa")

        cliente.inativar_cliente()

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
            "34888888888",
            "Casa")

        cliente.inativar_cliente()

        self.assertFalse(cliente.is_active)

    def test_inativar_cliente_ja_inativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        cliente.inativar_cliente()

        with self.assertRaises(ValueError):
            cliente.inativar_cliente()

    def test_ativar_cliente(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        cliente.inativar_cliente()

        cliente.ativar_cliente()

        self.assertTrue(cliente.is_active)

    def test_ativar_cliente_ja_ativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        with self.assertRaises(ValueError):
            cliente.ativar_cliente()

    def test_validar_cliente_ativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        resultado = cliente.is_active

        self.assertTrue(resultado)

    def test_validar_cliente_inativo(self):
        cliente = Cliente("00000000000",
            "Ana Gabriela",
            "Aves",
            "Rua B",
            200,
            "34888888888",
            "Casa")

        cliente.inativar_cliente()

        resultado = cliente.is_active

        self.assertFalse(resultado)


    def test_cpf_somente_leitura(self):
        cliente = Cliente(cpf="00000000000",
            nome="Ana Gabriela",
            bairro="Aves",
            rua="Rua B",
            numero=200,
            telefone="34888888888",
            complemento="Casa")

        with self.assertRaises(AttributeError):
            cliente.cpf = "11111111111"

        self.assertEqual(cliente.cpf, "00000000000")

    def test_alterar_cpf_pelo_atributo_privado(self):
        cliente = Cliente(cpf="00000000000",
            nome="Ana Gabriela",
            bairro="Aves",
            rua="Rua B",
            numero=200,
            telefone="34888888888",
            complemento="Casa")

        with self.assertRaises(ValueError):
            cliente._cpf = "11111111111"

        self.assertEqual(cliente.cpf, "00000000000")

    def test_is_active_somente_leitura(self):
        cliente = Cliente(cpf="00000000000",
            nome="Ana Gabriela",
            bairro="Aves",
            rua="Rua B",
            numero=200,
            telefone="34888888888",
            complemento="Casa")

        with self.assertRaises(AttributeError):
            cliente.is_active = False

        self.assertTrue(cliente.is_active)


if __name__ == "__main__":
    unittest.main()
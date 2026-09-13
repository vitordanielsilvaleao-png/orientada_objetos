import unittest

from fastapi import HTTPException

from src.modulos.cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from src.modulos.cliente.service.cliente_service import ClienteService
from src.modulos.cliente.cliente import Cliente
from src.database.database import db

class TestClienteService(unittest.TestCase):

    def test_cadastrar_cliente_corretamente(self):
        sessao = db.session()
        try:

            data = SchemaClienteCadastro(
                nome = "Teste Cadastro Cliente",
                bairro = "bairro",
                rua = "rua",
                numero = 1,
                complemento = "complemento",
                telefone = "123456789"
            )

            cliente_service = ClienteService(sessao)

            cliente = cliente_service.cadastrar(data)

            self.assertEqual(cliente.nome, "Teste Cadastro Cliente")
            self.assertEqual(cliente.bairro, "bairro")
            self.assertEqual(cliente.rua, "rua")
            self.assertEqual(cliente.numero, 1)
            self.assertEqual(cliente.complemento, "complemento")
            self.assertEqual(cliente.telefone, "123456789")

            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_cliente_existente(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)
            cliente_novo = self.criar_cliente(sessao)

            data = SchemaClienteCadastro(
                nome = "Teste Cadastro Cliente 2",
                bairro = "bairro",
                rua = "rua",
                numero = 1,
                complemento = "complemento",
                telefone = "123456789"
            )

            with self.assertRaises(HTTPException):
                cliente_service.cadastrar(data)

            sessao.delete(cliente_novo)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_cliente(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            lista_cliente = cliente_service.visualizar()

            for cliente in lista_cliente:
                self.assertIsInstance(cliente, Cliente)
        finally:
            sessao.close()

    def test_atualiza_cliente(self):
        sessao = db.session()
        try:

            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)

            data = SchemaClienteAtualizacao(
                nome = "Teste Cadastro Cliente 1",
                bairro = "bairro2",
                rua = "rua2",
                numero = 12,
                complemento = "complemento2",
                telefone = "1234567892"
            )

            cliente_service.atualizar(cliente_novo.id, data)
            sessao.refresh(cliente_novo)

            self.assertEqual(cliente_novo.nome, "Teste Cadastro Cliente 1")
            self.assertEqual(cliente_novo.bairro, "bairro2")
            self.assertEqual(cliente_novo.rua, "rua2")
            self.assertEqual(cliente_novo.numero, 12)
            self.assertEqual(cliente_novo.complemento, "complemento2")
            self.assertEqual(cliente_novo.telefone, "1234567892")

            sessao.delete(cliente_novo)
            sessao.commit()
        finally:
            sessao.close()


    def test_inativar_cliente_ativo(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)

            cliente_service.inativar(cliente_novo.id)

            sessao.refresh(cliente_novo)

            self.assertFalse(cliente_novo.is_active)

            sessao.delete(cliente_novo)
            sessao.commit()
        finally:
            sessao.close()

    def test_inativar_cliente_inexistente(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            with self.assertRaises(HTTPException):
                cliente_service.inativar(0)
        finally:
            sessao.close()

    def test_ativar_cliente_inativo(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)
            cliente_novo.inativar_cliente()

            cliente_service.ativar(cliente_novo.id)

            sessao.refresh(cliente_novo)

            self.assertTrue(cliente_novo.is_active)

            sessao.delete(cliente_novo)
            sessao.commit()
        finally:
            sessao.close()

    def test_ativar_cliente_inexistente(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            with self.assertRaises(HTTPException):
                cliente_service.ativar(0)
        finally:
            sessao.close()

    def criar_cliente(self, sessao):

        cliente_novo = Cliente(
            nome = "Teste Cadastro Cliente 2",
            bairro = "bairro",
            rua = "rua",
            numero = 1,
            complemento = "complemento",
            telefone = "123456789"
        )

        sessao.add(cliente_novo)
        sessao.commit()
        sessao.refresh(cliente_novo)
        return cliente_novo
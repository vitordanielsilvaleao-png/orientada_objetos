import unittest

from fastapi import HTTPException

from src.modulos.cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from src.modulos.cliente.service.cliente_service import ClienteService
from src.modulos.cliente.entidade.cliente import Cliente
from src.database.database import db

class TestClienteService(unittest.TestCase):

    def test_cadastrar_cliente_corretamente(self):
        sessao = db.session()
        try:

            data = SchemaClienteCadastro(
                cpf="00000000000",
                nome="Teste Cadastro Cliente",
                bairro="bairro",
                rua="rua",
                numero=1,
                complemento="complemento",
                telefone="34888888888"
            )

            cliente_service = ClienteService(sessao)

            cliente = cliente_service.cadastrar(data)

            self.assertEqual(cliente.nome, "Teste Cadastro Cliente")
            self.assertEqual(cliente.bairro, "bairro")
            self.assertEqual(cliente.rua, "rua")
            self.assertEqual(cliente.numero, 1)
            self.assertEqual(cliente.complemento, "complemento")
            self.assertEqual(cliente.telefone, "34888888888")
            self.assertEqual(cliente.cpf, "00000000000")

            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_cliente_cpf_duplicado(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)
            cliente_novo = self.criar_cliente(sessao)

            data = SchemaClienteCadastro(
                cpf=cliente_novo.cpf,
                nome="Teste Cadastro Cliente 2",
                bairro="bairro",
                rua="rua",
                numero=1,
                complemento="complemento",
                telefone="34888888888"
            )

            with self.assertRaises(HTTPException):
                cliente_service.cadastrar(data)

            sessao.delete(cliente_novo)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_cliente_dados_invalidos(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            data = SchemaClienteCadastro(
                cpf="00000000000",
                nome="Teste Cadastro Cliente",
                bairro="bairro",
                rua="rua",
                numero=1,
                complemento="complemento",
                telefone="abcdefghij"
            )

            with self.assertRaises(HTTPException) as contexto:
                cliente_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 422)
            self.assertEqual(contexto.exception.detail, "O telefone informado é inválido")

        finally:
            sessao.close()

    def test_visualiza_cliente(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)

            lista_cliente = cliente_service.visualizar()

            for cliente in lista_cliente:
                self.assertIsInstance(cliente, Cliente)

            sessao.delete(cliente_novo)
            sessao.commit()
        finally:
            sessao.close()

    def test_atualiza_cliente(self):
        sessao = db.session()
        try:

            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)

            data = SchemaClienteAtualizacao(
                nome="Teste Cadastro Cliente 1",
                bairro="bairro2",
                rua="rua2",
                numero=12,
                complemento="complemento2",
                telefone="34888888888"
            )

            cliente_service.atualizar(cliente_novo.id, data)
            sessao.refresh(cliente_novo)

            self.assertEqual(cliente_novo.nome, "Teste Cadastro Cliente 1")
            self.assertEqual(cliente_novo.bairro, "bairro2")
            self.assertEqual(cliente_novo.rua, "rua2")
            self.assertEqual(cliente_novo.numero, 12)
            self.assertEqual(cliente_novo.complemento, "complemento2")
            self.assertEqual(cliente_novo.telefone, "34888888888")

            sessao.delete(cliente_novo)
            sessao.commit()
        finally:
            sessao.close()


    def test_inativar_cliente_ativo(self):
        sessao = db.session()
        try:
            cliente_service = ClienteService(sessao)

            cliente_novo = self.criar_cliente(sessao)

            cliente_inativado = cliente_service.inativar(cliente_novo.id)

            self.assertEqual(cliente_inativado.id, cliente_novo.id)
            self.assertFalse(cliente_inativado.is_active)

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

            cliente_ativado = cliente_service.ativar(cliente_novo.id)

            self.assertEqual(cliente_ativado.id, cliente_novo.id)
            self.assertTrue(cliente_ativado.is_active)

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
            cpf="00000000000",
            nome="Teste Cadastro Cliente 2",
            bairro="bairro",
            rua="rua",
            numero=1,
            complemento="complemento",
            telefone="34888888888"
        )

        sessao.add(cliente_novo)
        sessao.commit()
        sessao.refresh(cliente_novo)
        return cliente_novo
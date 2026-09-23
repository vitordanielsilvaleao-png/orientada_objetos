from datetime import datetime, timedelta
import unittest
import random

from fastapi import HTTPException

from src.compartilhado.enum import StatusMaterial
from src.modulos.material.entidades.editora import Editora
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.livro.entidades.autor import Autor
from src.modulos.reserva.reserva import Reserva
from src.modulos.emprestimo.emprestimo import Emprestimo
from src.modulos.cliente.cliente import Cliente
from src.modulos.livro.entidades.livro import Livro
from database.database import db

from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro
from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService


class TestEmprestimoService(unittest.TestCase):

    def test_cadastrar_emprestimo_corretamente(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            emprestimo = emprestimo_service.cadastrar(data)

            self.assertEqual(emprestimo.cliente_id, cliente.id)
            self.assertEqual(emprestimo.material_id, livro.id)
            self.assertTrue(emprestimo.is_active)
            self.assertEqual(emprestimo.status, "ABERTO")
            self.assertEqual(emprestimo.data_devolucao, None)

            sessao.delete(emprestimo)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_com_reserva_para_cliente(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            reserva_nova = Reserva(
                cliente_id=cliente.id,
                titulo=livro.titulo,
                material_id=livro.id
            )

            livro.status = StatusMaterial.RESERVADO

            sessao.add(reserva_nova)
            sessao.commit()

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            emprestimo = emprestimo_service.cadastrar(data)

            self.assertEqual(emprestimo.cliente_id, cliente.id)
            self.assertEqual(emprestimo.material_id, livro.id)
            self.assertTrue(emprestimo.is_active)
            self.assertEqual(emprestimo.status, "ABERTO")
            self.assertEqual(emprestimo.data_devolucao, None)
            self.assertEqual(livro.status, StatusMaterial.EMPRESTADO)

            sessao.delete(emprestimo)
            sessao.delete(reserva_nova)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_com_reserva_usuario_diferente(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)
            cliente2 = self.criar_cliente(sessao)

            reserva_nova = Reserva(
                cliente_id=cliente.id,
                titulo=livro.titulo,
                material_id=livro.id
            )

            livro.status = StatusMaterial.RESERVADO

            sessao.add(reserva_nova)
            sessao.commit()

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente2.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(reserva_nova)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.delete(cliente2)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_usuario_inativo(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            cliente.inativar_cliente()

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_material_inexistente(self):
        sessao = db.session()
        try:

            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=0,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 400)

            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_material_inativo(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            livro.inativar()

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_material_indisponivel(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            livro.status = StatusMaterial.EMPRESTADO

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_com_emprestimo_atrasado(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            livro2, categoria_livro2, editora_livro2, autor_livro2 = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data_atual = datetime.now()
            data_atrasada = data_atual - timedelta(days=31)

            emprestimo = Emprestimo(
                cliente_id=cliente.id,
                material_id=livro2.id,
                data_emprestimo= data_atrasada,
                status = "ATRASADO"
            )

            livro2.status = StatusMaterial.EMPRESTADO

            sessao.add(emprestimo)
            sessao.commit()

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(emprestimo)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(livro2)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

            sessao.delete(categoria_livro2)
            sessao.delete(editora_livro2)
            sessao.delete(autor_livro2)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_emprestimo_com_limite_emprestimo(self):
        sessao = db.session()
        try:

            livros = []
            emprestimos = []
            categorias = []
            editoras = []
            autores = []

            cliente = self.criar_cliente(sessao)

            for _ in range(4):
                livro, categoria, editora, autor = self.criar_livro(sessao)
                livros.append(livro)
                categorias.append(categoria)
                editoras.append(editora)
                autores.append(autor)

                emprestimo = Emprestimo(
                    cliente_id=cliente.id,
                    material_id=livro.id
                )

                livro.status = StatusMaterial.EMPRESTADO

                emprestimos.append(emprestimo)

                sessao.add(livro)
                sessao.add(emprestimo)
                sessao.commit()

            livro_excedente, categoria_excedente, editora_excedente, autor_excedente = self.criar_livro(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro_excedente.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            # Limpa os 4 empréstimos
            for emprestimo in emprestimos:
                sessao.delete(emprestimo)

            sessao.commit()

            # Limpa os livros
            for livro in livros:
                sessao.delete(livro)

            sessao.delete(livro_excedente)
            sessao.delete(cliente)
            sessao.commit()

            for categoria in categorias:
                sessao.delete(categoria)

            for editora in editoras:
                sessao.delete(editora)

            for autor in autores:
                sessao.delete(autor)

            sessao.delete(categoria_excedente)
            sessao.delete(editora_excedente)
            sessao.delete(autor_excedente)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_emprestimos(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            emprestimo = Emprestimo(
                cliente_id=cliente.id,
                material_id=livro.id
            )

            sessao.add(emprestimo)
            sessao.commit()

            emprestimo_service = EmprestimoService(sessao)

            lista_emprestimo = emprestimo_service.visualizar()

            for emprestimo in lista_emprestimo:
                self.assertIsInstance(emprestimo, Emprestimo)

            sessao.delete(emprestimo)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_emprestimos_atrasados(self):
        sessao = db.session()
        try:

            data_atual = datetime.now()
            data_atrasada = data_atual - timedelta(days=31)

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            emprestimo = Emprestimo(
                cliente_id=cliente.id,
                material_id=livro.id,
                status="ATRASADO",
                data_emprestimo=data_atrasada

            )

            sessao.add(emprestimo)
            sessao.commit()

            emprestimo_service = EmprestimoService(sessao)

            lista_atrasados = emprestimo_service.visualizar_atrasados()

            for emprestimo in lista_atrasados:
                self.assertIsInstance(emprestimo, Emprestimo)

            sessao.delete(emprestimo)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_registar_devolucao_corretamente(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            emprestimo = emprestimo_service.cadastrar(data)

            emprestimo_service.registrar_devolucao(emprestimo.id)

            self.assertEqual(emprestimo.cliente_id, cliente.id)
            self.assertEqual(emprestimo.material_id, livro.id)
            self.assertEqual(emprestimo.status, "DEVOLVIDO")
            self.assertIsNotNone(emprestimo.data_devolucao)
            self.assertFalse(emprestimo.is_active)
            self.assertEqual(livro.status, StatusMaterial.DISPONIVEL)

            sessao.delete(emprestimo)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_registar_devolucao_emprestimo_inexistente(self):
        sessao = db.session()
        try:

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.registrar_devolucao(0)

            self.assertEqual(contexto.exception.status_code, 404)

        finally:
            sessao.close()

    def test_registrar_devolucao_com_reserva_ativa(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)
            cliente = self.criar_cliente(sessao)
            cliente_reserva = self.criar_cliente(sessao)

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            emprestimo = emprestimo_service.cadastrar(data)

            reserva = Reserva(
                titulo=livro.titulo,
                cliente_id=cliente_reserva.id,
                material_id=None
            )

            sessao.add(reserva)
            sessao.commit()

            emprestimo_service.registrar_devolucao(emprestimo.id)

            self.assertEqual(emprestimo.status, "DEVOLVIDO")
            self.assertFalse(emprestimo.is_active)
            self.assertIsNotNone(emprestimo.data_devolucao)

            self.assertEqual(livro.status, StatusMaterial.RESERVADO)

            self.assertEqual(reserva.material_id, livro.id)
            self.assertTrue(reserva.is_active)

            sessao.delete(emprestimo)
            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(livro)
            sessao.delete(cliente)
            sessao.delete(cliente_reserva)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def criar_categoria(self, sessao):

        num = random.randint(1, 999999)

        categoria_nova = Categoria(
            nome=f"Teste Categoria{num}"
        )

        sessao.add(categoria_nova)
        sessao.commit()
        sessao.refresh(categoria_nova)

        return categoria_nova

    def criar_editora(self, sessao):

        num = random.randint(1, 999999)

        editora_nova = Editora(
            nome=f"Teste Editora{num}"
        )

        sessao.add(editora_nova)
        sessao.commit()
        sessao.refresh(editora_nova)

        return editora_nova

    def criar_autor(self, sessao):

        num = random.randint(1, 999999)

        autor_novo = Autor(
            nome=f'Teste Autor{num}'
        )

        sessao.add(autor_novo)
        sessao.commit()
        sessao.refresh(autor_novo)

        return autor_novo

    def criar_livro(self, sessao):

        isbn = random.randint(1111111111111, 9999999999999)

        categoria = self.criar_categoria(sessao)
        editora = self.criar_editora(sessao)
        autor = self.criar_autor(sessao)

        livro_novo = Livro(
            titulo="teste atualizar livro",
            ano_publi=2025,
            editora_id=editora.id,
            categoria_id=categoria.id,
            autor_id=autor.id,
            isbn=str(isbn))

        sessao.add(livro_novo)
        sessao.commit()
        sessao.refresh(livro_novo)
        return livro_novo, categoria, editora, autor


    def criar_cliente(self, sessao):

        cliente_novo = Cliente(
            nome=f"Teste Emprestimo {random.randint(1, 999999)}",
            bairro="Centro",
            rua="Afonso Pena",
            numero=131,
            complemento="Casa",
            telefone="99999999999"
        )

        sessao.add(cliente_novo)
        sessao.commit()
        sessao.refresh(cliente_novo)
        return cliente_novo
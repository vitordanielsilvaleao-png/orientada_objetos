import unittest

from fastapi import HTTPException

from src.modulos.reserva.schemas.schema_reserva import SchemaReservaCadastro
from src.modulos.reserva.service.reserva_service import ReservaService
from src.modulos.reserva.reserva import Reserva
from src.modulos.cliente.cliente import Cliente
from src.modulos.material.entidades.material import Material
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.material.entidades.editora import Editora
from src.database.database import db

from datetime import datetime, timedelta

class TestReservaService(unittest.TestCase):

    def test_cadastrar_reserva_corretamente(self):
        sessao = db.session()
        try:
            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            data = SchemaReservaCadastro(
                titulo="Livro Teste",
                cliente_id=cliente.id,
                material_id=material.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            self.assertEqual(reserva.titulo, "Livro Teste")
            self.assertEqual(reserva.cliente_id, cliente.id)
            self.assertEqual(reserva.material_id, material.id)
            self.assertTrue(reserva.is_active)

            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_reserva_existente(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            reserva_nova = self.criar_reserva(
                sessao,
                cliente.id,
                material.id
            )

            data = SchemaReservaCadastro(
                titulo="Livro Teste",
                cliente_id=cliente.id,
                material_id=material.id
            )

            with self.assertRaises(HTTPException) as erro:
                reserva_service.cadastrar(data)

            self.assertEqual(erro.exception.status_code, 409)

            sessao.delete(reserva_nova)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()
            
            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_reserva_mesmo_material_outro_cliente(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente1 = self.criar_cliente(sessao, "Cliente Reserva 1")
            cliente2 = self.criar_cliente(sessao, "Cliente Reserva 2")
            material, categoria, editora = self.criar_material(sessao)

            reserva1 = self.criar_reserva(
                sessao,
                cliente1.id,
                material.id
            )

            data = SchemaReservaCadastro(
                titulo="Livro Teste",
                cliente_id=cliente2.id,
                material_id=material.id
            )

            reserva2 = reserva_service.cadastrar(data)

            self.assertIsInstance(reserva2, Reserva)
            self.assertEqual(reserva2.cliente_id, cliente2.id)
            self.assertEqual(reserva2.material_id, material.id)

            sessao.delete(reserva1)
            sessao.delete(reserva2)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente1)
            sessao.delete(cliente2)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_reserva(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            lista_reserva = reserva_service.visualizar()

            for reserva in lista_reserva:
                self.assertIsInstance(reserva, Reserva)

        finally:
            sessao.close()

    def test_visualizar_reserva_expirada(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id
            )

            # Simula uma reserva com mais de 10 dias
            reserva.data = datetime.now() - timedelta(days=11)
            sessao.commit()

            reservas_expiradas = reserva_service.visualizar_expiradas()

            self.assertIn(reserva, reservas_expiradas)
            self.assertFalse(reserva.is_active)

            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualizar_reserva_nao_expirada(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id
            )

            reservas_expiradas = reserva_service.visualizar_expiradas()

            self.assertNotIn(reserva, reservas_expiradas)
            self.assertTrue(reserva.is_active)

            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_reserva_ativa(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id
            )

            reserva_service.inativar(reserva.id)

            sessao.refresh(reserva)

            self.assertFalse(reserva.is_active)

            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_reserva_inativa(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao)
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id
            )

            reserva_service.inativar(reserva.id)

            with self.assertRaises(HTTPException) as erro:
                reserva_service.inativar(reserva.id)

            self.assertEqual(erro.exception.status_code, 400)

            sessao.delete(reserva)
            sessao.commit()

            sessao.delete(material)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(cliente)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_reserva_inexistente(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            with self.assertRaises(HTTPException) as erro:
                reserva_service.inativar(0)

            self.assertEqual(erro.exception.status_code, 404)

        finally:
            sessao.close()

    def criar_reserva(self, sessao, cliente_id, material_id):

        reserva_nova = Reserva(
            titulo="Teste Livro",
            cliente_id=cliente_id,
            material_id=material_id
        )

        sessao.add(reserva_nova)
        sessao.commit()
        sessao.refresh(reserva_nova)

        return reserva_nova

    def criar_cliente(self, sessao, nome=None):

        if nome is None:
            nome = "Teste Cliente"

        cliente_novo = Cliente(
            nome=nome,
            bairro="bairro",
            rua="rua",
            numero=1,
            complemento="complemento",
            telefone="123456789"
        )

        sessao.add(cliente_novo)
        sessao.commit()
        sessao.refresh(cliente_novo)

        return cliente_novo

    def criar_categoria(self,sessao):

        categoria_nova = Categoria(
            nome="Teste Categoria"
        )

        sessao.add(categoria_nova)
        sessao.commit()
        sessao.refresh(categoria_nova)

        return categoria_nova

    def criar_editora(self,sessao):

        editora_nova = Editora(
            nome="Teste Editora"
        )

        sessao.add(editora_nova)
        sessao.commit()
        sessao.refresh(editora_nova)

        return editora_nova
    
    def criar_material(self, sessao):

        categoria = self.criar_categoria(sessao)
        editora = self.criar_editora(sessao)
    
        material_novo = Material(
            titulo="Material Teste",
            ano_publi=2015,
            categoria_id=categoria.id,
            editora_id=editora.id,
            tipo="material"
        )

        sessao.add(material_novo)
        sessao.commit()
        sessao.refresh(material_novo)

        return material_novo, categoria, editora
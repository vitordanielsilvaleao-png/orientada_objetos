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

class TestReservaService(unittest.TestCase):

    def test_cadastrar_reserva_corretamente(self):
        sessao = db.session()
        try:
            cliente = self.criar_cliente(sessao, "Cliente Cadastro")
            material, categoria, editora = self.criar_material(sessao)

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            self.assertEqual(reserva.titulo, material.titulo)
            self.assertEqual(reserva.cliente_id, cliente.id)
            self.assertEqual(reserva.material_id, material.id)
            self.assertTrue(reserva.is_active)
            self.assertEqual(material.status, "RESERVADO")

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

    def test_cadastrar_reserva_corretamente_sem_material_disponivel(self):
        sessao = db.session()
        try:
            cliente = self.criar_cliente(sessao, "Cliente Cadastro")
            material, categoria, editora = self.criar_material(sessao)

            material.status = "EMPRESTADO"

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            self.assertEqual(reserva.titulo, material.titulo)
            self.assertEqual(reserva.cliente_id, cliente.id)
            self.assertIsNone(reserva.material_id)
            self.assertTrue(reserva.is_active)
            self.assertEqual(material.status, "EMPRESTADO")

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

    def test_cadastrar_reserva_usuario_inativo(self):
        sessao = db.session()
        try:

            cliente = self.criar_cliente(sessao, "Cliente Inativo")
            material, categoria, editora = self.criar_material(sessao)

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            cliente.inativar_cliente()

            reserva_service = ReservaService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                reserva_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

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

            cliente = self.criar_cliente(sessao, "Cliente Reserva Existente")
            material, categoria, editora = self.criar_material(sessao)

            reserva_nova = self.criar_reserva(
                sessao,
                cliente.id,
                material.id,
                material.titulo
            )

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
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
                material.id,
                material.titulo
            )

            material.status = "RESERVADO"
            sessao.commit()

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente2.id
            )

            reserva2 = reserva_service.cadastrar(data)

            self.assertIsInstance(reserva2, Reserva)
            self.assertEqual(reserva2.cliente_id, cliente2.id)
            self.assertEqual(reserva2.titulo, material.titulo)
            self.assertIsNone(reserva2.material_id)

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

            cliente = self.criar_cliente(sessao, "Cliente Cadastro")
            material, categoria, editora = self.criar_material(sessao)

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            lista_reserva = reserva_service.visualizar()

            for reserva in lista_reserva:
                self.assertIsInstance(reserva, Reserva)

            self.assertIn(reserva, lista_reserva)

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

    def test_visualizar_reserva_expirada(self):
        sessao = db.session()
        try:
            reserva_service = ReservaService(sessao)

            cliente = self.criar_cliente(sessao, "Cliente Reserva Expirada")
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id,
                material.titulo
            )

            reserva.is_active = False
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

            cliente = self.criar_cliente(sessao, "Cliente Reserva Nao Expirada")
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id,
                material.titulo
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

            cliente = self.criar_cliente(sessao, "Cliente Reserva Ativa")
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id,
                material.titulo
            )

            reserva_service.inativar(reserva.id)

            sessao.refresh(reserva)

            self.assertFalse(reserva.is_active)
            self.assertEqual(material.status, "DISPONIVEL")

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

            cliente = self.criar_cliente(sessao, "Cliente Reserva Inativa")
            material, categoria, editora = self.criar_material(sessao)

            reserva = self.criar_reserva(
                sessao,
                cliente.id,
                material.id,
                material.titulo
            )

            reserva_service.inativar(reserva.id)

            with self.assertRaises(HTTPException) as erro:
                reserva_service.inativar(reserva.id)

            self.assertEqual(erro.exception.status_code, 400)

            self.assertEqual(material.status, "DISPONIVEL")

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

    def test_criar_emprestimo_de_reserva_corretamente(self): 
        sessao = db.session()

        try: 
            cliente = self.criar_cliente(sessao, "Cliente Emprestimo") 
            material, categoria, editora = self.criar_material(sessao) 

            data = SchemaReservaCadastro( 
                titulo=material.titulo, 
                cliente_id=cliente.id 
            ) 

            reserva_service = ReservaService(sessao) 

            reserva = reserva_service.cadastrar(data) 

            reserva_apos_emprestimo, emprestimo = reserva_service.atender_reserva(reserva.id) 

            self.assertFalse(reserva_apos_emprestimo.is_active) 
            self.assertIsNotNone(emprestimo)
            self.assertEqual(emprestimo.cliente_id, cliente.id)
            self.assertEqual(emprestimo.material_id, material.id)
            self.assertTrue(emprestimo.is_active)
            self.assertEqual(material.status, "EMPRESTADO")

            sessao.delete(reserva) 
            sessao.delete(emprestimo) 
            sessao.commit() 

            sessao.delete(material) 
            sessao.commit() 

            sessao.delete(categoria) 
            sessao.delete(editora) 

            sessao.delete(cliente) 
            sessao.commit() 
        finally: 
            sessao.close()

    def test_criar_emprestimo_de_reserva_sem_material_disponivel(self):

        sessao = db.session()

        try:
            cliente = self.criar_cliente(sessao, "Cliente Emprestimo Sem Material Disponivel")
            material, categoria, editora = self.criar_material(sessao)

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            material.status = "EMPRESTADO"

            with self.assertRaises(HTTPException) as erro:
                reserva_service.atender_reserva(reserva.id)

            self.assertEqual(erro.exception.status_code, 409)
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

    def test_criar_emprestimo_de_reserva_sem_material(self):

        sessao = db.session()

        try:
            cliente = self.criar_cliente(sessao, "Cliente Emprestimo Sem Material")
            material, categoria, editora = self.criar_material(sessao)
            
            material.status = "EMPRESTADO"

            data = SchemaReservaCadastro(
                titulo=material.titulo,
                cliente_id=cliente.id
            )

            reserva_service = ReservaService(sessao)

            reserva = reserva_service.cadastrar(data)

            with self.assertRaises(HTTPException) as erro:
                reserva_service.atender_reserva(reserva.id)

            self.assertEqual(erro.exception.status_code, 404)
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

    def criar_reserva(self, sessao, cliente_id, material_id, titulo):

        reserva_nova = Reserva(
            titulo= titulo,
            cliente_id=cliente_id,
            material_id=material_id
        )

        sessao.add(reserva_nova)
        sessao.commit()
        sessao.refresh(reserva_nova)

        return reserva_nova

    def criar_cliente(self, sessao, nome):

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
            titulo="material teste",
            ano_publi=2015,
            categoria_id=categoria.id,
            editora_id=editora.id,
        )

        sessao.add(material_novo)
        sessao.commit()
        sessao.refresh(material_novo)

        return material_novo, categoria, editora
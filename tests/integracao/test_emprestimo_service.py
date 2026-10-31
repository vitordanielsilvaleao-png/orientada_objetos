import unittest
from datetime import datetime, timedelta
import random
from fastapi import HTTPException

from src.compartilhado.enum import StatusMaterial, StatusEmprestimo
from src.modulos.material.entidades.editora import Editora
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.livro.entidades.autor import Autor
from src.modulos.reserva.entidade.reserva import Reserva
from src.modulos.emprestimo.entidade.emprestimo import Emprestimo
from src.modulos.cliente.entidade.cliente import Cliente
from src.modulos.livro.entidades.livro import Livro
from src.database.database import db

class TestEmprestimoService(unittest.TestCase):
    def criar_livro(self, sessao):
        autor = Autor(nome=f"Autor {random.randint(1, 999999)}")
        categoria = Categoria(nome=f"Categoria {random.randint(1, 999999)}")
        editora = Editora(nome=f"Editora {random.randint(1, 999999)}")
        sessao.add_all([autor, categoria, editora])
        sessao.commit()

        livro = Livro(
            titulo=f"Livro {random.randint(1, 999999)}",
            isbn=str(random.randint(1000000000000, 9999999999999)),
            paginas=100,
            autor_id=autor.id,
            categoria_id=categoria.id,
            editora_id=editora.id
        )
        sessao.add(livro)
        sessao.commit()
        return livro, categoria, editora, autor

    def criar_cliente(self, sessao):
        cliente_novo = Cliente(
            cpf=f"{random.randint(0, 99999999999):011d}",
            nome=f"Teste Emprestimo {random.randint(1, 999999)}",
            bairro="Centro",
            rua="Afonso Pena",
            numero=100,
            telefone="34999999999"
        )
        sessao.add(cliente_novo)
        sessao.commit()
        return cliente_novo

    def test_cadastrar_emprestimo_com_sucesso(self):
        sessao = db.session()
        try:
            cliente = self.criar_cliente(sessao)
            livro, categoria, editora, autor = self.criar_livro(sessao)

            data = SchemaEmprestimoCadastro if 'SchemaEmprestimoCadastro' in globals() else None
            # Usando import local ou direto
            from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro

            dados = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=livro.id
            )

            emprestimo_service = EmprestimoService(sessao) if 'EmprestimoService' in globals() else None
            from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService
            emprestimo_service = EmprestimoService(sessao)

            emprestimo = emprestimo_service.cadastrar(dados)

            self.assertIsNotNone(emprestimo.id)
            self.assertEqual(emprestimo.status, StatusEmprestimo.ABERTO)
            self.assertEqual(emprestimo.data_devolucao, None)
            self.assertEqual(livro.status, StatusMaterial.EMPRESTADO)

            sessao.delete(emprestimo)
            sessao.delete(livro)
            sessao.delete(cliente)
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

            from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro
            from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService

            data = SchemaEmprestimoCadastro(
                cliente_id=cliente.id,
                material_id=2147483647,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 404)

            sessao.delete(cliente)
            sessao.commit()
        finally:
            sessao.close()

    def test_cadastrar_emprestimo_cliente_inexistente(self):
        sessao = db.session()
        try:
            livro, categoria, editora, autor = self.criar_livro(sessao)

            from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro
            from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService

            data = SchemaEmprestimoCadastro(
                cliente_id=2147483647,
                material_id=livro.id,
            )

            emprestimo_service = EmprestimoService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                emprestimo_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 404)

            sessao.delete(livro)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()
        finally:
            sessao.close()
import unittest
import random

from fastapi import HTTPException

from src.modulos.material.schemas.schemas_categoria import SchemaCategoriaCadastro, SchemaCategoriaAtualizacao
from src.modulos.material.service.categoria_service import CategoriaService
from src.modulos.material.entidades.categoria import Categoria
from src.database.database import db


class TestCategoriaService(unittest.TestCase):

    def test_cadastrar_categoria_corretamente(self):
        sessao = db.session()
        try:
            nome_cadastro = f"Teste Cadastro Categoria {random.randint(1, 999999)}"

            data = SchemaCategoriaCadastro(nome=nome_cadastro)

            categoria_service = CategoriaService(sessao)

            categoria = categoria_service.cadastrar(data)

            self.assertEqual(categoria.nome, nome_cadastro)

            sessao.delete(categoria)
            sessao.commit()
        finally:
            sessao.close()

    def test_cadastrar_categoria_com_nome_vazio(self):
        sessao = db.session()
        try:

            data = SchemaCategoriaCadastro(nome=" ")

            categoria_service = CategoriaService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                categoria_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 400)

        finally:
            sessao.close()

    def test_cadastrar_categoria_com_nome_normalizado_duplicado(self):
        sessao = db.session()
        try:

            categoria_service = CategoriaService(sessao)

            categoria_existente = self.criar_categoria(sessao)
            categoria_existente.nome = "Ficção"
            sessao.commit()

            data = SchemaCategoriaCadastro(nome="ficçao")

            with self.assertRaises(HTTPException) as contexto:
                categoria_service.cadastrar(data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(categoria_existente)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_categorias(self):
        sessao = db.session()
        try:
            categoria_nova = self.criar_categoria(sessao)

            categoria_service = CategoriaService(sessao)

            lista_categoria = categoria_service.visualizar()

            self.assertIn(categoria_nova, lista_categoria)

            for categoria in lista_categoria:
                self.assertIsInstance(categoria, Categoria)

            sessao.delete(categoria_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualiza_categoria(self):
        sessao = db.session()
        try:
            categoria_service = CategoriaService(sessao)

            categoria_nova = self.criar_categoria(sessao)

            novo_nome = f"Teste Atualizar Categoria {random.randint(1, 999999)}"

            data = SchemaCategoriaAtualizacao(nome=novo_nome)

            categoria_service.atualizar(categoria_nova.id, data)
            sessao.refresh(categoria_nova)

            self.assertEqual(categoria_nova.nome, novo_nome)

            sessao.delete(categoria_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualiza_categoria_inexistente(self):
        sessao = db.session()
        try:
            categoria_service = CategoriaService(sessao)

            data = SchemaCategoriaAtualizacao(nome="Categoria Inexistente")

            with self.assertRaises(HTTPException) as contexto:
                categoria_service.atualizar(0, data)

            self.assertEqual(contexto.exception.status_code, 404)

        finally:
            sessao.close()

    def test_atualiza_categoria_com_nome_vazio(self):
        sessao = db.session()
        try:

            categoria = self.criar_categoria(sessao)

            data = SchemaCategoriaAtualizacao(nome=" ")

            categoria_service = CategoriaService(sessao)

            with self.assertRaises(HTTPException) as contexto:
                categoria_service.atualizar(categoria.id, data)

            self.assertEqual(contexto.exception.status_code, 400)

            sessao.delete(categoria)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualiza_categoria_com_nome_duplicado(self):
        sessao = db.session()
        try:
            categoria_service = CategoriaService(sessao)

            categoria_um = self.criar_categoria(sessao)
            categoria_um.nome = "Ficção"

            categoria_dois = self.criar_categoria(sessao)
            categoria_dois.nome = "Romance"

            sessao.commit()

            data = SchemaCategoriaAtualizacao(nome="ficçao")

            with self.assertRaises(HTTPException) as contexto:
                categoria_service.atualizar(categoria_dois.id, data)

            self.assertEqual(contexto.exception.status_code, 409)

            sessao.delete(categoria_um)
            sessao.delete(categoria_dois)
            sessao.commit()

        finally:
            sessao.close()

    def criar_categoria(self, sessao):
        categoria_nova = Categoria(
            nome=f"Categoria Base {random.randint(1, 999999)}"
        )

        sessao.add(categoria_nova)
        sessao.commit()
        sessao.refresh(categoria_nova)
        return categoria_nova


if __name__ == "__main__":
    unittest.main()
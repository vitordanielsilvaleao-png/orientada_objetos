import unittest
import random

from fastapi import HTTPException

from src.modulos.livro.schemas.schemas_livro import SchemaLivroCadastro, SchemaLivroAtualizacao
from src.modulos.livro.services.livro_service import LivroService
from src.modulos.livro.entidades.livro import Livro
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.material.entidades.editora import Editora
from src.modulos.livro.entidades.autor import Autor
from src.database.database import db

class TestLivroService(unittest.TestCase):

    def test_cadastrar_livro_corretamente(self):
        sessao = db.session()
        try:

            isbn = random.randint(1111111111111, 9999999999999)

            categoria = self.criar_categoria(sessao)
            editora = self.criar_editora(sessao)
            autor = self.criar_autor(sessao)

            data = SchemaLivroCadastro(
                titulo = "Teste Cadastro Livro",
                ano_publi = 2026,
                editora_id = editora.id,
                categoria_id = categoria.id,
                autor_id = autor.id,
                isbn = str(isbn)
            )

            livro_service = LivroService(sessao)

            livro = livro_service.cadastrar(data)

            self.assertEqual(livro.titulo, "teste cadastro livro")
            self.assertEqual(livro.ano_publi, 2026)
            self.assertEqual(livro.editora_id, editora.id)
            self.assertEqual(livro.categoria_id, categoria.id)
            self.assertEqual(livro.autor_id, autor.id)
            self.assertEqual(livro.isbn, str(isbn))

            sessao.delete(livro)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_livro_sem_editora(self):
        sessao = db.session()
        try:
            data = SchemaLivroCadastro(
                titulo = "teste cadastro livro",
                ano_publi = 2026,
                editora_id = 0,
                categoria_id = 1,
                autor_id = 1,
                isbn = "8579632584567"
            )

            livro_service = LivroService(sessao)

            with self.assertRaises(HTTPException):
                livro_service.cadastrar(data)
        finally:
            sessao.close()

    def test_cadastrar_livro_sem_categoria(self):
        sessao = db.session()
        try:
            data = SchemaLivroCadastro(
                titulo = "teste cadastro livro",
                ano_publi = 2026,
                editora_id = 1,
                categoria_id = 0,
                autor_id = 1,
                isbn = "8579632584567"
            )

            livro_service = LivroService(sessao)

            with self.assertRaises(HTTPException):
                livro_service.cadastrar(data)
        finally:
            sessao.close()

    def test_cadastrar_livro_sem_autor(self):
        sessao = db.session()
        try:
            data = SchemaLivroCadastro(
                titulo = "Teste Cadastro Livro",
                ano_publi = 2026,
                editora_id = 1,
                categoria_id = 1,
                autor_id = 0,
                isbn = "8579632584567"
            )

            livro_service = LivroService(sessao)

            with self.assertRaises(HTTPException):
                livro_service.cadastrar(data)
        finally:
            sessao.close()

    def test_visualiza_livros(self):
        sessao = db.session()
        try:

            livro, categoria, editora, autor = self.criar_livro(sessao)

            livro_service = LivroService(sessao)

            lista_livro = livro_service.visualizar()

            for livro in lista_livro:
                self.assertIsInstance(livro, Livro)

            sessao.delete(livro)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualiza_livro(self):
        sessao = db.session()
        try:

            livro_service = LivroService(sessao)


            livro_novo, categoria, editora, autor = self.criar_livro(sessao)

            data = SchemaLivroAtualizacao(
                titulo="Teste Atualizar Livro 1",
                ano_publi=2026,
                editora_id=editora.id,
                categoria_id=categoria.id,
                autor_id=autor.id
            )

            livro_service.atualizar(livro_novo.id, data)
            sessao.refresh(livro_novo)

            self.assertEqual(livro_novo.titulo, "teste atualizar livro 1")
            self.assertEqual(livro_novo.ano_publi, 2026)
            self.assertEqual(livro_novo.editora_id, editora.id)
            self.assertEqual(livro_novo.categoria_id, categoria.id)
            self.assertEqual(livro_novo.autor_id, autor.id)

            sessao.delete(livro_novo)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_livro_ativo(self):
        sessao = db.session()
        try:
            livro_service = LivroService(sessao)

            livro_novo, categoria, editora, autor = self.criar_livro(sessao)

            livro_service.inativar(livro_novo.id)

            sessao.refresh(livro_novo)

            self.assertFalse(livro_novo.is_active)

            sessao.delete(livro_novo)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_livro_inexistente(self):
        sessao = db.session()
        try:
            livro_service = LivroService(sessao)

            with self.assertRaises(HTTPException):
                livro_service.inativar(0)
        finally:
            sessao.close()

    def test_ativar_livro_inativo(self):
        sessao = db.session()
        try:
            livro_service = LivroService(sessao)

            livro_novo, categoria, editora, autor = self.criar_livro(sessao)
            livro_novo.inativar()

            livro_service.ativar(livro_novo.id)

            sessao.refresh(livro_novo)

            self.assertTrue(livro_novo.is_active)

            sessao.delete(livro_novo)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_ativar_livro_inexistente(self):
        sessao = db.session()
        try:
            livro_service = LivroService(sessao)

            with self.assertRaises(HTTPException):
                livro_service.ativar(0)
        finally:
            sessao.close()

    def criar_categoria(self,sessao):

        num = random.randint(1, 999999)

        categoria_nova = Categoria(
            nome=f"Teste Categoria{num}"
        )

        sessao.add(categoria_nova)
        sessao.commit()
        sessao.refresh(categoria_nova)

        return categoria_nova

    def criar_editora(self,sessao):

        num = random.randint(1, 999999)

        editora_nova = Editora(
            nome=f"Teste Editora{num}"
        )

        sessao.add(editora_nova)
        sessao.commit()
        sessao.refresh(editora_nova)

        return editora_nova

    def criar_autor(self,sessao):

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
            isbn= str(isbn))

        sessao.add(livro_novo)
        sessao.commit()
        sessao.refresh(livro_novo)
        return livro_novo, categoria, editora, autor
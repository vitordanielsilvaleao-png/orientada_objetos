import unittest
import random

from fastapi import HTTPException

from src.modulos.material.entidades.categoria import Categoria
from src.modulos.material.entidades.editora import Editora
from src.modulos.revista.schemas.schamas_revista import (SchemaRevistaCadastro, SchemaRevistaAtualizacao)
from src.modulos.revista.service.revista_service import RevistaService
from src.modulos.revista.revista import Revista
from src.database.database import db


class TestRevistaService(unittest.TestCase):

    def test_cadastrar_revista_corretamente(self):
        sessao = db.session()

        try:
            issn = str(random.randint(10000000, 99999999))

            editora = self.criar_editora(sessao)
            categoria = self.criar_categoria(sessao)

            data = SchemaRevistaCadastro(
                titulo="Teste Cadastro Revista",
                ano_publi=2026,
                editora_id=editora.id,
                categoria_id=categoria.id,
                issn=issn,
                edicao=1
            )

            revista_service = RevistaService(sessao)

            revista = revista_service.cadastrar(data)

            self.assertEqual(revista.titulo, "teste cadastro revista")
            self.assertEqual(revista.ano_publi, 2026)
            self.assertEqual(revista.editora_id, editora.id)
            self.assertEqual(revista.categoria_id, categoria.id)
            self.assertEqual(revista.issn, issn)
            self.assertEqual(revista.edicao, 1)

            sessao.delete(revista)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_revista_sem_editora(self):
        sessao = db.session()

        try:
            data = SchemaRevistaCadastro(
                titulo="Teste Revista",
                ano_publi=2026,
                editora_id=0,
                categoria_id=1,
                issn=str(random.randint(10000000, 99999999)),
                edicao=1
            )

            revista_service = RevistaService(sessao)

            with self.assertRaises(HTTPException):
                revista_service.cadastrar(data)

        finally:
            sessao.close()

    def test_cadastrar_revista_sem_categoria(self):
        sessao = db.session()

        try:
            data = SchemaRevistaCadastro(
                titulo="Teste Revista",
                ano_publi=2026,
                editora_id=1,
                categoria_id=0,
                issn=str(random.randint(10000000, 99999999)),
                edicao=1
            )

            revista_service = RevistaService(sessao)

            with self.assertRaises(HTTPException):
                revista_service.cadastrar(data)

        finally:
            sessao.close()

    def test_visualizar_revistas(self):
        sessao = db.session()

        try:

            revista, categoria, editora = self.criar_revista(sessao)

            revista_service = RevistaService(sessao)

            lista_revistas = revista_service.visualizar()

            for revista in lista_revistas:
                self.assertIsInstance(revista, Revista)

            sessao.delete(revista)
            sessao.commit()

            sessao.delete(editora)
            sessao.delete(categoria)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualizar_revista(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            revista_nova, categoria, editora = self.criar_revista(sessao)

            data = SchemaRevistaAtualizacao(
                titulo="Teste Atualizar Revista",
                ano_publi=2026,
                editora_id=editora.id,
                categoria_id=categoria.id,
                edicao=10
            )

            revista_service.atualizar(revista_nova.id, data)

            sessao.refresh(revista_nova)

            self.assertEqual(
                revista_nova.titulo,
                "teste atualizar revista"
            )
            self.assertEqual(revista_nova.ano_publi, 2026)
            self.assertEqual(revista_nova.editora_id, editora.id)
            self.assertEqual(revista_nova.categoria_id, categoria.id)
            self.assertEqual(revista_nova.edicao, 10)

            sessao.delete(revista_nova)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_revista_ativa(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            revista_nova, categoria, editora = self.criar_revista(sessao)

            revista_service.inativar(revista_nova.id)

            sessao.refresh(revista_nova)

            self.assertFalse(revista_nova.is_active)

            sessao.delete(revista_nova)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_revista_inexistente(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            with self.assertRaises(HTTPException):
                revista_service.inativar(0)

        finally:
            sessao.close()

    def test_ativar_revista_inativa(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            revista_nova, categoria, editora = self.criar_revista(sessao)

            revista_nova.inativar()
            sessao.commit()

            revista_service.ativar(revista_nova.id)

            sessao.refresh(revista_nova)

            self.assertTrue(revista_nova.is_active)

            sessao.delete(revista_nova)
            sessao.commit()

            sessao.delete(categoria)
            sessao.delete(editora)
            sessao.commit()

        finally:
            sessao.close()

    def test_ativar_revista_inexistente(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            with self.assertRaises(HTTPException):
                revista_service.ativar(0)

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

    def criar_revista(self, sessao):

        categoria = self.criar_categoria(sessao)
        editora = self.criar_editora(sessao)

        issn = str(random.randint(10000000, 99999999))

        revista_nova = Revista(
            titulo="teste revista",
            ano_publi=1988,
            editora_id=editora.id,
            categoria_id=categoria.id,
            issn=issn,
            edicao=1
        )

        sessao.add(revista_nova)
        sessao.commit()
        sessao.refresh(revista_nova)

        return revista_nova, categoria, editora

if __name__ == "__main__":
    unittest.main()

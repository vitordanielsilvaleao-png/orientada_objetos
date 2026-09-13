import unittest
import random

from fastapi import HTTPException

from src.modulos.revista.schemas.schamas_revista import (
    SchemaRevistaCadastro,
    SchemaRevistaAtualizacao
)
from src.modulos.revista.service.revista_service import RevistaService
from src.modulos.revista.revista import Revista
from src.database.database import db


class TestRevistaService(unittest.TestCase):

    def test_cadastrar_revista_corretamente(self):
        sessao = db.session()

        try:
            issn = str(random.randint(10000000, 99999999))

            data = SchemaRevistaCadastro(
                titulo="Teste Cadastro Revista",
                ano_publi=2026,
                editora_id=1,
                categoria_id=1,
                issn=issn,
                edicao=1
            )

            revista_service = RevistaService(sessao)

            revista = revista_service.cadastrar(data)

            self.assertEqual(revista.titulo, "Teste Cadastro Revista")
            self.assertEqual(revista.ano_publi, 2026)
            self.assertEqual(revista.editora_id, 1)
            self.assertEqual(revista.categoria_id, 1)
            self.assertEqual(revista.issn, issn)
            self.assertEqual(revista.edicao, 1)

            sessao.delete(revista)
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
            revista_service = RevistaService(sessao)

            lista_revistas = revista_service.visualizar()

            for revista in lista_revistas:
                self.assertIsInstance(revista, Revista)

        finally:
            sessao.close()

    def test_atualizar_revista(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            revista_nova = self.criar_revista(sessao)

            data = SchemaRevistaAtualizacao(
                titulo="Teste Atualizar Revista",
                ano_publi=2026,
                editora_id=1,
                categoria_id=1,
                edicao=10
            )

            revista_service.atualizar(revista_nova.id, data)

            sessao.refresh(revista_nova)

            self.assertEqual(
                revista_nova.titulo,
                "Teste Atualizar Revista"
            )
            self.assertEqual(revista_nova.ano_publi, 2026)
            self.assertEqual(revista_nova.editora_id, 1)
            self.assertEqual(revista_nova.categoria_id, 1)
            self.assertEqual(revista_nova.edicao, 10)

            sessao.delete(revista_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_inativar_revista_ativa(self):
        sessao = db.session()

        try:
            revista_service = RevistaService(sessao)

            revista_nova = self.criar_revista(sessao)

            revista_service.inativar(revista_nova.id)

            sessao.refresh(revista_nova)

            self.assertFalse(revista_nova.is_active)

            sessao.delete(revista_nova)
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

            revista_nova = self.criar_revista(sessao)

            revista_nova.inativar()
            sessao.commit()

            revista_service.ativar(revista_nova.id)

            sessao.refresh(revista_nova)

            self.assertTrue(revista_nova.is_active)

            sessao.delete(revista_nova)
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

    def criar_revista(self, sessao):

        issn = str(random.randint(10000000, 99999999))

        revista_nova = Revista(
            titulo="Teste Revista",
            ano_publi=2025,
            editora_id=1,
            categoria_id=1,
            issn=issn,
            edicao=1
        )

        sessao.add(revista_nova)
        sessao.commit()
        sessao.refresh(revista_nova)

        return revista_nova


if __name__ == "__main__":
    unittest.main()

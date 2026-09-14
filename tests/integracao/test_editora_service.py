import unittest
from fastapi import HTTPException

from schemas.schemas_editora import SchemaEditoraCadastro
from src.modulos.material.service.editora_service import EditoraService
from src.modulos.material.entidades.editora import Editora
from src.database.database import db


class TestEditoraService(unittest.TestCase):

    def test_cadastrar_editora(self):
        sessao = db.session()

        try:

            data = SchemaEditoraCadastro(nome="Editora")

            editora_service = EditoraService(sessao)
            editora = editora_service.cadastrar(data)

            self.assertEqual(editora.nome, "Editora")

            sessao.delete(editora)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_editora_existente(self):
        sessao = db.session()

        try:

            editora_nova = self.criar_editora(sessao)

            data = SchemaEditoraCadastro(nome=editora_nova.nome)

            editora_service = EditoraService(sessao)

            with self.assertRaises(HTTPException):
                editora_service.cadastrar(data)

            sessao.delete(editora_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_editoras(self):
        sessao = db.session()

        try:

            editora_service = EditoraService(sessao)

            lista_editora = editora_service.visualizar()

            for editora in lista_editora:
                self.assertIsInstance(editora, Editora)

        finally:
            sessao.close()

    def test_atualiza_editora(self):
        sessao = db.session()

        try:

            editora_service = EditoraService(sessao)

            editora_nova = self.criar_editora(sessao)

            data = "Editora Atualizada"

            editora_service.atualizar(editora_nova.id, data)

            sessao.refresh(editora_nova)

            self.assertEqual(
                editora_nova.nome,
                "Editora Atualizada"
            )

            sessao.delete(editora_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualizar_editora_id_invalido(self):
        sessao = db.session()

        try:

            editora_service = EditoraService(sessao)

            editora_nova = self.criar_editora(sessao)

            data = "Editora Atualizada"

            with self.assertRaises(HTTPException):
                editora_service.atualizar(250, data)

            sessao.delete(editora_nova)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualizar_editora_ja_existente(self):
        sessao = db.session()

        try:

            editora_service = EditoraService(sessao)

            editora_nova = self.criar_editora(sessao)
            editora_para_atualizar = self.criar_editora_para_atualizacao(
                sessao
            )

            data = editora_nova.nome

            with self.assertRaises(HTTPException):
                editora_service.atualizar(
                    editora_para_atualizar.id,
                    data
                )

            sessao.delete(editora_nova)
            sessao.delete(editora_para_atualizar)
            sessao.commit()

        finally:
            sessao.close()

    def criar_editora(self, sessao):

        editora_nova = Editora(
            nome="Editora"
        )

        sessao.add(editora_nova)
        sessao.commit()
        sessao.refresh(editora_nova)

        return editora_nova

    def criar_editora_para_atualizacao(self, sessao):

        editora_nova = Editora(
            nome="Atualizar Editora"
        )

        sessao.add(editora_nova)
        sessao.commit()
        sessao.refresh(editora_nova)

        return editora_nova


if __name__ == "__main__":
    unittest.main()
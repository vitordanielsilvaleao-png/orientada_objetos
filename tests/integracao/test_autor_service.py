import unittest
from fastapi import HTTPException

from src.modulos.livro.schemas.schemas_autor import SchemaAutorCadastro
from src.modulos.livro.services.autor_service import AutorService
from src.modulos.livro.entidades.autor import Autor
from src.database.database import db

class TestAutorService(unittest.TestCase):

    def test_cadastrar_autor(self):
        sessao = db.session()

        try:

            data = SchemaAutorCadastro(nome="Autor1")

            autor_service = AutorService(sessao)
            autor = autor_service.cadastrar(data)

            self.assertEqual(autor.nome, "Autor1")

            sessao.delete(autor)
            sessao.commit()

        finally:
            sessao.close()

    def test_cadastrar_autor_existente(self):
        sessao = db.session()

        try:

            autor_novo = self.criar_autor(sessao)
            
            data = SchemaAutorCadastro(nome=autor_novo.nome)

            autor_service = AutorService(sessao)

            with self.assertRaises(HTTPException):
                autor_service.cadastrar(data)

            sessao.delete(autor_novo)
            sessao.commit()

        finally:
            sessao.close()

    def test_visualiza_autores(self):
        sessao = db.session()

        try:

            autor_service = AutorService(sessao)
        
            lista_autor = autor_service.visualizar()
        
            for autor in lista_autor:
                self.assertIsInstance(autor, Autor)

        finally:
            sessao.close()

    def test_atualiza_autor(self):
        sessao = db.session()

        try:
        
            autor_service = AutorService(sessao)
        
            autor_novo = self.criar_autor(sessao)
        
            data = "Autor Atualizado"
        
            autor_service.atualizar(autor_novo.id, data)
            sessao.refresh(autor_novo)
        
            self.assertEqual(autor_novo.nome, "Autor Atualizado")
        
            sessao.delete(autor_novo)
            sessao.commit()

        finally:
            sessao.close()

    def test_atualizar_autor_id_invalido(self):
        sessao = db.session()

        try:

            autor_service = AutorService(sessao)
                    
            autor_novo = self.criar_autor(sessao)
                    
            data = "Atualiza Autor"

            with self.assertRaises(HTTPException):
                autor_service.atualizar(250, data)

            sessao.delete(autor_novo)
            sessao.commit()
            
        finally:
            sessao.close()

    def test_atualizar_autor_ja_existente(self):
        sessao = db.session()

        try:

            autor_service = AutorService(sessao)
                    
            autor_novo = self.criar_autor(sessao)
            autor_para_atualizar = self.criar_autor_para_atualizacao(sessao)
                    
            data = autor_novo.nome

            with self.assertRaises(HTTPException):
                autor_service.atualizar(autor_para_atualizar.id, data)

            sessao.delete(autor_novo)
            sessao.delete(autor_para_atualizar)
            sessao.commit()
            
        finally:
            sessao.close()

    def criar_autor(self, sessao):

       autor_novo = Autor(
           nome="Autor1"
       )

       sessao.add(autor_novo)
       sessao.commit()
       sessao.refresh(autor_novo)
       return autor_novo

    def criar_autor_para_atualizacao(self, sessao):
        autor_novo = Autor(
            nome="Atualizar Autor"
        )

        sessao.add(autor_novo)
        sessao.commit()
        sessao.refresh(autor_novo)
        return autor_novo
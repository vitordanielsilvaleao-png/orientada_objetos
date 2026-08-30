#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from fastapi import HTTPException
from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService
from modulos.livro.schemas.schemas_livro import SchemaLivroCadastro, SchemaLivroAtualizacao
from modulos.livro.entidades.autor import Autor
from modulos.material.entidades.editora import Editora
from modulos.material.entidades.categoria import Categoria
from modulos.livro.entidades.livro import Livro

#Declaração da classe LivroService
class LivroService(BaseService):

    #Declaração do construtor da classe LivroService
     def __init__(self, session:Session):
         super().__init__(session)

    #Método para cadastrar livros
     def cadastrar(self, data:SchemaLivroCadastro):

         autor_cadastrar = self.session.query(Autor).filter_by(
             id = data.autor_id
         ).first()

         editora_cadastrar = self.session.query(Editora).filter_by(
             id = data.editora_id
         ).first()

         categoria_cadastrar = self.session.query(Categoria).filter_by(
             id = data.categoria_id
         ).first()

         if not autor_cadastrar:
             raise HTTPException(
                 status_code=404,
                 detail="O autor_cadastrar informado não existe"
             )

         if not editora_cadastrar:
             raise HTTPException(
                 status_code=404,
                 detail="A editora_cadastrar informada não existe"
             )

         if not categoria_cadastrar:
             raise HTTPException(
                 status_code=404,
                 detail="A categoria_cadastrar informada não existe"
             )

         livro_cadastrar = Livro(
             titulo = data.titulo,
             ano_publi = data.ano_publi,
             autor_id = data.autor_id,
             editora_id = data.editora_id,
             categoria_id = data.categoria_id,
             isbn = data.isbn
         )

         self.salvar(livro_cadastrar)
         self.session.refresh(livro_cadastrar)
         return livro_cadastrar

    #Método para visualizar livros
     def visualizar(self):

         return self.session.query(Livro).all()

    #Método para atualizar livros
     def atualizar(self, id:int, data:SchemaLivroAtualizacao):

         livro_atualizar = self.session.query(Livro).filter_by(
             id = id
         ).first()

         if not livro_atualizar:
             raise HTTPException(
                 status_code=404,
                 detail="Livro não encontrado"
             )

         livro_atualizar.atualizar(
             titulo = data.titulo,
             ano_publi = data.ano_publi,
             autor_id = data.autor_id,
             editora_id = data.editora_id,
             categoria_id = data.categoria_id
         )

         self.session.commit()

    #Método para inativar livros
     def inativar(self, id:int):

         livro_inativar = self.session.query(Livro).filter_by(
             id=id
         ).first()

         if not livro_inativar:
             raise HTTPException(
                 status_code=404,
                 detail="Livro não encontrado"
             )

         livro_inativar.inativar()
         self.session.commit()

    #Método para ativar livros
     def ativar(self, id: int):

         livro_ativar = self.session.query(Livro).filter_by(
             id=id
         ).first()

         if not livro_ativar:
             raise HTTPException(
                 status_code=404,
                 detail="Livro não encontrado"
             )

         livro_ativar.ativar()
         self.session.commit()
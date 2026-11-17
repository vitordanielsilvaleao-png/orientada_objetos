#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.modulos.reserva.entidade.reserva import Reserva
from src.compartilhado.base_service import BaseService
from src.modulos.livro.schemas.schemas_livro import SchemaLivroCadastro, SchemaLivroAtualizacao
from src.modulos.livro.entidades.autor import Autor
from src.modulos.material.entidades.editora import Editora
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.livro.entidades.livro import Livro

#Declaração da classe LivroService
class LivroService(BaseService):

    #Método para cadastrar livros
    def cadastrar(self, data:SchemaLivroCadastro):

        isbn_normalizado = Livro.normalizar_isbn(data.isbn)

        isbn_existente = self.session.query(Livro).filter_by(
            isbn = isbn_normalizado
        ).first()

        if isbn_existente:
            raise HTTPException(
                status_code=409,
                detail="O ISBN informado já está cadastrado no sistema"
            )

        self._validar_autor_editora_categoria(data.autor_id, data.editora_id, data.categoria_id)

        try:
            livro_cadastrar = Livro(
                titulo = data.titulo,
                ano_publi = data.ano_publi,
                autor_id = data.autor_id,
                editora_id = data.editora_id,
                categoria_id = data.categoria_id,
                isbn = isbn_normalizado
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(livro_cadastrar)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="O ISBN informado já está cadastrado no sistema"
            )

        self.session.refresh(livro_cadastrar)

        reserva_pendente = (
            self.session.query(Reserva)
            .filter(
                Reserva.titulo == livro_cadastrar.titulo,
                Reserva.is_active == True,
                Reserva.material_id.is_(None)
            )
            .order_by(Reserva.data.asc())
            .first()
        )

        if not reserva_pendente:
            livro_cadastrar.disponibilizar()
        else:
            livro_cadastrar.reservar()
            reserva_pendente.vincular_material(livro_cadastrar.id)

        self.session.commit()
        self.session.refresh(livro_cadastrar)

        return livro_cadastrar

    #Método auxiliar para buscar um livro pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, livro_id: int) -> Livro:
        livro = self.session.query(Livro).filter_by(
            id = livro_id
        ).first()

        if not livro:
            raise HTTPException(
                status_code=404,
                detail="Livro não encontrado"
            )

        return livro

    #Método auxiliar para validar se o autor, a editora e a categoria informados existem, lançando 404 caso não existam
    def _validar_autor_editora_categoria(self, autor_id: int | None, editora_id: int | None, categoria_id: int | None):

        if autor_id is not None:
            autor_existente = self.session.query(Autor).filter_by(
                id = autor_id
            ).first()

            if not autor_existente:
                raise HTTPException(
                    status_code=404,
                    detail="O autor informado não existe"
                )

        if editora_id is not None:
            editora_existente = self.session.query(Editora).filter_by(
                id = editora_id
            ).first()

            if not editora_existente:
                raise HTTPException(
                    status_code=404,
                    detail="A editora informada não existe"
                )

        if categoria_id is not None:
            categoria_existente = self.session.query(Categoria).filter_by(
                id = categoria_id
            ).first()

            if not categoria_existente:
                raise HTTPException(
                    status_code=404,
                    detail="A categoria informada não existe"
                )

    #Método para visualizar livros
    def visualizar(self):

        return self.session.query(Livro).all()

    #Método para atualizar livros
    def atualizar(self, livro_id:int, data:SchemaLivroAtualizacao):

        livro_atualizar = self._buscar_por_id(livro_id)

        self._validar_autor_editora_categoria(data.autor_id, data.editora_id, data.categoria_id)

        try:
            livro_atualizar.atualizar(
                titulo = data.titulo,
                ano_publi = data.ano_publi,
                autor_id = data.autor_id,
                editora_id = data.editora_id,
                categoria_id = data.categoria_id
            )

            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(livro_atualizar)
        return livro_atualizar

    #Método para inativar livros
    def inativar(self, livro_id:int):

        livro_inativar = self._buscar_por_id(livro_id)

        try:
            livro_inativar.inativar()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(livro_inativar)
        return livro_inativar

    #Método para ativar livros
    def ativar(self, livro_id: int):

        livro_ativar = self._buscar_por_id(livro_id)

        try:
            livro_ativar.ativar()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(livro_ativar)
        return livro_ativar

#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.modulos.livro.schemas.schemas_autor import SchemaAutorCadastro, SchemaAutorAtualizacao
from src.modulos.livro.entidades.autor import Autor
from src.compartilhado.base_service import BaseService

#Declaração da classe AutorService
class AutorService(BaseService):

    #Método para cadastrar autores
    def cadastrar(self, data:SchemaAutorCadastro):
        nome_normalizado = Autor.normalizar_nome(data.nome)

        autor_existente = self.session.query(Autor).filter_by(nome=nome_normalizado).first()
        if autor_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um autor cadastrado com este nome."
            )

        try:
            novo_autor = Autor(
                nome=nome_normalizado
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(novo_autor)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe um autor cadastrado com este nome."
            )

        self.session.refresh(novo_autor)
        return novo_autor

    #Método auxiliar para buscar um autor pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, autor_id: int) -> Autor:
        autor = self.session.query(Autor).filter_by(id=autor_id).first()

        if not autor:
            raise HTTPException(
                status_code=404,
                detail="Autor não encontrado."
            )

        return autor

    #Método para visualizar autores
    def visualizar(self):
        return self.session.query(Autor).all()

    #Método para atualizar autor
    def atualizar(self, autor_id: int, data: SchemaAutorAtualizacao):
        autor_atualizar = self._buscar_por_id(autor_id)

        nome_normalizado = Autor.normalizar_nome(data.nome)

        nome_existente = self.session.query(Autor).filter_by(nome=nome_normalizado).first()
        if nome_existente and nome_existente.id != autor_id:
            raise HTTPException(
                status_code=409,
                detail="Já existe outro autor cadastrado com este nome."
            )

        try:
            autor_atualizar.renomear(nome_normalizado)
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe outro autor cadastrado com este nome."
            )

        self.session.refresh(autor_atualizar)
        return autor_atualizar

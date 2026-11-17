#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.modulos.material.schemas.schemas_categoria import (
    SchemaCategoriaCadastro,
    SchemaCategoriaAtualizacao
)
from src.modulos.material.entidades.categoria import Categoria
from src.compartilhado.base_service import BaseService


#Declaração da classe CategoriaService
class CategoriaService(BaseService):

    # Método para cadastrar categorias
    def cadastrar(self, data: SchemaCategoriaCadastro):

        nome_normalizado = Categoria.normalizar_nome(data.nome)

        categoria_existente = self.session.query(Categoria).filter_by(
            nome=nome_normalizado
        ).first()

        if categoria_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma categoria cadastrada com esse nome"
            )

        try:
            categoria_cadastrar = Categoria(
                nome=nome_normalizado
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(categoria_cadastrar)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe uma categoria cadastrada com esse nome"
            )

        self.session.refresh(categoria_cadastrar)

        return categoria_cadastrar

    # Método auxiliar para buscar uma categoria pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, categoria_id: int) -> Categoria:
        categoria = self.session.query(Categoria).filter_by(
            id=categoria_id
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada"
            )

        return categoria

    # Método para visualizar categorias
    def visualizar(self):

        return self.session.query(Categoria).all()

    # Método para atualizar categorias
    def atualizar(
        self,
        categoria_id: int,
        data: SchemaCategoriaAtualizacao
    ):

        categoria_atualizar = self._buscar_por_id(categoria_id)

        nome_normalizado = Categoria.normalizar_nome(data.nome)

        categoria_existente = self.session.query(Categoria).filter(
            Categoria.nome == nome_normalizado,
            Categoria.id != categoria_id
        ).first()

        if categoria_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma categoria cadastrada com esse nome"
            )

        try:
            categoria_atualizar.renomear(nome_normalizado)
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
                detail="Já existe uma categoria cadastrada com esse nome"
            )

        self.session.refresh(categoria_atualizar)

        return categoria_atualizar

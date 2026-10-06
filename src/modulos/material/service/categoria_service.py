from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.compartilhado.normalizador import normalizar_texto
from src.modulos.material.schemas.schemas_categoria import (
    SchemaCategoriaCadastro,
    SchemaCategoriaAtualizacao
)
from src.modulos.material.entidades.categoria import Categoria
from src.compartilhado.base_service import BaseService


class CategoriaService(BaseService):

    # Declaração do construtor da classe CategoriaService
    def __init__(self, session: Session):
        super().__init__(session)

    # Método para cadastrar categorias
    def cadastrar(self, data: SchemaCategoriaCadastro):

        nome_normalizado = normalizar_texto(data.nome)

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
                nome=data.nome
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=400,
                detail=str(erro)
            )

        self.salvar(categoria_cadastrar)
        self.session.refresh(categoria_cadastrar)

        return categoria_cadastrar

    # Método para visualizar categorias
    def visualizar(self):

        return self.session.query(Categoria).all()

    # Método para atualizar categorias
    def atualizar(
        self,
        categoria_id: int,
        data: SchemaCategoriaAtualizacao
    ):

        categoria_atualizar = self.session.query(Categoria).filter_by(
            id=categoria_id
        ).first()

        if not categoria_atualizar:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada"
            )

        nome_normalizado = normalizar_texto(data.nome)

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
            categoria_atualizar.atualizar(data.nome)
        except ValueError as erro:
            raise HTTPException(
                status_code=400,
                detail=str(erro)
            )

        self.session.commit()
        self.session.refresh(categoria_atualizar)

        return categoria_atualizar

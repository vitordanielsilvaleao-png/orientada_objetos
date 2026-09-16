from fastapi import HTTPException

from src.compartilhado.normalizador import normalizar_texto

from src.modulos.material.schemas.schemas_categoria import SchemaCategoriaCadastro, SchemaCategoriaAtualizacao
from src.modulos.material.entidades.categoria import Categoria
from compartilhado.base_service import BaseService


class CategoriaService(BaseService):

    # Método para cadastrar categorias
    def cadastrar(self, data:SchemaCategoriaCadastro):

        nome_categoria = data.nome.strip()

        if not nome_categoria:
            raise HTTPException(
                status_code=400,
                detail="O nome da categoria é obrigatório"
            )

        nome_normalizado = normalizar_texto(nome_categoria)

        categoria_existente = self.session.query(Categoria).all()

        for categoria in categoria_existente:
            if normalizar_texto(categoria.nome) == nome_normalizado:
                raise HTTPException(
                    status_code=409,
                    detail="Já existe uma categoria cadastrada com esse nome"
                )

        categoria_cadastrar = Categoria(
            nome=nome_categoria
        )

        self.salvar(categoria_cadastrar)
        self.session.refresh(categoria_cadastrar)
        return categoria_cadastrar

    # Método para visualizar categorias
    def visualizar(self):

        return self.session.query(Categoria).all()

    # Método para atualizar categorias
    def atualizar(self, categoria_id: int, data:SchemaCategoriaAtualizacao):

        categoria_atualizar = self.session.query(Categoria).filter_by(
            id=categoria_id
        ).first()

        if not categoria_atualizar:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada"
            )

        nome_categoria = data.nome.strip()

        if not nome_categoria:
            raise HTTPException(
                status_code=400,
                detail="O nome da categoria é obrigatório"
            )

        nome_normalizado = normalizar_texto(nome_categoria)

        categorias = self.session.query(Categoria).filter(
            Categoria.id != categoria_id
        )

        for categoria in categorias:
            if normalizar_texto(categoria.nome) == nome_normalizado:
                raise HTTPException(
                    status_code=409,
                    detail="Já existe uma categoria cadastrada com esse nome"
                )

        categoria_atualizar.atualizar(nome_categoria)

        self.session.commit()
        self.session.refresh(categoria_atualizar)

        return categoria_atualizar
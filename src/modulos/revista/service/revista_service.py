# Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.modulos.reserva.entidade.reserva import Reserva
from src.compartilhado.base_service import BaseService
from src.modulos.revista.schemas.schamas_revista import (SchemaRevistaCadastro, SchemaRevistaAtualizacao)
from src.modulos.material.entidades.editora import Editora
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.revista.entidade.revista import Revista


# Declaração da classe RevistaService
class RevistaService(BaseService):

    # Método para cadastrar revistas
    def cadastrar(self, data: SchemaRevistaCadastro):

        issn_normalizado = Revista.normalizar_issn(data.issn)

        issn_existente = self.session.query(Revista).filter_by(
            issn = issn_normalizado
        ).first()

        if issn_existente:
            raise HTTPException(
                status_code=409,
                detail="O ISSN informado já está cadastrado no sistema"
            )

        self._validar_editora_categoria(data.editora_id, data.categoria_id)

        try:
            revista_cadastrar = Revista(
                titulo=data.titulo,
                ano_publi=data.ano_publi,
                editora_id=data.editora_id,
                categoria_id=data.categoria_id,
                issn=issn_normalizado,
                edicao=data.edicao
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(revista_cadastrar)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="O ISSN informado já está cadastrado no sistema"
            )

        self.session.refresh(revista_cadastrar)

        reserva_pendente = (
            self.session.query(Reserva)
            .filter(
                Reserva.titulo == revista_cadastrar.titulo,
                Reserva.is_active == True,
                Reserva.material_id.is_(None)
            )
            .order_by(Reserva.data.asc())
            .first()
        )

        if not reserva_pendente:
            revista_cadastrar.disponibilizar()
        else:
            revista_cadastrar.reservar()
            reserva_pendente.vincular_material(revista_cadastrar.id)

        self.session.commit()
        self.session.refresh(revista_cadastrar)

        return revista_cadastrar

    # Método auxiliar para buscar uma revista pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, revista_id: int) -> Revista:
        revista = self.session.query(Revista).filter_by(
            id=revista_id
        ).first()

        if not revista:
            raise HTTPException(
                status_code=404,
                detail="Revista não encontrada"
            )

        return revista

    # Método auxiliar para validar se a editora e a categoria informadas existem, lançando 404 caso não existam
    def _validar_editora_categoria(self, editora_id: int | None, categoria_id: int | None):

        if editora_id is not None:
            editora_existente = self.session.query(Editora).filter_by(
                id=editora_id
            ).first()

            if not editora_existente:
                raise HTTPException(
                    status_code=404,
                    detail="A editora informada não existe"
                )

        if categoria_id is not None:
            categoria_existente = self.session.query(Categoria).filter_by(
                id=categoria_id
            ).first()

            if not categoria_existente:
                raise HTTPException(
                    status_code=404,
                    detail="A categoria informada não existe"
                )

    # Método para visualizar revistas
    def visualizar(self):

        return self.session.query(Revista).all()

    # Método para atualizar revistas
    def atualizar(
        self,
        revista_id: int,
        data: SchemaRevistaAtualizacao
    ):

        revista_atualizar = self._buscar_por_id(revista_id)

        self._validar_editora_categoria(data.editora_id, data.categoria_id)

        try:
            revista_atualizar.atualizar(
                titulo=data.titulo,
                ano_publi=data.ano_publi,
                categoria_id=data.categoria_id,
                editora_id=data.editora_id,
                edicao=data.edicao
            )

            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(revista_atualizar)
        return revista_atualizar

    # Método para inativar revistas
    def inativar(self, revista_id: int):

        revista_inativar = self._buscar_por_id(revista_id)

        try:
            revista_inativar.inativar()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(revista_inativar)
        return revista_inativar

    # Método para ativar revistas
    def ativar(self, revista_id: int):

        revista_ativar = self._buscar_por_id(revista_id)

        try:
            revista_ativar.ativar()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(revista_ativar)
        return revista_ativar

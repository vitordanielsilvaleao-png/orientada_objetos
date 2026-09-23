# Import das bibliotecas e classes necessárias para o funcionamento do sistema
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.modulos.reserva.reserva import Reserva
from src.compartilhado.base_service import BaseService
from src.modulos.revista.schemas.schamas_revista import (SchemaRevistaCadastro, SchemaRevistaAtualizacao)
from src.modulos.material.entidades.editora import Editora
from src.modulos.material.entidades.categoria import Categoria
from src.modulos.revista.revista import Revista


# Declaração da classe RevistaService
class RevistaService(BaseService):

    # Declaração do construtor da classe
    def __init__(self, session: Session):
        super().__init__(session)

    # Método para cadastrar revistas
    def cadastrar(self, data: SchemaRevistaCadastro):

        editora_cadastrar = self.session.query(Editora).filter_by(
            id=data.editora_id
        ).first()

        categoria_cadastrar = self.session.query(Categoria).filter_by(
            id=data.categoria_id
        ).first()

        if not editora_cadastrar:
            raise HTTPException(
                status_code=404,
                detail="A editora informada não existe"
            )

        if not categoria_cadastrar:
            raise HTTPException(
                status_code=404,
                detail="A categoria informada não existe"
            )

        revista_cadastrar = Revista(
            titulo=data.titulo,
            ano_publi=data.ano_publi,
            editora_id=data.editora_id,
            categoria_id=data.categoria_id,
            issn=data.issn,
            edicao=data.edicao
        )

        self.salvar(revista_cadastrar)
        self.session.refresh(revista_cadastrar)

        reserva_pendente = (
            self.session.query(Reserva)
            .filter(
                Reserva.titulo == data.titulo,
                Reserva.is_active == True,
                Reserva.material_id.is_(None)
            )
            .order_by(Reserva.data.asc())
            .first()
        )

        if not reserva_pendente:
            revista_cadastrar.status = "DISPONIVEL"
        else:
            revista_cadastrar.status = "RESERVADO"
            reserva_pendente.material_id = revista_cadastrar.id

        self.session.commit()

        return revista_cadastrar

    # Método para visualizar revistas
    def visualizar(self):

        return self.session.query(Revista).all()

    # Método para atualizar revistas
    def atualizar(
        self,
        revista_id: int,
        data: SchemaRevistaAtualizacao
    ):

        revista_atualizar = self.session.query(Revista).filter_by(
            id=revista_id
        ).first()

        if not revista_atualizar:
            raise HTTPException(
                status_code=404,
                detail="Revista não encontrada"
            )

        revista_atualizar.atualizar(
            titulo=data.titulo,
            ano_publi=data.ano_publi,
            categoria_id=data.categoria_id,
            editora_id=data.editora_id,
            edicao=data.edicao
        )

        self.session.commit()
        self.session.refresh(revista_atualizar)

        return revista_atualizar

    # Método para inativar revistas
    def inativar(self, revista_id: int):

        revista_inativar = self.session.query(Revista).filter_by(
            id=revista_id
        ).first()

        if not revista_inativar:
            raise HTTPException(
                status_code=404,
                detail="Revista não encontrada"
            )

        revista_inativar.inativar()
        self.session.commit()

    # Método para ativar revistas
    def ativar(self, revista_id: int):

        revista_ativar = self.session.query(Revista).filter_by(
            id=revista_id
        ).first()

        if not revista_ativar:
            raise HTTPException(
                status_code=404,
                detail="Revista não encontrada"
            )

        revista_ativar.ativar()
        self.session.commit()

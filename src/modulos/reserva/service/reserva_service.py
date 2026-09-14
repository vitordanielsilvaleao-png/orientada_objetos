#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.compartilhado.base_service import BaseService
from src.modulos.reserva.schemas.schema_reserva import SchemaReservaCadastro
from src.modulos.reserva.reserva import Reserva

#Declaração da classe ReservaService
class ReservaService (BaseService):

    #Declaração do construtor da classe
    def __init__(self, session:Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaReservaCadastro):

        reserva_existente = self.session.query(Reserva).filter_by(
            cliente_id=data.cliente_id,
            material_id=data.material_id,
            is_active=True
        ).first()

        if reserva_existente:
            raise HTTPException(
                status_code=409,
                detail="O cliente já possui uma reserva ativa para este material"
            )

        reserva_cadastrar = Reserva(
            titulo = data.titulo,
            cliente_id = data.cliente_id,
            material_id = data.material_id
        )

        self.salvar(reserva_cadastrar)
        self.session.refresh(reserva_cadastrar)
        return reserva_cadastrar

    def visualizar(self):

        return self.session.query(Reserva).all()

    def visualizar_expiradas(self):

        reservas = self.session.query(Reserva).filter_by(
            is_active=True
        ).all()

        reservas_expiradas = []

        for reserva in reservas:
            if reserva.verificar_expiracao():
                reservas_expiradas.append(reserva)

        self.session.commit()

        return reservas_expiradas
    
    def inativar(self, reserva_id:int):

        reserva_inativar = self.session.query(Reserva).filter_by(
             id=reserva_id
        ).first()

        if not reserva_inativar:
            raise HTTPException(
                 status_code=404,
                 detail="Reserva não encontrada"
            )
         
        try:
            reserva_inativar.cancelar()
        except ValueError as erro:
            raise HTTPException(
                status_code=400,
                detail=str(erro)
            )

        self.session.commit()
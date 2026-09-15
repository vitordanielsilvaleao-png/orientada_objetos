#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.compartilhado.base_service import BaseService
from src.modulos.reserva.schemas.schema_reserva import SchemaReservaCadastro
from src.modulos.reserva.reserva import Reserva
from src.modulos.cliente.cliente import Cliente
from src.modulos.material.entidades.material import Material

#Declaração da classe ReservaService
class ReservaService (BaseService):

    #Declaração do construtor da classe
    def __init__(self, session:Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaReservaCadastro):

        usuario_ativo = self.session.query(Cliente).filter_by(
            id=data.cliente_id,
            is_active=True
        ).first()

        if not usuario_ativo:
            raise HTTPException(
                status_code=409,
                detail="A reserva não pode ser efetuada, pois o usuário se encontra inativo"
            )

        reserva_existente = self.session.query(Reserva).filter_by(
            cliente_id=data.cliente_id,
            titulo=data.titulo,
            is_active=True
        ).first()

        if reserva_existente:
            raise HTTPException(
                status_code=409,
                detail="O cliente já possui uma reserva ativa para este material"
            )

        material_existente = self.session.query(Material).filter_by(
            titulo = data.titulo,
            status="DISPONIVEL",
            is_active=True
        ).first()

        if material_existente:
            material_id = material_existente.id
            material_existente.status = "RESERVADO"
        else:
            material_id = None

        reserva_cadastrar = Reserva(
            titulo = data.titulo,
            cliente_id = data.cliente_id,
            material_id = material_id
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
        self.session.refresh(reserva_inativar)

        return reserva_inativar
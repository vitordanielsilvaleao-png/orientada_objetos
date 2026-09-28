#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.compartilhado.base_service import BaseService
from src.compartilhado.enum import StatusMaterial

from src.modulos.reserva.schemas.schema_reserva import SchemaReservaCadastro
from src.modulos.reserva.reserva import Reserva
from src.modulos.cliente.cliente import Cliente
from src.modulos.material.entidades.material import Material
from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService
from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro


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

        titulo_formatado = data.titulo.strip().lower()

        reserva_existente = self.session.query(Reserva).filter_by(
            cliente_id=data.cliente_id,
            titulo=titulo_formatado,
            is_active=True
        ).first()

        if reserva_existente:
            raise HTTPException(
                status_code=409,
                detail="O cliente já possui uma reserva ativa para este material"
            )

        material_existente = self.session.query(Material).filter_by(
            titulo = titulo_formatado,
            status=StatusMaterial.DISPONIVEL,
            is_active=True
        ).first()

        if material_existente:
            material_id = material_existente.id
            material_existente.status = StatusMaterial.RESERVADO
        else:
            material_id = None

        reserva_cadastrar = Reserva(
            titulo = titulo_formatado,
            cliente_id = data.cliente_id,
            material_id = material_id
        )

        self.salvar(reserva_cadastrar)
        self.session.refresh(reserva_cadastrar)
        return reserva_cadastrar

    def visualizar(self):

        return self.session.query(Reserva).all()

    def visualizar_abertos(self):

        return self.session.query(Reserva).filter_by(
            is_active = True
        ).all()

    def visualizar_expiradas(self):

        return self.session.query(Reserva).filter_by(
            is_active=False
        ).all()
    
    def inativar(self, reserva_id:int):

        reserva_inativar = self.session.query(Reserva).filter_by(
            id = reserva_id,
            is_active = True
        ).first()

        if not reserva_inativar:
            raise HTTPException(
                status_code=404,
                detail="Reserva não encontrada ou inativa"
            )

        try:
            reserva_inativar.cancelar()
        except ValueError as erro:
            raise HTTPException(
                status_code=400,
                detail=str(erro)
            )

        if reserva_inativar.material_id is not None:

            material_reservado = self.session.query(Material).filter_by(
                id=reserva_inativar.material_id
            ).first()

            if material_reservado:
                material_reservado.status = StatusMaterial.DISPONIVEL

        self.session.commit()
        self.session.refresh(reserva_inativar)

        return reserva_inativar

    def atender_reserva(self, reserva_id:int):

        reserva = self.session.query(Reserva).filter_by(
            id = reserva_id,
            is_active = True
        ).first()

        if not reserva:
            raise HTTPException(
                 status_code=404,
                 detail="A reserva não foi encontrada ou está inativa"
            )
        
        if reserva.material_id is None:
            raise HTTPException(
                 status_code=404,
                 detail="Reserva não possui material associado"
            )

        emprestimo = EmprestimoService(self.session)

        data = SchemaEmprestimoCadastro(
            cliente_id=reserva.cliente_id,
            material_id=reserva.material_id
        )

        novo_emprestimo = emprestimo.cadastrar(data)

        reserva.cancelar()

        self.session.commit()
        self.session.refresh(reserva)

        return reserva, novo_emprestimo
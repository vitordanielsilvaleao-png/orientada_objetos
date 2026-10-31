from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.compartilhado.enum import StatusMaterial, StatusEmprestimo

from src.compartilhado.base_service import BaseService
from src.modulos.emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro
from src.modulos.reserva.entidade.reserva import Reserva
from src.modulos.material.entidades.material import Material
from src.modulos.cliente.entidade.cliente import Cliente
from src.modulos.emprestimo.entidade.emprestimo import Emprestimo

#Declaração da classe EmprestimoService
class EmprestimoService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)

    #Método para cadastrar empréstimos
    def cadastrar(self, data: SchemaEmprestimoCadastro):
        limite_emprestimo = 4
        cont_emprestimos = 0

        cliente_existente = self.session.query(Cliente).filter_by(
            id = data.cliente_id
        ).first()

        if not cliente_existente:
            raise HTTPException(
                status_code=404,
                detail="O cliente informado não está cadastrado!"
            )

        if not cliente_existente.is_active:
             raise HTTPException(
                 status_code=409,
                 detail="O empréstimo não pode ser registrado, pois o cadastro do cliente se encontra inativo"
             )

        material_existente = self.session.query(Material).filter_by(
            id = data.material_id
        ).first()

        if not material_existente:
             raise HTTPException(
                status_code=404,
                 detail="O material informado não está cadastrado no acervo!"
             )

        if not material_existente.is_active:
             raise HTTPException(
                 status_code=409,
                 detail="O empréstimo não pode ser registrado, pois o material selecionado está inativo"
             )

        if material_existente.status == StatusMaterial.EMPRESTADO:
             raise HTTPException(
                 status_code=409,
                 detail="O empréstimo não pode ser realizado pois o material se encontra emprestado"
             )

        reserva_existente = self.session.query(Reserva).filter_by(
            material_id = data.material_id,
            cliente_id = data.cliente_id,
            is_active = True
        ).first()

        if material_existente.status == StatusMaterial.RESERVADO and not reserva_existente:
             raise HTTPException(
                 status_code=409,
                 detail="O material selecionado está reservado para outro usuário"
             )

        emprestimos_cliente = self.session.query(Emprestimo).filter_by(
            cliente_id = data.cliente_id,
            _is_active = True
        ).all()

        for emp in emprestimos_cliente:
             cont_emprestimos += 1
             if emp.verificar_atraso():
                 raise HTTPException(
                     status_code=409,
                     detail="O cliente possui empréstimo(s) em atraso"
                 )

        if cont_emprestimos >= limite_emprestimo:
             raise HTTPException(
                 status_code=409,
                 detail="O cliente atingiu o limite máximo de empréstimos permitidos"
             )

        emprestimo_cadastrar = Emprestimo(
             material_id = data.material_id,
             cliente_id = data.cliente_id
        )

        material_existente.emprestar()

        #A reserva do cliente para este material é encerrada no mesmo commit do empréstimo
        if reserva_existente:
            reserva_existente.concluir()

        self.salvar(emprestimo_cadastrar)
        self.session.refresh(emprestimo_cadastrar)
        return emprestimo_cadastrar

    #Método para visualizar empréstimos
    def visualizar(self):
         return self.session.query(Emprestimo).all()

    #Método para visualizar empréstimos abertos
    def visualizar_abertos(self):
        return self.session.query(Emprestimo).filter_by(_is_active=True).all()

    #Método para visualizar empréstimos atrasados
    def visualizar_atrasados(self):
        emprestimos = self.session.query(Emprestimo).filter_by(_is_active=True).all()
        atrasados = []
        for emp in emprestimos:
            if emp.verificar_atraso():
                atrasados.append(emp)
        return atrasados

    #Método para registrar devolução
    def registrar_devolucao(self, emprestimo_id: int):
        emprestimo_devolucao = self.session.query(Emprestimo).filter_by(
            id = emprestimo_id
        ).first()

        if not emprestimo_devolucao:
             raise HTTPException(
                 status_code=404,
                 detail="Empréstimo não encontrado"
             )

        if not emprestimo_devolucao.is_active:
             raise HTTPException(
                 status_code=409,
                 detail="Este empréstimo já foi devolvido"
             )

        material_devolucao = self.session.query(Material).filter_by(
            id = emprestimo_devolucao.material_id
        ).first()

        emprestimo_devolucao.devolver()

        reserva_pendente = self.session.query(Reserva).filter_by(
            material_id = material_devolucao.id,
            is_active = True
        ).first()

        if not reserva_pendente:
             material_devolucao.disponibilizar()
        else:
             material_devolucao.reservar()
             reserva_pendente.vincular_material(material_devolucao.id)

        self.session.commit()
        self.session.refresh(emprestimo_devolucao)
        return emprestimo_devolucao
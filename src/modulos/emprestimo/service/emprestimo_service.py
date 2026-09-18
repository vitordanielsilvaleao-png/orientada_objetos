#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from fastapi import HTTPException
from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService
from emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro
from src.modulos.reserva.reserva import Reserva
from src.modulos.material.entidades.material import Material
from src.modulos.cliente.cliente import Cliente
from src.modulos.emprestimo.emprestimo import Emprestimo

#Declaração da classe EmprestimoService
class EmprestimoService(BaseService):

    # Declaração do construtor da classe EmprestimoService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaEmprestimoCadastro):

        limite_emprestimo = 4
        cont_emprestimos = 0

        usuario_ativo = self.session.query(Cliente).filter_by(
            id = data.cliente_id,
            is_active = True
        ).first()

        if not usuario_ativo:
            raise HTTPException(
                status_code=409,
                detail="O empréstimo não pode ser registrado, pois o cadastro do cliente se encontra inativo"
            )

        material_existente = self.session.query(Material).filter_by(
            id = data.material_id
        ).first()

        if not material_existente:
            raise HTTPException(
                status_code=400,
                detail="O material informado não está cadastrado no acervo!"
            )

        if not material_existente.is_active:
            raise HTTPException(
                status_code=409,
                detail="O empréstimo não pode ser registrado, pois o material está inativo"
            )

        reserva_existente = self.session.query(Reserva).filter_by(
            cliente_id=data.cliente_id,
            material_id=data.material_id,
            is_active=True
        ).first()

        if material_existente.status == "DISPONIVEL":
            pass

        elif material_existente.status == "RESERVADO" and reserva_existente:
            pass

        else:
            raise HTTPException(
                status_code=409,
                detail="O empréstimo não pode ser registrado, pois o material informado não está disponível"
            )

        lista_emprestimo = self.session.query(Emprestimo).filter_by(
            is_active = True
        )

        for emprestimo in lista_emprestimo:

            if emprestimo.cliente_id == data.cliente_id:

                cont_emprestimos += 1

                if emprestimo.status == "ATRASADO":
                    raise HTTPException(
                        status_code=409,
                        detail="O empréstimo não pode ser registrado, pois o usuário possuí um empréstimo ativo em atraso!"
                    )

        if cont_emprestimos >= limite_emprestimo:
            raise HTTPException(
                status_code=409,
                detail="O empréstimo não pode ser registrado, pois o usuário atingiu o limite de empréstimos ativos!"
            )

        emprestimo_cadastrar = Emprestimo(
            material_id = data.material_id,
            cliente_id = data.cliente_id
        )

        material_existente.status = "EMPRESTADO"

        self.salvar(emprestimo_cadastrar)
        self.session.refresh(emprestimo_cadastrar)
        return emprestimo_cadastrar

    def visualizar(self):

        return self.session.query(Emprestimo).all()

    def visualizar_abertos(self):

        return self.session.query(Emprestimo).filter(
            Emprestimo.data_devolucao == None,
            Emprestimo.is_active == True
        ).all()

    def visualizar_atrasados(self):

        return self.session.query(Emprestimo).filter_by(
            is_active = True,
            status = "ATRASADO"
        ).all()

    def registrar_devolucao(self, emprestimo_id:int):

        emprestimo_devolucao = self.session.query(Emprestimo).filter_by(
            id = emprestimo_id
        ).first()

        if not emprestimo_devolucao:
            raise HTTPException(
                status_code=404,
                detail="O empréstimo informado não foi localizado!"
            )

        emprestimo_devolucao.devolver()

        material_devolucao = self.session.query(Material).filter_by(
            id = emprestimo_devolucao.material_id
        ).first()

        if not material_devolucao:
            raise HTTPException(
                status_code=404,
                detail="O material associado ao empréstimo não foi localizado!"
            )

        reserva_pendente = (
            self.session.query(Reserva)
            .filter(
                Reserva.titulo == material_devolucao.titulo,
                Reserva.is_active == True,
                Reserva.material_id.is_(None)
            )
            .order_by(Reserva.data.asc())
            .first()
        )

        if not reserva_pendente:

            material_devolucao.status = "DISPONIVEL"

        else:

            material_devolucao.status = "RESERVADO"
            reserva_pendente.atender_reserva(material_devolucao.id)

        self.session.commit()
        self.session.refresh(emprestimo_devolucao)
        return emprestimo_devolucao
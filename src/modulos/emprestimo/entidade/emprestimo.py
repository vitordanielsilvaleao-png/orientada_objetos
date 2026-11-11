#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Emprestimo
from sqlalchemy import ForeignKey, Boolean, DateTime, func, Enum
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from src.compartilhado.enum import StatusEmprestimo
from src.database.database import Base
from datetime import datetime, timedelta

#Criação da entidade Emprestimo
class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    material_id: Mapped[int] =  mapped_column(
        ForeignKey("material.id"),
        nullable=False
    )

    cliente_id: Mapped[int] =  mapped_column(
        ForeignKey("cliente.id"),
        nullable=False
    )

    data_emprestimo: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    #Atributos privados mapeados para as colunas de mesmo nome, alterados somente por devolver e marcar_atrasado
    _data_devolucao: Mapped[datetime | None] = mapped_column(
        "data_devolucao",
        DateTime,
        nullable=True
    )

    _status: Mapped[StatusEmprestimo] = mapped_column(
        "status",
        Enum(StatusEmprestimo),
        nullable=False,
        default=StatusEmprestimo.ABERTO
    )

    _is_active: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        nullable=False,
        default=True
    )

    #Declaração do construtor da Classe
    def __init__(
            self,
            material_id,
            cliente_id
    ):
        self.material_id = material_id
        self.cliente_id = cliente_id
        self.data_emprestimo = datetime.now()
        self._data_devolucao = None
        self._status = StatusEmprestimo.ABERTO
        self._is_active = True

    #Getters dos atributos somente leitura
    @hybrid_property
    def data_devolucao(self):
        return self._data_devolucao

    @hybrid_property
    def status(self):
        return self._status

    @hybrid_property
    def is_active(self):
        return self._is_active

    #[RF-DEV-001] Registro de Devolução
    def devolver(self):
        if self.is_active:
            self._data_devolucao = datetime.now()
            self._status = StatusEmprestimo.DEVOLVIDO
            self._is_active = False
        else:
            raise ValueError("Este empréstimo já foi encerrado.")

    #[RN-EMP-002] Prazo do Empréstimo
    def verificar_atraso(self):
        if self.is_active:
            prazo = self.data_emprestimo + timedelta(days=30)

            if datetime.now() > prazo:
                return True
            else:
                return False
        else:    
            return False

    def marcar_atrasado(self):

        if self.verificar_atraso():
            self._status = StatusEmprestimo.ATRASADO

    def validar_emprestimo_ativo(self):
        return self.data_devolucao is None
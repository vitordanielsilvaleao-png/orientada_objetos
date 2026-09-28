#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Emprestimo
from sqlalchemy import ForeignKey, Boolean, DateTime, func, Enum
from sqlalchemy.orm import  Mapped, mapped_column

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

    data_devolucao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[StatusEmprestimo] = mapped_column(
        Enum(StatusEmprestimo),
        nullable=False,
        default=StatusEmprestimo.ABERTO
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    #[RF-DEV-001] Registro de Devolução
    def devolver(self):
        if self.is_active:
            self.data_devolucao = datetime.now()
            self.status = StatusEmprestimo.DEVOLVIDO
            self.is_active = False
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
            self.status = StatusEmprestimo.ATRASADO

    def validar_emprestimo_ativo(self):
        return self.data_devolucao is None
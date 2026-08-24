#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Emprestimo
from sqlalchemy import String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import  Mapped, mapped_column
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

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ABERTO"
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
            self.status = "DEVOLVIDO"
            self.is_active = False
        else:
            raise ValueError("Este empréstimo já foi encerrado.")

    #[RN-EMP-002] Prazo do Empréstimo
    def verificar_atraso(self):
        if self.is_active:
            prazo = self.data_emprestimo + timedelta(days=30)

            if datetime.now() > prazo:
                self.status = "ATRASADO"
                return True
        else:    
            return False

    def validar_emprestimo(self):
        return self.data_devolucao is None
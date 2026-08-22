#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Emprestimo
from sqlalchemy import String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import  Mapped, mapped_column
from src.database.database import Base
from datetime import datetime

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

#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Revista
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

#Criação da entidade Cliente
class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    bairro: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    rua: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    numero: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    complemento: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    telefone: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
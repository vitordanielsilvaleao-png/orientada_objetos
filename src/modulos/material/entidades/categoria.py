#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Categoria
from sqlalchemy import String
from sqlalchemy.orm import  Mapped, mapped_column
from src.database.database import Base

#Criação da entidade Categoria
class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )


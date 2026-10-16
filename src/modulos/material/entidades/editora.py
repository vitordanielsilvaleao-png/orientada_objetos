#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Editora
from sqlalchemy import String
from sqlalchemy.orm import  Mapped, mapped_column, validates
from src.database.database import Base

from src.compartilhado.normalizador import normalizar_texto

#Criação da entidade Editora
class Editora(Base):
    __tablename__ = "editora"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    #Validação de dados recebidos
    @validates("nome")
    def validar_nome(self, key, nome):
        return self._normalizar_nome(nome)
     
    @staticmethod
    def _normalizar_nome(nome):
        return normalizar_texto(nome)
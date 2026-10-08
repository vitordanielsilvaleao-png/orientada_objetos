#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Autor
from sqlalchemy import String
from sqlalchemy.orm import  Mapped, mapped_column, validates
from src.database.database import Base

#Criação da entidade Autor
class Autor(Base):
    __tablename__ = "autor"

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
    def validar_nome(self, chave:str, nome:str):
        self._validar_nome_existente(nome)
        return self._normalizar_nome(nome)

    #Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _validar_nome_existente(nome:str):
        if not nome or not nome.strip():
            raise ValueError(
                "O nome do autor é obrigatório"
            )

    @staticmethod
    def _normalizar_nome(nome:str):
        return nome.strip().lower()
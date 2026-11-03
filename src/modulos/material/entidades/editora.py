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
    def validar_nome(self, chave:str, nome:str):
        self._validar_nome_existente(nome)
        return self.normalizar_nome(nome)

    #Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _validar_nome_existente(nome:str):
        if not nome or not nome.strip():
            raise ValueError(
                "O nome da editora é obrigatório"
            )

    @staticmethod
    def normalizar_nome(nome:str):
        return normalizar_texto(nome)

    #Método para renomear a editora, validado e normalizado por validar_nome
    def renomear(self, nome:str):
        self.nome = nome

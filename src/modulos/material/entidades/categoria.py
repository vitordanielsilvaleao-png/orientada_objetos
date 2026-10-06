# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Categoria
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.database.database import Base
from src.compartilhado.normalizador import normalizar_texto


# Criação da entidade Categoria
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

    # Validação e normalização do nome da categoria
    @validates("nome")
    def validar_nome(self, chave, nome):
        if not isinstance(nome, str):
            raise ValueError("O nome da categoria deve ser um texto")

        nome_normalizado = normalizar_texto(nome)

        if not nome_normalizado:
            raise ValueError("O nome da categoria não pode ser vazio")

        return nome_normalizado

    # Método para atualização do nome da categoria
    def atualizar(self, nome: str):
        self.nome = nome

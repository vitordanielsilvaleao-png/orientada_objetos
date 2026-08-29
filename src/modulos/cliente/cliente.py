#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Cliente
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

    #[RF-CLI-003] Atualização de Cliente
    def atualizar_cliente(self,nome,bairro,rua,numero,complemento,telefone):
        if self.is_active:
            self.nome = nome
            self.bairro = bairro
            self.rua = rua
            self.numero = numero
            self.complemento = complemento
            self.telefone = telefone
        else:
            raise ValueError("Cliente inativo")

    #[RF-CLI-004] Inativação de Cliente
    def inativar_cliente(self):
        if self.is_active:
            self.is_active = False
        else:
            raise ValueError("Cliente já inativado")

    def ativar_cliente(self):
        if not self.is_active:
            self.is_active = True
        else:
            raise ValueError("Cliente já ativado")

    def validar_cliente_ativo(self):
        return self.is_active
# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Cliente
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.database.database import Base

# Criação da entidade Cliente
class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        unique=True
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False
        # Removido o unique=True, pois agora o identificador único é o CPF
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

    # Declaração do construtor da Classe
    def __init__(
            self,
            cpf,
            nome,
            bairro,
            rua,
            numero,
            telefone,
            complemento=None
    ):
        self.cpf = cpf
        self.nome = nome
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.telefone = telefone
        self.complemento = complemento

    # Validação de dados recebidos
    @validates("cpf")
    def validar_cpf(self, chave, cpf):
        cpf_normalizado = self._normalizar_cpf(cpf)
        self._validar_cpf(cpf_normalizado)
        return cpf_normalizado

    @validates("nome")
    def validar_nome(self, chave, nome):
        nome_normalizado = self._normalizar_nome(nome)
        self._validar_nome(nome_normalizado)
        return nome_normalizado

    # Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _normalizar_cpf(cpf):
        if cpf:
            return str(cpf).replace(".", "").replace("-", "").strip()
        return cpf

    @staticmethod
    def _validar_cpf(cpf):
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("O CPF informado é inválido")

    @staticmethod
    def _normalizar_nome(nome):
        if nome:
            # Remove espaços extras no meio e nas pontas, e deixa iniciais em maiúsculo
            return " ".join(str(nome).strip().split()).title()
        return nome

    @staticmethod
    def _validar_nome(nome):
        if not nome or len(nome) < 3:
            raise ValueError("O nome informado é inválido")

    # [RF-CLI-003] Atualização de Cliente
    def atualizar_cliente(
            self,
            nome=None,
            bairro=None,
            rua=None,
            numero=None,
            complemento=None,
            telefone=None
    ):
        if self.is_active:
            if nome is not None:
                self.nome = nome

            if bairro is not None:
                self.bairro = bairro

            if rua is not None:
                self.rua = rua

            if numero is not None:
                self.numero = numero

            if complemento is not None:
                self.complemento = complemento

            if telefone is not None:
                self.telefone = telefone
        else:
            raise ValueError("Cliente inativo")

    # [RF-CLI-004] Inativação de Cliente
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
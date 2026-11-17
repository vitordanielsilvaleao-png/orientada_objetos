#Importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Cliente
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.ext.hybrid import hybrid_property
from src.database.database import Base

#Criação da entidade Cliente
class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    #Atributo privado mapeado para a coluna "cpf", acessado somente pela property cpf
    _cpf: Mapped[str] = mapped_column(
        "cpf",
        String(11),
        nullable=False,
        unique=True
    )

    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False
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

    complemento: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    telefone: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    #Atributo privado mapeado para a coluna "is_active", alterado somente por ativar_cliente e inativar_cliente
    _is_active: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        nullable=False,
        default=True
    )

    #Declaração do construtor da Classe
    def __init__(
            self,
            cpf,
            nome,
            bairro,
            rua,
            numero,
            telefone,
            complemento
    ):
        self._cpf = cpf
        self.nome = nome
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.telefone = telefone
        self.complemento = complemento
        self._is_active = True

    #Getters dos atributos somente leitura
    @hybrid_property
    def cpf(self):
        return self._cpf

    @hybrid_property
    def is_active(self):
        return self._is_active

    #Validação de dados recebidos
    @validates("_cpf")
    def _definir_cpf(self, chave, cpf: str):
        if self._cpf is not None:
            raise ValueError("O CPF não pode ser alterado")

        cpf_normalizado = self.normalizar_cpf(cpf)
        self._validar_cpf(cpf_normalizado)
        return cpf_normalizado

    @validates("nome")
    def _definir_nome(self, chave, nome: str):
        nome_normalizado = self.normalizar_nome(nome)
        self._validar_nome(nome_normalizado)
        return nome_normalizado

    @validates("rua")
    def _definir_rua(self, chave, rua: str):
        rua_normalizada = self.normalizar_nome(rua)
        self._validar_rua(rua_normalizada)
        return rua_normalizada

    @validates("bairro")
    def _definir_bairro(self, chave, bairro: str):
        bairro_normalizado = self.normalizar_nome(bairro)
        self._validar_bairro(bairro_normalizado)
        return bairro_normalizado

    @validates("complemento")
    def _definir_complemento(self, chave, complemento):
        if complemento is None:
            return None
        complemento = self.normalizar_nome(complemento)
        if not complemento:
            return None
        return complemento

    @validates("telefone")
    def _definir_telefone(self, chave, telefone: str):
        telefone_normalizado = self.normalizar_telefone(telefone)
        self._validar_telefone(telefone_normalizado)
        return telefone_normalizado

    @validates("numero")
    def _definir_numero(self, chave, numero: int):
        numero_normalizado = self.normalizar_numero(numero)
        self._validar_numero(numero_normalizado)
        return numero_normalizado

    #Métodos para validação e normalização de dados do construtor
    @staticmethod
    def normalizar_cpf(cpf: str):
        if cpf:
            return str(cpf).replace(".", "").replace("-", "").strip()
        return cpf

    @staticmethod
    def _validar_cpf(cpf: str):
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("O CPF informado é inválido")

    @staticmethod
    def normalizar_nome(nome: str):
        if nome:
            return " ".join(str(nome).strip().split())
        return nome

    @staticmethod
    def _validar_nome(nome: str):
        if not nome or len(nome) < 3:
            raise ValueError("O nome informado é inválido")

    @staticmethod
    def normalizar_telefone(telefone: str):
        if telefone:
            return "".join(c for c in str(telefone) if c.isdigit())
        return telefone

    @staticmethod
    def _validar_telefone(telefone: str):
        if not telefone or len(telefone) not in (10, 11) or not telefone.isdigit():
            raise ValueError("O telefone informado é inválido")

    @staticmethod
    def normalizar_numero(numero: int):
        try:
            return int(numero)
        except (TypeError, ValueError):
            raise ValueError("O número informado é inválido!")

    @staticmethod
    def _validar_numero(numero: int):
        if numero <= 0:
            raise ValueError("O número informado é inválido!")

    @staticmethod
    def _validar_rua(rua: str):
        if not rua:
            raise ValueError("A rua informada é inválida")

    @staticmethod
    def _validar_bairro(bairro: str):
        if not bairro:
            raise ValueError("O bairro informado é inválido")

    #[RF-CLI-003] Atualização de Cliente
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

    #[RF-CLI-004] Inativação de Cliente
    def inativar_cliente(self):
        if self.is_active:
            self._is_active = False
        else:
            raise ValueError("Cliente já inativado")

    def ativar_cliente(self):
        if not self.is_active:
            self._is_active = True
        else:
            raise ValueError("Cliente já ativado")
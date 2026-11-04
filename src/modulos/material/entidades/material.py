# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Material
from sqlalchemy import Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.ext.hybrid import hybrid_property
from src.database.database import Base
from src.compartilhado.enum import StatusMaterial

# Criação da entidade Material
class Material(Base):
    __tablename__ = "material"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ano_publi: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id"),
        nullable=False
    )

    editora_id: Mapped[int] = mapped_column(
        ForeignKey("editora.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    #Atributos privados mapeados para as colunas de mesmo nome, alterados somente pelos métodos de domínio
    _status: Mapped[StatusMaterial] = mapped_column(
        "status",
        Enum(StatusMaterial),
        nullable=False,
        default=StatusMaterial.DISPONIVEL
    )

    _is_active: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        nullable=False,
        default=True
    )

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "material",
    }

    #Declaração do Construtor da Classe
    def __init__(
        self,
        titulo,
        ano_publi,
        categoria_id,
        editora_id
    ):
        super().__init__()

        self.titulo = titulo
        self.ano_publi = ano_publi
        self.categoria_id = categoria_id
        self.editora_id = editora_id
        self._is_active = True
        self._status = StatusMaterial.DISPONIVEL

    #Getters dos atributos somente leitura
    @hybrid_property
    def status(self):
        return self._status

    @hybrid_property
    def is_active(self):
        return self._is_active

    #Validação de dados recebidos
    @validates("titulo")
    def validar_titulo(self, chave:str, titulo:str):
        self._validar_titulo_existente(titulo)
        return self._normalizar_titulo(titulo)

    @validates("ano_publi")
    def validar_ano_publi(self, chave, ano_publi):
        self._validar_ano_publi(ano_publi)
        return ano_publi

    #Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _validar_titulo_existente(titulo:str):
        if not titulo or not titulo.strip():
            raise ValueError(
                "O título do material é obrigatório"
            )

    @staticmethod
    def _normalizar_titulo(titulo:str):
        return titulo.strip().lower()

    @staticmethod
    def _validar_ano_publi(ano_publi):
        if not ano_publi or ano_publi <= 0:
            raise ValueError(
                "O ano de publicação é inválido"
            )

    #Método para atualização de materiais
    def atualizar(
            self,
            titulo=None,
            ano_publi=None,
            categoria_id=None,
            editora_id=None
    ):

        if not self.is_active:
            raise ValueError(
                "Material inativo não pode ser atualizado"
            )

        if titulo is not None:
            self.titulo = titulo

        if ano_publi is not None:
            self.ano_publi = ano_publi

        if categoria_id is not None:
            self.categoria_id = categoria_id

        if editora_id is not None:
            self.editora_id = editora_id

    # [RF-ACER-003] [RN-ACER-013] Inativação do Material
    def inativar(self):
        if self.is_active:
            self._is_active = False
        else:
            raise ValueError("Material já inativado")

    # Ativação do Material
    def ativar(self):
        if not self.is_active:
            self._is_active = True
        else:
            raise ValueError("Material já ativado")

    # Verifica se o Material está ativo e disponível
    def esta_disponivel(self):
        return self.is_active and self.status == StatusMaterial.DISPONIVEL

    #Métodos de domínio para as transições de status do Material
    def disponibilizar(self):
        self._status = StatusMaterial.DISPONIVEL

    def reservar(self):
        self._status = StatusMaterial.RESERVADO

    def emprestar(self):
        self._status = StatusMaterial.EMPRESTADO

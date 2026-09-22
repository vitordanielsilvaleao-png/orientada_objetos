# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Revista
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.modulos.material.entidades.material import Material

# Criação da entidade Revista que herda atributos da entidade Material


class Revista(Material):
    __tablename__ = "revista"

    id: Mapped[int] = mapped_column(
        ForeignKey("material.id"),
        primary_key=True
    )

    issn: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        unique=True,
        primary_key=True
    )

    edicao: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "revista",
    }

    # Declaração do construtor da Classe
    def __init__(
            self,
            titulo,
            ano_publi,
            categoria_id,
            editora_id,
            issn,
            edicao
    ):
        super().__init__(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        self.issn = issn
        self.edicao = edicao

    #Validação de dados recebidos
    @validates("issn")
    def validar_issn(self, chave, issn):
        issn_normalizado = self._normalizar_issn(issn)
        self._validar_issn(issn_normalizado)
        return issn_normalizado

    @validates("edicao")
    def validar_edicao(self, chave, edicao):
        self._validar_edicao(edicao)
        return edicao

    # Métodos para validação e normalização de dados do construtor
    @staticmethod
    def _normalizar_issn(issn):
        return issn.replace(".", "").replace("-", "")

    @staticmethod
    def _validar_issn(issn):
        if len(issn) != 8 or not issn.isdigit():
            raise ValueError(
                "O ISSN informado é inválido"
            )

    @staticmethod
    def _validar_edicao(edicao):
        if edicao <= 0:
            raise ValueError(
                "A edição informada é inválida"
            )

    # [RF-ACER-002] Atualização dos dados da Revista - Sobreescrição do método da classe pai Material
    def atualizar(
            self,
            titulo=None,
            ano_publi=None,
            categoria_id=None,
            editora_id=None,
            edicao=None
    ):
        super().atualizar(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        if edicao is not None:
            self.edicao = edicao
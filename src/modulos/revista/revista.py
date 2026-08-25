# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Revista
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.modulos.material.entidades.material import Material

# Criação da entidade Revista que herda atributos da entidade Material


class Revista(Material):
    __tablename__ = "revista"

    id: Mapped[int] = mapped_column(
        ForeignKey("material.id"),
        primary_key=True
    )

    issn: Mapped[str] = mapped_column(
        String(14),
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

    # [RF-ACER-002] Atualização dos dados da Revista
    def atualizar_revista(
        self,
        titulo,
        ano_publi,
        categoria_id,
        editora_id,
        issn,
        edicao
    ):
        super().atualizar_material(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        self.issn = issn
        self.edicao = edicao

    # Implementação do método descricao herdado de Material
    def descricao(self):
        return f"Título: {self.titulo} | Edição: {self.edicao} | ISSN: {self.issn}"

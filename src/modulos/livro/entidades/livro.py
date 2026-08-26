# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Livro
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.modulos.material.entidades.material import Material

# Criação da entidade Livro que herda atributos da entidade Material
class Livro(Material):
    __tablename__ = "livro"

    id: Mapped[int] = mapped_column(
        ForeignKey("material.id"),
        primary_key=True
    )

    isbn: Mapped[str] = mapped_column(
        String(14),
        nullable=False,
        unique=True,
        primary_key=True
    )

    autor_id: Mapped[int] = mapped_column(
        ForeignKey("autor.id"),
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "livro",
    }

    # [RF-ACER-002] Atualização dos dados do Livro
    def atualizar_livro(
        self,
        titulo,
        ano_publi,
        categoria_id,
        editora_id,
        isbn,
        autor_id
    ):
        super().atualizar_material(
            titulo,
            ano_publi,
            categoria_id,
            editora_id
        )

        self.isbn = isbn
        self.autor_id = autor_id
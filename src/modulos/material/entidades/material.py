#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Material
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import  Mapped, mapped_column
from src.database.database import Base

#Criação da entidade Material
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

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DISPONIVEL"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "material",
    }
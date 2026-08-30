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

#Método para atualização de materiais
    def atualizar(
            self,
            titulo=None,
            ano_publi=None,
            categoria_id=None,
            editora_id=None
    ):
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
            self.is_active = False
        else:
            raise ValueError("Material já inativado")

    # Ativação do Material
    def ativar(self):
        if not self.is_active:
            self.is_active = True
        else:
            raise ValueError("Material já ativado")

    # Verifica se o Material está ativo
    def esta_ativo(self):
        return self.is_active

    # Verifica se o Material está ativo e disponível
    def esta_disponivel(self):
        return self.is_active and self.status == "DISPONIVEL"
from abc import ABC, abstractmethod
# importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Material
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

# Criação da entidade Material


class Material(Base, ABC):
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

    # [RF-ACER-002] Atualização do Acervo
    def atualizar_material(self, titulo, ano_publi, categoria_id, editora_id):
        if not self.is_active:
            raise ValueError("Material inativo")

        self.titulo = titulo
        self.ano_publi = ano_publi
        self.categoria_id = categoria_id
        self.editora_id = editora_id

    # [RF-ACER-003] [RN-ACER-013] Inativação do Material
    def inativar_material(self):
        if self.is_active:
            self.is_active = False
        else:
            raise ValueError("Material já inativado")

    # Ativação do Material
    def ativar_material(self):
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

    # Método abstrato implementado obrigatoriamente pelas subclasses
    @abstractmethod
    def descricao(self):
        pass

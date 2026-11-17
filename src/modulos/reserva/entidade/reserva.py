#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Reserva
from sqlalchemy import String, ForeignKey, Boolean, DateTime, func, Enum
from sqlalchemy.orm import  Mapped, mapped_column, validates
from sqlalchemy.ext.hybrid import hybrid_property

from src.compartilhado.enum import StatusReserva
from src.database.database import Base
from datetime import datetime, timedelta

#Criação da entidade Reserva
class Reserva(Base):
    __tablename__ = "reserva"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("cliente.id"),
        nullable=False
    )

    material_id: Mapped[int | None] = mapped_column(
        ForeignKey("material.id"),
        nullable=True
    )

    data: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    #Atributos privados mapeados para as colunas de mesmo nome, alterados somente por cancelar, concluir e verificar_expiracao
    _status: Mapped[StatusReserva] = mapped_column(
        "status",
        Enum(StatusReserva),
        nullable=False,
        default=StatusReserva.ABERTA
    )

    _is_active: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        nullable=False,
        default=True
    )

    #Declaração do construtor da Classe
    def __init__(
            self,
            titulo,
            cliente_id,
            material_id=None
    ):
        self.titulo = titulo
        self.cliente_id = cliente_id
        self.material_id = material_id
        self.data = datetime.now()
        self._status = StatusReserva.ABERTA
        self._is_active = True

    #Getters dos atributos somente leitura
    @hybrid_property
    def status(self):
        return self._status

    @hybrid_property
    def is_active(self):
        return self._is_active

    @validates("titulo")
    def validar_titulo(self, chave, titulo):
        return self._normalizar_titulo(titulo)

    @staticmethod
    def _normalizar_titulo(titulo):
        return titulo.strip().lower()

    #[RN-RES-006] Cancelamento Automático da Reserva
    #[RN-RES-005] Prazo da Reserva
    def verificar_expiracao(self):
        if self.is_active:
            prazo = self.data + timedelta(days=10)

            if datetime.now() > prazo:
                self._status = StatusReserva.EXPIRADA
                self._is_active = False
                return True
            else:
                return False
        else:
            return False

    #[RN-RES-007] Cancelamento de Reserva Ativa
    def cancelar(self):
        if self.is_active:
            self._status = StatusReserva.CANCELADA
            self._is_active = False
        else:
            raise ValueError("Essa reserva já foi desativada")

    #Encerra a reserva quando o empréstimo do material reservado é registrado
    def concluir(self):
        if self.is_active:
            self._status = StatusReserva.ATENDIDA
            self._is_active = False
        else:
            raise ValueError("Essa reserva já foi desativada")

    #Associa à reserva o material que ficou disponível para o cliente
    def vincular_material(self, material_id):
        self.material_id = material_id

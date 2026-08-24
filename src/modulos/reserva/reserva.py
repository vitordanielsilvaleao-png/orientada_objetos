#importando da biblioteca SQLAlchemy as ferramentas necessárias para criação da entidade Reserva
from sqlalchemy import String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import  Mapped, mapped_column
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

    material_id: Mapped[int] = mapped_column(
        ForeignKey("material.id"),
        nullable=True
    )

    data: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    #[RN-RES-006] Cancelamento Automático da Reserva
    #[RN-RES-005] Prazo da Reserva
    def verificar_expiração(self):
        if self.is_active:
            prazo = self.data + timedelta(days=10)
            
            if datetime.now() > prazo:
                self.is_active = False
                return True
        else:    
            return False
    
    #[RN-RES-007] Cancelamento de Reserva Ativa
    def cancelar(self):
        if self.is_active:
            self.is_active = False
        else:
            raise ValueError("Essa reserva já foi desativada")

    def validar_reserva(self):
        return self.is_active
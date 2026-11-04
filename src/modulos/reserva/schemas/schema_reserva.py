#Import das bibliotecas necessárias para o funcionamento do Schema
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from src.compartilhado.enum import StatusReserva

#Schema para armazenamento dos dados de cadastro de reservas
class SchemaReservaCadastro(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    cliente_id: int = Field(gt=0, le=2147483647)

#Schema para retorno dos dados de reservas, lidos a partir dos getters da entidade
class SchemaReservaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    cliente_id: int
    material_id: int | None
    data: datetime
    status: StatusReserva
    is_active: bool

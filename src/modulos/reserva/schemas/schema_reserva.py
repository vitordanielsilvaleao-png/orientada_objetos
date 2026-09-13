#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de reservas
class SchemaReservaCadastro(BaseModel):
    titulo: str
    cliente_id: int
    material_id: int | None = None
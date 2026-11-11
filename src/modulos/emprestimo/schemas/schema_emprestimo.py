
from datetime import datetime
from pydantic import BaseModel, Field

#Schema para armazenamento dos dados de cadastro de empréstimos
class SchemaEmprestimoCadastro(BaseModel):
    material_id: int = Field(gt=0, le=2147483647)
    cliente_id: int = Field(gt=0, le=2147483647)

class SchemaEmprestimoResposta(BaseModel):
    id: int
    material_id: int
    cliente_id: int
    data_emprestimo: datetime
    data_devolucao: datetime | None
    status: str
    is_active: bool
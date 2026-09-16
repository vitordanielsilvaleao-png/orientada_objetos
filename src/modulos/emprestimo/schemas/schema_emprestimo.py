from datetime import datetime
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de empréstimos
class SchemaEmprestimoCadastro(BaseModel):
    material_id: int
    cliente_id: int

class SchemaEmprestimoResposta(BaseModel):
    id: int
    material_id: int
    cliente_id: int
    data_emprestimo: datetime
    data_devolucao: datetime | None
    status: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }
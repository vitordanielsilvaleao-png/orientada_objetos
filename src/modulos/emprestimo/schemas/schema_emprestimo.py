from datetime import datetime
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de empréstimos
class SchemaEmprestimoCadastro(BaseModel):
    material_id: int
    cliente_id: int

#Schema que armazena a data de devolução do empréstimo
class SchemaEmprestimoDevolucao(BaseModel):
    data_devolucao: datetime
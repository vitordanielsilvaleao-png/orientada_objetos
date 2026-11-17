#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict, Field

#Schema para armazenamento dos dados de cadastro de autores
class SchemaAutorCadastro(BaseModel):
    nome: str = Field(min_length=1, max_length=255)

#Schema para armazenamento dos dados de atualização de autores
class SchemaAutorAtualizacao(BaseModel):
    nome: str = Field(min_length=1, max_length=255)

#Schema para retorno dos dados de autores
class SchemaAutorResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str

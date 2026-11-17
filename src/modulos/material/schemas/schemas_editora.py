#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict, Field

#Schema para armazenamento dos dados de cadastro de editoras
class SchemaEditoraCadastro(BaseModel):
    nome: str = Field(min_length=1, max_length=255)

#Schema para armazenamento dos dados de atualização de editoras
class SchemaEditoraAtualizacao(BaseModel):
    nome: str = Field(min_length=1, max_length=255)

#Schema para retorno dos dados de editoras
class SchemaEditoraResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str

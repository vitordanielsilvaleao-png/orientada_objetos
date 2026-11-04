#Import das bibliotecas necessárias para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict, Field

from src.compartilhado.enum import StatusMaterial

#Schema para armazenamento dos dados de cadastro de revistas
class SchemaRevistaCadastro(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    ano_publi: int = Field(gt=0, le=2147483647)
    categoria_id: int = Field(gt=0, le=2147483647)
    editora_id: int = Field(gt=0, le=2147483647)
    issn: str = Field(min_length=8, max_length=9)
    edicao: int = Field(gt=0, le=2147483647)

#Schema para armazenamento dos dados de atualização de revistas
class SchemaRevistaAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    ano_publi: int | None = Field(default=None, gt=0, le=2147483647)
    categoria_id: int | None = Field(default=None, gt=0, le=2147483647)
    editora_id: int | None = Field(default=None, gt=0, le=2147483647)
    #O ISSN não é incluído aqui, pois identifica a publicação e não deve ser alterado
    edicao: int | None = Field(default=None, gt=0, le=2147483647)

#Schema para retorno dos dados de revistas
class SchemaRevistaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publi: int
    categoria_id: int
    editora_id: int
    issn: str
    edicao: int
    status: StatusMaterial
    is_active: bool

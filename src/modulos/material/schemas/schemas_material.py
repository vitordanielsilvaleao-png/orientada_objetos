#Import das bibliotecas necessárias para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict

from src.compartilhado.enum import StatusMaterial

#Schema para retorno dos dados de materiais do catálogo, lidos a partir dos getters da entidade
class SchemaMaterialResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publi: int
    categoria_id: int
    editora_id: int
    tipo: str
    status: StatusMaterial
    is_active: bool

#Schema para retorno de uma quantidade de materiais
class SchemaQuantidadeMaterial(BaseModel):
    quantidade: int

#Schema para retorno da quantidade de materiais agrupada por categoria
class SchemaQuantidadePorCategoria(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    categoria_id: int
    quantidade: int

#Schema para retorno da quantidade de materiais agrupada por tipo
class SchemaQuantidadePorTipo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo: str
    quantidade: int

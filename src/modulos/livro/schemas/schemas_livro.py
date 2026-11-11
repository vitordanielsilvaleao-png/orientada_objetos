#Import das bibliotecas necessárias para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict, Field

from src.compartilhado.enum import StatusMaterial

#Schema para armazenamento dos dados de cadastro de livros
class SchemaLivroCadastro(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    ano_publi: int = Field(gt=0, le=2147483647)
    categoria_id: int = Field(gt=0, le=2147483647)
    editora_id: int = Field(gt=0, le=2147483647)
    isbn: str = Field(min_length=13, max_length=17)
    autor_id: int = Field(gt=0, le=2147483647)

#Schema para armazenamento dos dados de atualização de livros
class SchemaLivroAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    ano_publi: int | None = Field(default=None, gt=0, le=2147483647)
    categoria_id: int | None = Field(default=None, gt=0, le=2147483647)
    editora_id: int | None = Field(default=None, gt=0, le=2147483647)
    autor_id: int | None = Field(default=None, gt=0, le=2147483647)

#Schema para retorno dos dados de livros
class SchemaLivroResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publi: int
    categoria_id: int
    editora_id: int
    isbn: str
    autor_id: int
    status: StatusMaterial
    is_active: bool

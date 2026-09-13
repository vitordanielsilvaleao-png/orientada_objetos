#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de revistas
class SchemaRevistaCadastro(BaseModel):
    titulo: str
    ano_publi: int
    categoria_id: int
    editora_id: int
    issn: str
    edicao: int

#Schema para armazenamento dos dados de atualização de revistas
class SchemaRevistaAtualizacao(BaseModel):
    titulo: str | None = None
    ano_publi: int | None = None
    categoria_id: int | None = None
    editora_id: int | None = None
    issn: str | None = None
    edicao: int | None = None
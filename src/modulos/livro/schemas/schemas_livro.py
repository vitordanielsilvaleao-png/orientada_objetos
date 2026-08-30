#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de livros
class SchemaLivroCadastro(BaseModel):
    titulo: str
    ano_publi: int
    categoria_id: int
    editora_id: int
    isbn: str
    autor_id: int

#Schema para armazenamento dos dados de atualização de livros
class SchemaLivroAtualizacao(BaseModel):
    titulo: str | None = None
    ano_publi: int | None = None
    categoria_id: int | None = None
    editora_id: int | None = None
    isbn: str | None = None
    autor_id: int | None = None
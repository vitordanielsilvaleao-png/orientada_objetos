from pydantic import BaseModel

class SchemaCategoriaCadastro(BaseModel):
    nome: str

class SchemaCategoriaAtualizacao(BaseModel):
    nome: str
#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de livros
class SchemaEditoraCadastro(BaseModel):
    nome: str
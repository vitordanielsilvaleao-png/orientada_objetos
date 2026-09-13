#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de autores
class SchemaAutorCadastro(BaseModel):
    nome: str
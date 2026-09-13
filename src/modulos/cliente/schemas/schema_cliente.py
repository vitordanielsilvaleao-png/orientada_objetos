#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel

#Schema para armazenamento dos dados de cadastro de clientes
class SchemaClienteCadastro(BaseModel):
    nome: str
    bairro: str
    rua: str
    numero: int
    complemento: str
    telefone: str

#Schema para armazenamento dos dados de atualização de clientes
class SchemaClienteAtualizacao(BaseModel):
    nome: str | None = None
    bairro: str | None = None
    rua: str | None = None
    numero: int | None = None
    complemento: str | None = None
    telefone: str | None = None

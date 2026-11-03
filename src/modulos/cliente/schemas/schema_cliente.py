#Import da biblioteca necessária para o funcionamento do Schema
from pydantic import BaseModel, ConfigDict, Field


#Schema para armazenamento dos dados de cadastro de clientes
class SchemaClienteCadastro(BaseModel):
    cpf: str = Field(min_length=11, max_length=14)
    nome: str = Field(min_length=3, max_length=255)
    bairro: str = Field(min_length=1, max_length=50)
    rua: str = Field(min_length=1, max_length=50)
    numero: int = Field(gt=0, le=2147483647)
    complemento: str | None = Field(default=None, max_length=50)
    telefone: str = Field(min_length=1, max_length=15)

#Schema para armazenamento dos dados de atualização de clientes
class SchemaClienteAtualizacao(BaseModel):
    #O CPF não é incluído aqui para impedir que seja alterado indevidamente
    nome: str | None = Field(default=None, min_length=3, max_length=255)
    bairro: str | None = Field(default=None, min_length=1, max_length=50)
    rua: str | None = Field(default=None, min_length=1, max_length=50)
    numero: int | None = Field(default=None, gt=0, le=2147483647)
    complemento: str | None = Field(default=None, max_length=50)
    telefone: str | None = Field(default=None, min_length=1, max_length=15)

#Schema para retorno dos dados de clientes, lidos a partir dos getters da entidade
class SchemaClienteResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cpf: str
    nome: str
    bairro: str
    rua: str
    numero: int
    complemento: str | None
    telefone: str
    is_active: bool

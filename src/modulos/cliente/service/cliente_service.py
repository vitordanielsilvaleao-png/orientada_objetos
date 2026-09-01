#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session

from cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from compartilhado.base_service import BaseService


#Declaração da classe ClienteService
class ClienteService(BaseService):

    # Declaração do construtor da classe ClienteService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaClienteCadastro):
        pass

    def visualizar(self):
        pass

    def atualizar(self, cliente_id:int, data:SchemaClienteAtualizacao):
        pass

    def inativar(self, cliente_id:int):
        pass

    def ativar(self, cliente_id:int):
        pass
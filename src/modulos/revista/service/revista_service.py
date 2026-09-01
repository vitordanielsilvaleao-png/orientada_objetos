#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService
from revista.schemas.schamas_revista import SchemaRevistaCadastro, SchemaRevistaAtualizacao


#Declaração da classe RevistaService
class RevistaService(BaseService):

    #Declaração do construtor da classe
    def __init__(self, session:Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaRevistaCadastro):
        pass

    def visualizar(self):
        pass

    def atualizar(self, revista_id:int ,data:SchemaRevistaAtualizacao):
        pass

    def inativar(self, revista_id:int):
        pass

    def ativar(self, revista_id:int):
        pass
#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session

from compartilhado.base_service import BaseService
from src.modulos.reserva.schemas.schema_reserva import SchemaReservaCadastro


#Declaração da classe ReservaService
class ReservaService (BaseService):

    #Declaração do construtor da classe
    def __init__(self, session:Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaReservaCadastro):
        pass

    def visualizar(self):
        pass

    def visualizar_expiradas(self):
        pass

    def inativar(self, reserva_id:int):
        pass
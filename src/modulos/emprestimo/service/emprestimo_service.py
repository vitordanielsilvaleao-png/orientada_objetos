#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService
from emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro, SchemaEmprestimoDevolucao


#Declaração da classe EmprestimoService
class EmprestimoService(BaseService):

    # Declaração do construtor da classe EmprestimoService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data:SchemaEmprestimoCadastro):
        pass

    def visualizar(self):
        pass

    def visualizar_atrasados(self):
        pass

    def registrar_devolucao(self, emprestimo_id:int, data_devolucao:SchemaEmprestimoDevolucao):
        pass
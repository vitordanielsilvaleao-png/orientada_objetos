from fastapi import APIRouter, Depends
from emprestimo.depends.depends_emprestimo import obter_emprestimo_service
from emprestimo.schemas.schema_emprestimo import SchemaEmprestimoCadastro, SchemaEmprestimoDevolucao
from emprestimo.service.emprestimo_service import EmprestimoService


#Declaração da classe EmprestimoRouter
class EmprestimoRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{emprestimo_id}", self.registrar_devolucao, methods=["PATCH"])

    #Método para cadastros de empréstimos
    @staticmethod
    def cadastrar(data:SchemaEmprestimoCadastro, emprestimo_service:EmprestimoService = Depends(obter_emprestimo_service)):

        """Rota usada para cadastrar um novo empréstimo no sistema"""

        emprestimo_cadastrar = emprestimo_service.cadastrar(data)
        return emprestimo_cadastrar

    #Método para visualização de empréstimos
    @staticmethod
    def visualizar(emprestimo_service:EmprestimoService = Depends(obter_emprestimo_service)):

        """Rota usada para visualizar os empréstimos cadastrados no sistema"""

        return emprestimo_service.visualizar()

    #Método para registro de devolução
    @staticmethod
    def registrar_devolucao(emprestimo_id:int, data:SchemaEmprestimoDevolucao ,emprestimo_service:EmprestimoService = Depends(obter_emprestimo_service)):

        """Rota usada para registrar a devolução os empréstimos no sistema"""

        return emprestimo_service.registrar_devolucao(emprestimo_id, data)
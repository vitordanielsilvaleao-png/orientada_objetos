#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends, status
from src.modulos.emprestimo.depends.depends_emprestimo import obter_emprestimo_service
from src.modulos.emprestimo.schemas.schema_emprestimo import (
    SchemaEmprestimoCadastro,
    SchemaEmprestimoResposta
)
from src.modulos.emprestimo.service.emprestimo_service import EmprestimoService

#Declaração da classe EmprestimoRouter
class EmprestimoRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/emprestimos", tags=["Emprestimos"])
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"], response_model=SchemaEmprestimoResposta, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("", self.visualizar, methods=["GET"], response_model=list[SchemaEmprestimoResposta])
        self.router.add_api_route("/abertos", self.visualizar_abertos, methods=["GET"], response_model=list[SchemaEmprestimoResposta])
        self.router.add_api_route("/atrasados", self.visualizar_atrasados, methods=["GET"], response_model=list[SchemaEmprestimoResposta])
        self.router.add_api_route("/{emprestimo_id}/devolver", self.registrar_devolucao, methods=["PATCH"], response_model=SchemaEmprestimoResposta)

    #Método para cadastro de empréstimos
    @staticmethod
    def cadastrar(
            data: SchemaEmprestimoCadastro,
            emprestimo_service: EmprestimoService = Depends(obter_emprestimo_service)
    ):
        """Rota usada para cadastrar um novo empréstimo no sistema"""
        emprestimo_cadastrar = emprestimo_service.cadastrar(data)
        return emprestimo_cadastrar

    #Método para visualizar empréstimos
    @staticmethod
    def visualizar(emprestimo_service: EmprestimoService = Depends(obter_emprestimo_service)):
        """Rota usada para visualizar os empréstimos cadastrados no sistema"""
        return emprestimo_service.visualizar()

    #Método para visualizar empréstimos abertos
    @staticmethod
    def visualizar_abertos(emprestimo_service: EmprestimoService = Depends(obter_emprestimo_service)):
        """Rota usada para visualizar os empréstimos abertos cadastrados no sistema"""
        return emprestimo_service.visualizar_abertos()

    #Método para visualizar empréstimos atrasados
    @staticmethod
    def visualizar_atrasados(emprestimo_service: EmprestimoService = Depends(obter_emprestimo_service)):
        """Rota usada para visualizar os empréstimos atrasados cadastrados no sistema"""
        return emprestimo_service.visualizar_atrasados()

    #Método para registro de devolução
    @staticmethod
    def registrar_devolucao(
            emprestimo_id: int,
            emprestimo_service: EmprestimoService = Depends(obter_emprestimo_service)
    ):
        """Rota usada para registrar a devolução de empréstimos no sistema"""
        return emprestimo_service.registrar_devolucao(emprestimo_id)
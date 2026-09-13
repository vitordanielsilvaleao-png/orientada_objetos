from fastapi import APIRouter, Depends
from revista.depends.depends_revista import obter_revista_service
from revista.schemas.schamas_revista import SchemaRevistaCadastro, SchemaRevistaAtualizacao
from revista.service.revista_service import RevistaService


#Declaração da classe RevistaRouter
class RevistaRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    # Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{revista_id}", self.atualizar, methods=["PATCH"])
        self.router.add_api_route("/{revista_id}", self.inativar, methods=["DELETE"])
        self.router.add_api_route("/ativar/{revista_id}", self.ativar, methods=["PATCH"])

    #Método para cadastro de revistas
    @staticmethod
    def cadastrar(data:SchemaRevistaCadastro, revista_service:RevistaService = Depends(obter_revista_service)):

        """Rota usada para cadastrar uma nova revista no sistema"""

        revista_cadastrar = revista_service.cadastrar(data)
        return revista_cadastrar

    #Método para visualização de revistas
    @staticmethod
    def visualizar(revista_service:RevistaService = Depends(obter_revista_service)):

        """Rota usada para visualizar revistas cadastradas no sistema"""

        return revista_service.visualizar()

    #Método para atualização de revistas
    @staticmethod
    def atualizar(revista_id:int, data:SchemaRevistaAtualizacao, revista_service:RevistaService = Depends(obter_revista_service)):

        """Rota usada para atualizar revistas cadastradas no sistema"""

        revista_atualizar = revista_service.atualizar(revista_id, data)
        return revista_atualizar

    #Método para inativação de revistas
    @staticmethod
    def inativar(revista_id:int, revista_service:RevistaService = Depends(obter_revista_service)):

        """Rota usada para inativar revistas cadastradas no sistema"""

        return revista_service.inativar(revista_id)

    #Método para ativação de revistas
    @staticmethod
    def ativar(revista_id:int, revista_service:RevistaService = Depends(obter_revista_service)):

        """Rota usada para ativar revistas cadastradas no sistema"""

        return revista_service.ativar(revista_id)
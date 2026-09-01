#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends
from cliente.depends.depends_cliente import obter_cliente_service
from cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from cliente.service.cliente_service import ClienteService

#Declaração da classe ClienteRouter
class ClienteRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{cliente_id}", self.atualizar, methods=["PATCH"])
        self.router.add_api_route("/{cliente_id}", self.inativar, methods=["DELETE"])
        self.router.add_api_route("/ativar/{cliente_id}", self.ativar, methods=["PATCH"])

    #Método para cadastro de clientes
    @staticmethod
    def cadastrar(data:SchemaClienteCadastro, cliente_service:ClienteService = Depends(obter_cliente_service)):

        """Rota usada para cadastrar um novo cliente no sistema"""

        cliente_cadastrar = cliente_service.cadastrar(data)
        return cliente_cadastrar

    #Método para visualizar clientes
    @staticmethod
    def visualizar(cliente_service:ClienteService = Depends(obter_cliente_service)):

        """Rota usada para visualizar os clientes cadastrados no sistema"""

        return cliente_service.visualizar()

    #Método para atualizar clientes
    @staticmethod
    def atualizar(cliente_id:int, data:SchemaClienteAtualizacao, cliente_service:ClienteService = Depends(obter_cliente_service)):

        """Rota usada para atualizar clientes no sistema"""

        cliente_atualizar = cliente_service.atualizar(cliente_id, data)
        return cliente_atualizar

    #Método para inativação de clientes
    @staticmethod
    def inativar(cliente_id:int, cliente_service:ClienteService = Depends(obter_cliente_service)):

        """Rota usada para inativar clientes no sistema"""

        return cliente_service.inativar(cliente_id)

    #Método para ativação clientes

    @staticmethod
    def ativar(cliente_id:int, cliente_service:ClienteService = Depends(obter_cliente_service)):

        """Rota usada para ativar clientes no sistema"""

        return cliente_service.ativar(cliente_id)
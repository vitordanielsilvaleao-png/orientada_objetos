#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends
from modulos.livro.depends.depends_livro import obter_livro_service
from modulos.livro.schemas.schemas_livro import SchemaLivroCadastro, SchemaLivroAtualizacao
from modulos.livro.services.livro_service import LivroService

#Declaração da classe LivroRouter
class LivroRouter:

    #Declaração do construtor da classe LivroRouter
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{livro_id}", self.atualizar, methods=["PATCH"])
        self.router.add_api_route("/{livro_id}", self.inativar, methods=["DELETE"])
        self.router.add_api_route("/ativar/{livro_id}", self.ativar, methods=["PATCH"])

    #Método para cadastro de livros
    @staticmethod
    def cadastrar(data:SchemaLivroCadastro, livro_service:LivroService = Depends(obter_livro_service)):

        """Rota usada para cadastrar um novo livro no sistema"""

        livro_cadastrar = livro_service.cadastrar(data)
        return livro_cadastrar

    #Método para visualização de livros
    @staticmethod
    def visualizar(livro_service:LivroService = Depends(obter_livro_service)):

        """Rota usada para visualizar os livros cadastrados no sistema"""

        return livro_service.visualizar()

    #Método para atualização de livros
    @staticmethod
    def atualizar(livro_id:int, data:SchemaLivroAtualizacao, livro_service:LivroService = Depends(obter_livro_service)):

        """Rota usada para atualizar um livro no sistema"""

        livro_atualizar = livro_service.atualizar(livro_id, data)
        return livro_atualizar

    #Método para inativação de livros
    @staticmethod
    def inativar(livro_id:int, livro_service:LivroService = Depends(obter_livro_service)):

        """Rota usada para inativar um livro no sistema"""

        return livro_service.inativar(livro_id)

    #Método para ativação de livros
    @staticmethod
    def ativar(livro_id: int, livro_service: LivroService = Depends(obter_livro_service)):

        """Rota usada para ativar um livro no sistema"""

        return livro_service.ativar(livro_id)
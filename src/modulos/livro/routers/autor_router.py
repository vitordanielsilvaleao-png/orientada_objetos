#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends
from depends.depends_autor import obter_autor_service
from services.autor_service import AutorService


#Declaração da classe LivroRouter
class AutorRouter:

    #Declaração do construtor da classe LivroRouter
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("/{nome_autor}", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{autor_id}/{nome_autor}", self.atualizar, methods=["PATCH"])

    #Método para cadastro de autores
    @staticmethod
    def cadastrar(nome_autor:str, autor_service:AutorService = Depends(obter_autor_service)):

        """Rota usada para cadastrar um novo autor no sistema"""

        autor_cadastrar = autor_service.cadastrar(nome_autor)
        return autor_cadastrar

    #Método para visualização de autores
    @staticmethod
    def visualizar(autor_service:AutorService = Depends(obter_autor_service)):

        """Rota usada para visualizar os autores cadastrados no sistema"""

        return autor_service.visualizar()

    #Método para atualização de livros
    @staticmethod
    def atualizar(autor_id:int, nome_autor:str, autor_service:AutorService = Depends(obter_autor_service)):

        """Rota usada para atualizar um autor no sistema"""

        autor_atualizar = autor_service.atualizar(autor_id, nome_autor)
        return autor_atualizar
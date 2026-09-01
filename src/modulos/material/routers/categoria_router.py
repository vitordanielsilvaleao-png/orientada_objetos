#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends
from src.modulos.material.depends.depends_categoria import obter_categoria_service
from src.modulos.material.service.categoria_service import CategoriaService

#Declaração da classe CategoriaRouter
class CategoriaRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("/{nome_categoria}", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/{categoria_id}/{nome_categoria}", self.atualizar, methods=["PATCH"])

    #Método para cadastro de categorias
    @staticmethod
    def cadastrar(nome_categoria:str, categoria_service:CategoriaService = Depends(obter_categoria_service)):

        """Rota usada para cadastrar uma nova categoria no sistema"""

        categoria_cadastrar = categoria_service.cadastrar(nome_categoria)
        return categoria_cadastrar

    #Método para visualização de categorias
    @staticmethod
    def visualizar(categoria_service:CategoriaService = Depends(obter_categoria_service)):

        """Rota usada para visualizar as categorias cadastradas no sistema"""

        return categoria_service.visualizar()

    #Método para atualização de livros
    @staticmethod
    def atualizar(categoria_id:int, nome_categoria:str, categoria_service:CategoriaService = Depends(obter_categoria_service)):

        """Rota usada para atualizar um autor no sistema"""

        categoria_atualizar = categoria_service.atualizar(categoria_id, nome_categoria)
        return categoria_atualizar
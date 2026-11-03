#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends, status
from src.modulos.livro.depends.depends_autor import obter_autor_service
from src.modulos.livro.schemas.schemas_autor import (
    SchemaAutorCadastro,
    SchemaAutorAtualizacao,
    SchemaAutorResposta
)
from src.modulos.livro.services.autor_service import AutorService


#Declaração da classe AutorRouter
class AutorRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"], response_model=SchemaAutorResposta, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("", self.visualizar, methods=["GET"], response_model=list[SchemaAutorResposta])
        self.router.add_api_route("/{autor_id}", self.atualizar, methods=["PATCH"], response_model=SchemaAutorResposta)

    #Método para cadastro de autores
    @staticmethod
    def cadastrar(
            data: SchemaAutorCadastro,
            autor_service: AutorService = Depends(obter_autor_service)
    ):

        """Rota usada para cadastrar um novo autor no sistema"""

        autor_cadastrar = autor_service.cadastrar(data)
        return autor_cadastrar

    #Método para visualização de autores
    @staticmethod
    def visualizar(autor_service: AutorService = Depends(obter_autor_service)):

        """Rota usada para visualizar os autores cadastrados no sistema"""

        return autor_service.visualizar()

    #Método para atualização de autores
    @staticmethod
    def atualizar(
            autor_id: int,
            data: SchemaAutorAtualizacao,
            autor_service: AutorService = Depends(obter_autor_service)
    ):

        """Rota usada para atualizar um autor no sistema"""

        autor_atualizar = autor_service.atualizar(autor_id, data)
        return autor_atualizar

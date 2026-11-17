#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends, status
from src.modulos.material.schemas.schemas_editora import (
    SchemaEditoraCadastro,
    SchemaEditoraAtualizacao,
    SchemaEditoraResposta
)
from src.modulos.material.depends.depends_editora import obter_editora_service
from src.modulos.material.service.editora_service import EditoraService

#Declaração da classe EditoraRouter
class EditoraRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"], response_model=SchemaEditoraResposta, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("", self.visualizar, methods=["GET"], response_model=list[SchemaEditoraResposta])
        self.router.add_api_route("/{editora_id}", self.atualizar, methods=["PATCH"], response_model=SchemaEditoraResposta)

    #Método para cadastro de editoras
    @staticmethod
    def cadastrar(
            data: SchemaEditoraCadastro,
            editora_service: EditoraService = Depends(obter_editora_service)
    ):

        """Rota usada para cadastrar uma nova editora no sistema"""

        editora_cadastrar = editora_service.cadastrar(data)
        return editora_cadastrar

    #Método para visualização de editoras
    @staticmethod
    def visualizar(editora_service: EditoraService = Depends(obter_editora_service)):

        """Rota usada para visualizar as editoras cadastradas no sistema"""

        return editora_service.visualizar()

    #Método para atualização de editoras
    @staticmethod
    def atualizar(
            editora_id: int,
            data: SchemaEditoraAtualizacao,
            editora_service: EditoraService = Depends(obter_editora_service)
    ):

        """Rota usada para atualizar uma editora no sistema"""

        editora_atualizar = editora_service.atualizar(editora_id, data)
        return editora_atualizar

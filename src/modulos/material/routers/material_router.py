#Import das bibliotecas necessárias para o funcionamento do sistema
from fastapi import APIRouter, Depends

from src.modulos.material.schemas.schemas_material import (
    SchemaMaterialResposta,
    SchemaQuantidadeMaterial,
    SchemaQuantidadePorCategoria,
    SchemaQuantidadePorTipo
)
from src.modulos.material.depends.depends_material import obter_material_service
from src.modulos.material.service.material_service import MaterialService

#Declaração da classe MaterialRouter
class MaterialRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.consultar_catalogo_geral, methods=["GET"], response_model=list[SchemaMaterialResposta])
        self.router.add_api_route("/disponiveis", self.consultar_materiais_disponiveis, methods=["GET"], response_model=list[SchemaMaterialResposta])
        self.router.add_api_route("/emprestados", self.consultar_materiais_emprestados, methods=["GET"], response_model=list[SchemaMaterialResposta])
        self.router.add_api_route("/quantidade/total", self.contar_quantidade_total, methods=["GET"], response_model=SchemaQuantidadeMaterial)
        self.router.add_api_route("/quantidade/disponiveis", self.contar_quantidade_disponivel, methods=["GET"], response_model=SchemaQuantidadeMaterial)
        self.router.add_api_route("/quantidade/categoria", self.contar_materiais_por_categoria, methods=["GET"], response_model=list[SchemaQuantidadePorCategoria])
        self.router.add_api_route("/quantidade/tipo", self.contar_materiais_por_tipo, methods=["GET"], response_model=list[SchemaQuantidadePorTipo])

    #Método para consulta do catálogo geral de materiais
    @staticmethod
    def consultar_catalogo_geral(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para consultar o catálogo geral de materiais do sistema"""

        return material_service.consultar_catalogo_geral()

    #Método para consulta dos materiais disponíveis
    @staticmethod
    def consultar_materiais_disponiveis(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para consultar os materiais disponíveis no sistema"""

        return material_service.consultar_materiais_disponiveis()

    #Método para consulta dos materiais emprestados
    @staticmethod
    def consultar_materiais_emprestados(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para consultar os materiais emprestados no sistema"""

        return material_service.consultar_materiais_emprestados()

    #Método para contagem do total de materiais
    @staticmethod
    def contar_quantidade_total(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para contar a quantidade total de materiais do sistema"""

        return {"quantidade": material_service.contar_quantidade_total()}

    #Método para contagem dos materiais disponíveis
    @staticmethod
    def contar_quantidade_disponivel(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para contar a quantidade de materiais disponíveis no sistema"""

        return {"quantidade": material_service.contar_quantidade_disponivel()}

    #Método para contagem dos materiais por categoria
    @staticmethod
    def contar_materiais_por_categoria(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para contar os materiais do sistema agrupados por categoria"""

        return material_service.contar_materiais_por_categoria()

    #Método para contagem dos materiais por tipo
    @staticmethod
    def contar_materiais_por_tipo(material_service: MaterialService = Depends(obter_material_service)):

        """Rota usada para contar os materiais do sistema agrupados por tipo"""

        return material_service.contar_materiais_por_tipo()

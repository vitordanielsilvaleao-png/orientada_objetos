from fastapi import APIRouter, Depends

from reserva.depends.depends_reserva import obter_reserva_service
from reserva.schemas.schema_reserva import SchemaReservaCadastro
from reserva.service.reserva_service import ReservaService


#Declaração da classe ReservaRouter
class ReservaRouter:

    #Declaração do construtor da classe
    def __init__(self):
        self.router = APIRouter()
        self.adicionar_rotas()

    #Método para adicionar rotas
    def adicionar_rotas(self):
        self.router.add_api_route("", self.cadastrar, methods=["POST"])
        self.router.add_api_route("", self.visualizar, methods=["GET"])
        self.router.add_api_route("/abertas", self.visualizar_abertos, methods=["GET"])
        self.router.add_api_route("/expiradas", self.visualizar_expiradas, methods=["GET"])
        self.router.add_api_route("/{reserva_id}", self.inativar, methods=["DELETE"])
        self.router.add_api_route("/{reserva_id}", self.atender_reserva, methods=["PATCH"])

    #Método para cadastro de reservas
    @staticmethod
    def cadastrar(data:SchemaReservaCadastro, reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para cadastrar uma nova reserva no sistema"""

        reserva_cadastrar = reserva_service.cadastrar(data)
        return reserva_cadastrar

    #Método para visualização de reservas
    @staticmethod
    def visualizar(reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para visualizar as reservas cadastradas no sistema"""

        return reserva_service.visualizar()

    #Método para visualização de reservas abertas
    @staticmethod
    def visualizar_abertos(reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para visualizar as reservas abertas cadastradas no sistema"""

        return reserva_service.visualizar_abertos()

    #Método para visualização de reservas expiradas
    @staticmethod
    def visualizar_expiradas(reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para visualizar as reservas expiradas cadastradas no sistema"""

        return reserva_service.visualizar_expiradas()

    #Método usado para inativação de reservas
    @staticmethod
    def inativar(reserva_id:int, reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para inativar reservas no sistema"""

        return reserva_service.inativar(reserva_id)

    #Método usado para inativação de reservas
    @staticmethod
    def atender_reserva(reserva_id:int, reserva_service:ReservaService = Depends(obter_reserva_service)):

        """Rota usada para atender reservas no sistema"""

        return reserva_service.atender_reserva(reserva_id)
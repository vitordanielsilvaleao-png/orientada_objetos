from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from reserva.service.reserva_service import ReservaService

#Instância um objeto da classe ReservaService com a sessão criada em database/depends.py
def obter_reserva_service(sessao:Session = Depends(obter_sessao)):
    return ReservaService(sessao)
from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from src.modulos.cliente.service.cliente_service import ClienteService

#Instância um objeto da classe ClienteService com a sessão criada em database/depends.py
def obter_cliente_service(sessao:Session = Depends(obter_sessao)):
    return ClienteService(sessao)
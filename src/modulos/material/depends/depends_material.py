from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.depends import obter_sessao
from src.modulos.material.service.material_service import MaterialService

#Instância um objeto da classe MaterialService com a sessão criada em database/depends.py
def obter_material_service(sessao:Session = Depends(obter_sessao)):
    return MaterialService(sessao)

from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.depends import obter_sessao
from src.modulos.material.service.categoria_service import CategoriaService

#Instância um objeto da classe CategoriaService com a sessão criada em database/depends_categoria.py
def obter_categoria_service(sessao:Session = Depends(obter_sessao)):
    return CategoriaService(sessao)
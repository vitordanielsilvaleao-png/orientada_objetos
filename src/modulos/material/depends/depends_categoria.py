from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from service.categoria_service import CategoriaService

#Instância um objeto da classe CategoriaService com a sessão criada em database/depends_categoria.py
def obter_categoria_service(sessao:Session = Depends(obter_sessao)):
    return CategoriaService(sessao)
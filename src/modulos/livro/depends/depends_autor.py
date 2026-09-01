from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from services.autor_service import AutorService


#Instância um objeto da classe AutorService com a sessão criada em database/depends_autor.py
def obter_autor_service(sessao:Session = Depends(obter_sessao)):
    return AutorService(sessao)
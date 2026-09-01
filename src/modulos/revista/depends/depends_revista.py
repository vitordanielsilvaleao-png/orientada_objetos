from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from revista.service.revista_service import RevistaService

#Instância um objeto de RevistaService juntamente com a sessão criada no arquivo depends/depends.py
def obter_revista_service(sessao:Session = Depends(obter_sessao)):
    return RevistaService(sessao)
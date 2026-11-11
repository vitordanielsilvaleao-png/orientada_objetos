from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.depends import obter_sessao
from src.modulos.material.service.editora_service import EditoraService

#Instância um objeto da classe EditoraService com a sessão criada em database/depends.py
def obter_editora_service(sessao:Session = Depends(obter_sessao)):
    return EditoraService(sessao)
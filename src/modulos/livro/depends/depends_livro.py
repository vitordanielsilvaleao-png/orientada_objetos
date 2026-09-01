from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from modulos.livro.services.livro_service import LivroService

#Instância um objeto da classe LivroService com a sessão criada em database/depends_livro.py
def obter_livro_service(sessao:Session = Depends(obter_sessao)):
    return LivroService(sessao)
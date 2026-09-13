from fastapi import Depends
from sqlalchemy.orm import Session
from database.depends import obter_sessao
from emprestimo.service.emprestimo_service import EmprestimoService

#Instância um objeto da classe EmprestimoService com a sessão criada em database/depends.py
def obter_emprestimo_service(sessao:Session = Depends(obter_sessao)):
    return EmprestimoService(sessao)
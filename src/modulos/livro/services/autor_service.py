from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.modulos.livro.entidades.autor import Autor
from compartilhado.base_service import BaseService

class AutorService(BaseService):

    # Declaração do construtor da classe AutorService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data):
        autor_existente = self.session.query(Autor).filter_by(nome=data.nome).first()
        if autor_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe um autor cadastrado com este nome."
            )

        novo_autor = Autor(
            nome=data.nome
        )

        self.salvar(novo_autor)
        self.session.refresh(novo_autor)
        
        return novo_autor
    
    #Método para visualizar autores
    def visualizar(self):
        return self.session.query(Autor).all()

    #Método para atualizar autor
    def atualizar(self, autor_id, nome_autor):
        autor_atualizar = self.session.query(Autor).filter_by(id=autor_id).first()
    
        if not autor_atualizar:
            raise HTTPException(
                status_code=404,
                detail="Autor não encontrado."
            )
            
        nome_existente = self.session.query(Autor).filter_by(nome=nome_autor).first()
        if nome_existente and nome_existente.id != autor_id:
            raise HTTPException(
                status_code=400,            
                detail="Já existe outro autor cadastrado com este nome."            
            )
        
        autor_atualizar.nome = nome_autor
                    
        self.session.commit()
        self.session.refresh(autor_atualizar)
            
        return autor_atualizar
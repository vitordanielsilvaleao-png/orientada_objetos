from fastapi import HTTPException
from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService
from src.modulos.material.schemas.schemas_editora import SchemaEditoraCadastro
from src.modulos.material.entidades.editora import Editora

class EditoraService(BaseService):

    # declaração do construtor da classe EditoraService
    def __init__(self, session: Session):
        super().__init__(session)

    # método para cadastrar editora
    def cadastrar(self, data:SchemaEditoraCadastro):
        # verifica se já existe uma editora com este nome no banco
        editora_existente = self.session.query(Editora).filter_by(nome=data.nome).first()
        if editora_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma editora cadastrada com este nome."
            )

        # cria a nova editora
        nova_editora = Editora(
            nome=data.nome
        )

        # salva no banco de dados
        self.salvar(nova_editora)
        self.session.refresh(nova_editora)
        
        return nova_editora

    # método para visualizar todas as editoras
    def visualizar(self):
        return self.session.query(Editora).all()

    # método para atualizar a editora
    def atualizar(self, editora_id: int, nome_editora: str):
        # busca a editora pelo ID
        editora_atualizar = self.session.query(Editora).filter_by(id=editora_id).first()

        # se não encontrar, retorna erro 404
        if not editora_atualizar:
            raise HTTPException(
                status_code=404,
                detail="Editora não encontrada."
            )

        # verifica se o novo nome já pertence a OUTRA editora
        nome_existente = self.session.query(Editora).filter_by(nome=nome_editora).first()
        if nome_existente and nome_existente.id != editora_id:
            raise HTTPException(
                status_code=400,
                detail="Já existe outra editora cadastrada com este nome."
            )

        # atualiza os dados e salva
        editora_atualizar.nome = nome_editora
        
        self.session.commit()
        self.session.refresh(editora_atualizar)

        return editora_atualizar
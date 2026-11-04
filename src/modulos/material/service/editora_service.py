#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.compartilhado.base_service import BaseService
from src.modulos.material.schemas.schemas_editora import SchemaEditoraCadastro, SchemaEditoraAtualizacao
from src.modulos.material.entidades.editora import Editora

#Declaração da classe EditoraService
class EditoraService(BaseService):

    #Método para cadastrar editoras
    def cadastrar(self, data:SchemaEditoraCadastro):
        nome_normalizado = Editora.normalizar_nome(data.nome)

        editora_existente = self.session.query(Editora).filter_by(nome=nome_normalizado).first()
        if editora_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma editora cadastrada com este nome."
            )

        try:
            nova_editora = Editora(
                nome=nome_normalizado
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(nova_editora)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe uma editora cadastrada com este nome."
            )

        self.session.refresh(nova_editora)
        return nova_editora

    #Método auxiliar para buscar uma editora pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, editora_id: int) -> Editora:
        editora = self.session.query(Editora).filter_by(id=editora_id).first()

        if not editora:
            raise HTTPException(
                status_code=404,
                detail="Editora não encontrada."
            )

        return editora

    #Método para visualizar editoras
    def visualizar(self):
        return self.session.query(Editora).all()

    #Método para atualizar editoras
    def atualizar(self, editora_id: int, data: SchemaEditoraAtualizacao):
        editora_atualizar = self._buscar_por_id(editora_id)

        nome_normalizado = Editora.normalizar_nome(data.nome)

        nome_existente = self.session.query(Editora).filter_by(nome=nome_normalizado).first()
        if nome_existente and nome_existente.id != editora_id:
            raise HTTPException(
                status_code=409,
                detail="Já existe outra editora cadastrada com este nome."
            )

        try:
            editora_atualizar.renomear(nome_normalizado)
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe outra editora cadastrada com este nome."
            )

        self.session.refresh(editora_atualizar)
        return editora_atualizar

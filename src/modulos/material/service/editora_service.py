from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService


class EditoraService(BaseService):

    # Declaração do construtor da classe EditoraService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data):
        pass

    def visualizar(self):
        pass

    def atualizar(self, editora_id, nome_editora):
        pass
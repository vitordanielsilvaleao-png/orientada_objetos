from sqlalchemy.orm import Session
from compartilhado.base_service import BaseService


class CategoriaService(BaseService):

    # Declaração do construtor da classe CategoriaService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data):
        pass

    def visualizar(self):
        pass

    def atualizar(self, categoria_id, nome_categoria):
        pass
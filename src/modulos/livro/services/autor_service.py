from sqlalchemy.orm import Session

from compartilhado.base_service import BaseService


class AutorService(BaseService):

    # Declaração do construtor da classe AutorService
    def __init__(self, session: Session):
        super().__init__(session)

    def cadastrar(self, data):
        pass

    def visualizar(self):
        pass

    def atualizar(self, autor_id, nome_autor):
        pass
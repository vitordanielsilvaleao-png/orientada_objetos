from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class BaseService(ABC):

    def __init__(self, session:Session):
        self.session = session

    def salvar(self, entidade):
        self.session.add(entidade)
        self.session.commit()

    @abstractmethod
    def cadastrar(self, data):
        pass

    @abstractmethod
    def visualizar(self):
        pass
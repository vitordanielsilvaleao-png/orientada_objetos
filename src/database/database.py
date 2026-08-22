#Importando da tabela SQLAlchemy os elementos de criação da Engine do Banco de Dados
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Declaração da classe do Banco de Dados que é utilizada para criação das sessões e tabelas do banco de dados
Base = declarative_base()
class Database:
    def __init__(self) -> None:
        self.engine = create_engine(
            'mysql+pymysql://root:123456@localhost:3306/biblioteca'
        )

        self.session = sessionmaker(bind=self.engine)

#Instanciação do objeto db da classe Database
db = Database()
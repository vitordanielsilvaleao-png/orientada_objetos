from src.database.database import db

#Função para obter uma sessão do banco de dados e encerrar se houver uma sessão aberta
def obter_sessao():
    try:
        session = db.session()
        yield session

    finally:
        session.close()
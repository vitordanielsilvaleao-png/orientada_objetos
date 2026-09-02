from sqlalchemy.orm import Session
from sqlalchemy import func
from src.modulos.material.entidades.material import Material
from modulos.livro.entidades.livro import Livro
from modulos.revista.revista import Revista

#Declaração da classe MaterialService:
class MaterialService:

    #Declaração do construtor da classe
    def __init__(self, sessao:Session):
        self.session = sessao

    #Método para consultar o catálogo geral de materiais
    def consultar_catalogo_geral(self):

        return self.session.query(Material).all()

    #Método para consultar o catálogo de materiais disponíveis
    def consultar_materiais_disponiveis(self):

        return self.session.query(Material).filter_by(
            status="DISPONIVEL"
        ).all()

    #Método para consultar o catálogo de materiais emprestados
    def consultar_materiais_emprestados(self):

        return self.session.query(Material).filter_by(
            status="EMPRESTADO"
        ).all()

    #Método para contar a quantidade total de materiais no catálogo
    def contar_quantidade_total(self):

        return self.session.query(
            func.count(Material.id)
        ).scalar()

    #Método para contar a quantidade de materiais disponíveis no catálogo
    def contar_quantidade_disponivel(self):

        return self.session.query(
            func.count(Material.id)
        ).filter_by(
            status="DISPONIVEL"
        ).scalar()

    #Método para contar os materiais do catálogo por categoria
    def contar_materiais_por_categoria(self):

        return self.session.query(
            Material.categoria_id,
            func.count(Material.id)
        ).group_by(
            Material.categoria_id
        ).all()

    #Método para contar os materiais do catálogo por tipo
    def contar_materiais_por_tipo(self):

        return self.session.query(
            Material.tipo,
            func.count(Material.id)
        ).group_by(
            Material.tipo
        ).all()
#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.modulos.cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from src.compartilhado.base_service import BaseService
from src.modulos.cliente.cliente import Cliente

#Declaração da classe ClienteService
class ClienteService(BaseService):

    # Declaração do construtor da classe ClienteService
    def __init__(self, session: Session):
        super().__init__(session)

    #Método para cadastrar clientes
    def cadastrar(self, data:SchemaClienteCadastro):

        cliente_existente = self.session.query(Cliente).filter_by(
            nome=data.nome
        ).first()

        if cliente_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um cliente com esse nome"
            )

        
        cliente_cadastrar = Cliente(
            nome = data.nome,
            bairro = data.bairro,
            rua = data.rua,
            numero = data.numero,
            complemento = data.complemento,
            telefone = data.telefone
        )

        self.salvar(cliente_cadastrar)
        self.session.refresh(cliente_cadastrar)
        return cliente_cadastrar

    #Método para visualizar clientes
    def visualizar(self):

         return self.session.query(Cliente).all()

    #Método para atualizar clientes
    def atualizar(self, cliente_id:int, data:SchemaClienteAtualizacao):

         cliente_atualizar = self.session.query(Cliente).filter_by(
             id = cliente_id
         ).first()

         if not cliente_atualizar:
             raise HTTPException(
                 status_code=404,
                 detail="Cliente não encontrado"
             )

         cliente_atualizar.atualizar_cliente(
             nome = data.nome,
             bairro = data.bairro,
             rua = data.rua,
             numero = data.numero,
             complemento = data.complemento,
             telefone = data.telefone
         )

         self.session.commit()
         self.session.refresh(cliente_atualizar)

         return cliente_atualizar

    #Método para inativar clientes
    def inativar(self, cliente_id:int):

         cliente_inativar = self.session.query(Cliente).filter_by(
             id=cliente_id
         ).first()

         if not cliente_inativar:
             raise HTTPException(
                 status_code=404,
                 detail="Cliente não encontrado"
             )

         cliente_inativar.inativar_cliente()
         self.session.commit()

    #Método para ativar clientes
    def ativar(self, cliente_id:int):

         cliente_ativar = self.session.query(Cliente).filter_by(
             id=cliente_id
         ).first()

         if not cliente_ativar:
             raise HTTPException(
                 status_code=404,
                 detail="Cliente não encontrado"
             )

         cliente_ativar.ativar_cliente()
         self.session.commit()
#Import das bibliotecas e classes necessárias para o funcionamento do sistema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.modulos.cliente.schemas.schema_cliente import SchemaClienteCadastro, SchemaClienteAtualizacao
from src.compartilhado.base_service import BaseService
from src.modulos.cliente.entidade.cliente import Cliente

#Declaração da classe ClienteService
class ClienteService(BaseService):

    #Método para cadastrar clientes
    def cadastrar(self, data: SchemaClienteCadastro):

        cpf_normalizado = Cliente.normalizar_cpf(data.cpf)

        cliente_existente = self.session.query(Cliente).filter_by(
            cpf=cpf_normalizado
        ).first()

        if cliente_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um cliente com esse CPF"
            )

        try:
            cliente_cadastrar = Cliente(
                cpf=cpf_normalizado,
                nome=data.nome,
                bairro=data.bairro,
                rua=data.rua,
                numero=data.numero,
                complemento=data.complemento,
                telefone=data.telefone
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=422,
                detail=str(erro)
            )

        try:
            self.salvar(cliente_cadastrar)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Já existe um cliente com esse CPF"
            )

        self.session.refresh(cliente_cadastrar)
        return cliente_cadastrar

    #Método auxiliar para buscar um cliente pelo id, lançando 404 caso não exista
    def _buscar_por_id(self, cliente_id: int) -> Cliente:
        cliente = self.session.get(Cliente, cliente_id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

        return cliente

    #Método para visualizar clientes
    def visualizar(self):
        return self.session.query(Cliente).all()

    #Método para atualizar clientes
    def atualizar(self, cliente_id: int, data: SchemaClienteAtualizacao):
        cliente_atualizar = self._buscar_por_id(cliente_id)

        try:
            cliente_atualizar.atualizar_cliente(
                nome=data.nome,
                bairro=data.bairro,
                rua=data.rua,
                numero=data.numero,
                complemento=data.complemento,
                telefone=data.telefone
            )

            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(cliente_atualizar)
        return cliente_atualizar

    #Método para inativar clientes
    def inativar(self, cliente_id: int):
        cliente_inativar = self._buscar_por_id(cliente_id)

        try:
            cliente_inativar.inativar_cliente()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(cliente_inativar)
        return cliente_inativar

    #Método para ativar clientes
    def ativar(self, cliente_id: int):
        cliente_ativar = self._buscar_por_id(cliente_id)

        try:
            cliente_ativar.ativar_cliente()
            self.session.commit()

        except ValueError as erro:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(erro)
            )

        self.session.refresh(cliente_ativar)
        return cliente_ativar
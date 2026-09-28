from enum import Enum

#Criação do Enum para os estados dos Materiais
class StatusMaterial(Enum):
    DISPONIVEL = "DISPONIVEL"
    EMPRESTADO = "EMPRESTADO"
    RESERVADO = "RESERVADO"

#Criação do Enum para os estados dos Empréstimos
class StatusEmprestimo(Enum):
    ABERTO = "ABERTO"
    DEVOLVIDO = "DEVOLVIDO"
    ATRASADO =  "ATRASADO"
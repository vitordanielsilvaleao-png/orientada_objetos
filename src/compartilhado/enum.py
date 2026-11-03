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

#Criação do Enum para os estados das Reservas
class StatusReserva(Enum):
    ABERTA = "ABERTA"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"
    EXPIRADA = "EXPIRADA"

# Missão 10: Tratamento de Exceções e Validações em POO

## 1. Visão Geral
Esta missão aborda a implementação robusta de tratamento de exceções e validações de regras de negócio em um ambiente orientado a objetos. O objetivo é garantir que falhas esperadas ou inesperadas sejam capturadas, tratadas e comunicadas de forma clara, evitando que o sistema quebre abruptamente ou corrompa dados.

## 2. Objetivos Principais
* **Exceções Personalizadas (Custom Exceptions):** Criar classes de erro específicas para o domínio da aplicação (ex: `EntidadeNaoEncontradaException`, `RegraNegocioException`, `ValorInvalidoException`).
* **Validação de Camada de Serviço:** Garantir que dados inconsistentes ou violações de regras de negócio sejam bloqueados antes de atingirem a camada de persistência (banco de dados).
* **Mensagens Claras:** Retornar mensagens descritivas para facilitar a depuração e melhorar a experiência de uso ou integração.

## 3. Estrutura e Exemplos de Implementação

### 3.1. Exceção Base de Domínio
Geralmente, criamos uma exceção genérica da qual todas as regras de negócio específicas herdam:

```python
class DominioException(Exception):
    """Exceção base para erros relacionados às regras de negócio."""
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem

class RegistroNaoEncontradoException(DominioException):
    """Lançada quando um registro buscado não existe no sistema."""
    pass

class OperacaoInvalidaException(DominioException):
    """Lançada quando uma transação viola o estado atual do objeto."""
    pass
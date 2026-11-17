# Missão 10: Tratamento de Exceções e Validações

## 1. Visão Geral
Esta missão documenta a arquitetura de tratamento de exceções, validações de domínio e tradução de erros implementada no sistema. O objetivo é garantir que falhas nas regras de negócio, erros de validação de dados e exceções HTTP sejam tratados de forma centralizada e retornem mensagens claras e amigáveis ao usuário.

## 2. Componentes de Tratamento de Erros Implementados

### 2.1. Validações nas Entidades (`ValueError`)
As entidades do domínio utilizam exceções nativas do tipo `ValueError` para proteger o estado interno dos objetos. Sempre que ocorre uma tentativa de violação de regra de negócio ou transição de status inválida na construção ou manipulação da entidade, um `ValueError` é lançado.

### 2.2. Exceções HTTP nos Services (`HTTPException`)
A camada de serviços (`services`) utiliza o `HTTPException` do FastAPI para sinalizar erros de infraestrutura ou de negócio com os códigos de status HTTP adequados:
* **Status 404 (Not Found):** Utilizado quando um registro ou recurso buscado não é encontrado na base de dados.
* **Status 409 (Conflict):** Utilizado para conflitos de regras de negócio (ex: duplicidade de registros ou operações inválidas para o estado atual).

### 2.3. Exception Handlers Centrais (`src/main.py`)
No arquivo `src/main.py` (linhas 103 a 141), foram configurados manipuladores globais para capturar e formatar as respostas de erro da aplicação:
1. **`ValueError`:** Captura os erros gerados pelas validações das entidades e retorna uma resposta padronizada.
2. **`RequestValidationError`:** Captura erros de validação de schema do Pydantic (dados de entrada inválidos) e aciona o tradutor.
3. **`HTTPException`:** Padroniza o retorno das exceções HTTP lançadas pelos services.
4. **`Exception` (Genérica):** Captura qualquer erro inesperado do servidor para evitar vazamento de stack traces e retornar um erro 500 controlado.

### 2.4. Tradutor de Validação (`TradutorValidacao`)
Componente responsável por interceptar e traduzir os erros de validação padrão do FastAPI/Pydantic (código 422 - Unprocessable Entity), convertendo as mensagens técnicas de erro para o português de forma compreensível.

## 3. Decisões Técnicas
* Utilização de exceções nativas e do FastAPI (`ValueError` e `HTTPException`) em vez de criar uma hierarquia complexa de classes de exceção personalizadas que não eram utilizadas pelo sistema.
* Centralização dos tratamentos de erro no `main.py` para manter os controllers e services limpos e focados nas regras de negócio.

## 4. Dificuldades Encontradas
* Alinhar a documentação inicial genérica com a estrutura real de exception handlers já existente no `main.py` e nas entidades do repositório.

## 5. Reflexão
O tratamento centralizado de exceções garante consistência nas APIs, facilitando a integração com o front-end e melhorando a manutenibilidade do código ao separar erros de negócio de erros técnicos.

## 6. Commits
* `docs: adiciona documentacao da missao 10` — Documentação da arquitetura de tratamento de exceções (`ValueError`, `HTTPException`), manipuladores globais no `src/main.py` e tradução de erros 422 via `TradutorValidacao`.
# Sistema de Gestão de Biblioteca

Sistema web desenvolvido para auxiliar bibliotecas no gerenciamento e organização de seu acervo, além do controle de empréstimos, reservas, devoluções e visualização de relatórios.

## 📚 Sobre o projeto

O projeto busca solucionar problemas relacionados ao gerenciamento e à organização manual do acervo de livros, facilitando também o controle das principais operações bibliotecárias.

O sistema tem como público-alvo bibliotecas que enfrentam dificuldades no gerenciamento e organização de seu acervo e necessitam de uma solução informatizada.

Inicialmente, o sistema será utilizado por **bibliotecários**. Outros perfis, como administradores e leitores, poderão ser incorporados futuramente conforme a evolução do projeto.

## 🎯 Objetivo

Oferecer uma solução prática e abrangente para o gerenciamento das principais rotinas bibliotecárias, contemplando:

- Controle e catalogação do acervo de livros e revistas;
- Gerenciamento de empréstimos;
- Gerenciamento de reservas;
- Registro de devoluções;
- Acompanhamento de pendências;
- Visualização de relatórios e métricas.

Funcionalidades adicionais poderão ser incorporadas conforme a disponibilidade de tempo e a evolução do projeto.

## 🚀 MVP

O MVP (Minimum Viable Product) contempla as funcionalidades essenciais para o funcionamento inicial do sistema.

### 📖 Gerenciamento do acervo

- Cadastro de materiais;
- Edição de materiais;
- Inativação de materiais;
- Consulta do catálogo;
- Gerenciamento de categorias;
- Gerenciamento de autores;
- Gerenciamento de editoras.

Inicialmente, os materiais contemplados serão **livros e revistas**.

### 📘 Módulo de Livros

- Cadastro de livros;
- Edição de livros;
- Inativação de livros;
- Consulta de livros.

### 📕 Módulo de Revistas

- Cadastro de revistas;
- Edição de revistas;
- Inativação de revistas;
- Consulta de revistas.

### 📦 Disponibilidade

- Consulta da quantidade de materiais disponíveis no acervo;
- Acompanhamento da disponibilidade dos materiais cadastrados.

### 🔄 Empréstimos, reservas e devoluções

- Realização de empréstimos;
- Registro de devoluções;
- Consulta de empréstimos;
- Reserva de materiais do acervo;
- Cancelamento de reservas;
- Consulta de reservas;
- Consulta de pendências de devolução;
- Consulta de devoluções em atraso.

### 📊 Relatórios

O MVP contará inicialmente com três relatórios:

- Materiais mais emprestados;
- Empréstimos em aberto;
- Devoluções atrasadas.

### 👤 Cadastro de Clientes
- Cadastro, consulta, atualização e ativação/inativação de clientes.

## 🛠️ Tecnologias

| Camada | Tecnologias |
|---|---|
| Back-end | Python 3, FastAPI, Uvicorn, Pydantic |
| Persistência | MySQL, SQLAlchemy (ORM), PyMySQL, Alembic (migrações) |
| Tarefas automáticas | APScheduler |
| Front-end | HTML5, CSS3 e JavaScript puro (`fetch`), Google Fonts e Font Awesome |
| Testes | `unittest` |

## 🧪 Como executar os testes

Para executar os testes automatizados do projeto, utilize o comando:

```bash
python -m unittest
```

## ⚙️ Como executar a API

1. Crie e ative um ambiente virtual na raiz do projeto.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Com o MySQL em execução na porta `3306`, crie o banco de dados:

```sql
CREATE DATABASE biblioteca;
```

A conexão usa o usuário `root` com a senha `123456` em `localhost:3306`. Esses dados estão definidos em `src/database/database.py` (usado pela API) e na chave `sqlalchemy.url` do `alembic.ini` (usado pelas migrações). Se o seu MySQL usar outro usuário ou senha, altere os dois arquivos.

4. Execute as migrações para preparar o banco de dados:

```bash
alembic upgrade head
```

5. Inicie a API:

```bash
python -m uvicorn src.main:app --reload
```

Por padrão, a API ficará disponível em `http://localhost:8000`.

## 💻 Como abrir o frontend

1. API e frontend devem ser executados em terminais separados, mantendo os dois servidores ativos. Na raiz do projeto, inicie um servidor estático apontando para a pasta `src/frontend`:

```bash
python -m http.server 5500 --directory src/frontend
```

2. Acesse `http://localhost:5500` no navegador.

## 🔮 Funcionalidades futuras

As funcionalidades abaixo poderão ser incorporadas conforme a disponibilidade de tempo e a evolução do projeto:

- Consulta de multas por atraso pagas e pendentes;
- Área do leitor;
- Reservas realizadas pelo leitor;
- Consulta de datas de empréstimo e devolução pelo leitor;
- Consulta de multas pelo leitor.

## 🚫 O que o sistema não fará

O sistema não terá como objetivo:

- Realizar a compra de livros;
- Integrar-se com fornecedores;
- Realizar o controle financeiro da biblioteca;
- Integrar-se com sistemas governamentais.

## 💡 Diferencial

O diferencial do projeto é oferecer um sistema abrangente, porém de fácil utilização e intuitivo.

A proposta é proporcionar um controle consistente do acervo, aliado à visualização de métricas que auxiliem no acompanhamento das operações da biblioteca.

## 🚀 Missões

O projeto incorpora as 16 missões propostas para o desenvolvimento orientado a objetos. A documentação de cada uma, com o que foi implementado e onde está no código, fica em `docs/missao/`:

- **Missão 01** — Do Mundo Real ao Objeto
- **Missão 02** — Classes, Objetos e Atributos
- **Missão 03** — Métodos e Construtores
- **Missão 04** — Estáticos e Sobrecarga
- **Missão 05** — Regras de Negócio
- **Missão 06** — Repetição e Relatórios
- **Missão 07** — Encapsulamento
- **Missão 08** — Herança e Sobreposição
- **Missão 09** — Polimorfismo
- **Missão 10** — Exceções e Asserções
- **Missão 11** — Classes Abstratas
- **Missão 12** — Interfaces
- **Missão 13** — Arrays e Strings
- **Missão 14** — Coleções e Listas
- **Missão 15** — Arquivos e Persistência
- **Missão 16** — Integração Final

A documentação complementar está em `docs/`: regras de negócio e requisitos (versões 1.0 e 2.0), diagrama de classes e diagrama do banco de dados.

## 📌 Status do projeto

✅ **Versão 1.0 concluída**

As funcionalidades previstas para o MVP estão implementadas na API e no front-end. As alterações de cada versão estão registradas no `CHANGELOG.md`, e as funcionalidades futuras listadas acima poderão ser incorporadas em versões posteriores.

## 👥 Público-alvo

Bibliotecas que necessitam de uma solução informatizada para auxiliar no gerenciamento e na organização de seu acervo e de suas principais operações.

## 👨‍💻 Integrantes

| Integrante | GitHub |
|---|---|
| Ana Gabriela de Faria | [@AnaGFaria](https://github.com/AnaGFaria) |
| Gustavo Souza | [@gustavosouzags](https://github.com/gustavosouzags) |
| Heitor | [@heitorteixeira0203-cyber](https://github.com/heitorteixeira0203-cyber) |
| Henrique Prado | [@Henrique-Single](https://github.com/Henrique-Single) |
| henoli077 | [@henoli077](https://github.com/henoli077) |
| Vitor Daniel | [@vitordanielsilvaleao-png](https://github.com/vitordanielsilvaleao-png) |

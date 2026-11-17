# Changelog

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

O formato segue uma organização baseada em versões e etapas de desenvolvimento do projeto.

---

## [Unreleased]

---

## [1.0.0] - 2026-11-17

Primeira versão completa do Apolo: API, front-end e documentação das 16 missões.

### Estrutura do projeto

- Estrutura inicial do projeto organizada em `src`, `tests` e `docs`.
- Estrutura de documentação das 16 missões criada.
- Estrutura de documentação das regras de negócio criada.
- Estrutura de documentação dos requisitos funcionais e não funcionais criada.
- Ambiente virtual Python configurado para o projeto.
- Arquivo `requirements.txt` criado para gerenciamento das dependências.
- Arquivo `alembic.ini` configurado para gerenciamento das migrações do banco de dados.

### Documentação

- README principal criado com:
  - descrição do projeto;
  - objetivo;
  - público-alvo;
  - funcionalidades do MVP;
  - funcionalidades futuras;
  - escopo de atuação;
  - diferencial do sistema;
  - 16 missões de desenvolvimento orientado a objetos.
- Documentação das regras de negócio organizada em:
  - Controle de acervo;
  - Disponibilidade;
  - Empréstimos;
  - Reservas;
  - Devoluções;
  - Relatórios.
- Documentação dos requisitos organizada em:
  - Requisitos funcionais;
  - Requisitos não funcionais.
- Estrutura de documentação das 16 missões criada, da Missão 01 à Missão 16.

### Banco de dados e persistência

- Estrutura inicial de conexão com o banco criada em `src/database`.
- Configuração inicial do Alembic para controle de migrações.
- Estrutura de versões de migração criada.
- Migrações iniciais relacionadas às entidades do sistema adicionadas para:
  - Cliente;
  - Material;
  - Categoria;
  - Editora;
  - Livro;
  - Autor;
  - Revista;
  - Empréstimo;
  - Reserva.
- Estrutura de migrações preparada para evolução incremental do modelo de dados.

### Estrutura de módulos

- Módulo `cliente` criado.
- Módulo `emprestimo` criado.
- Módulo `livro` criado.
- Módulo `material` criado.
- Módulo `reserva` criado.
- Módulo `revista` criado.

### Entidades

- Estrutura inicial da entidade `Cliente` criada.
- Estrutura inicial da entidade `Empréstimo` criada.
- Estrutura inicial da entidade `Reserva` criada.
- Estrutura inicial da entidade `Material` criada.
- Estrutura inicial da entidade `Livro` criada.
- Estrutura inicial da entidade `Revista` criada.
- Estrutura inicial da entidade `Autor` criada.
- Estrutura inicial da entidade `Categoria` criada.
- Estrutura inicial da entidade `Editora` criada.

### Organização interna dos módulos

- Entidades relacionadas a livros organizadas em `src/modulos/livro/entidades`.
- Entidades relacionadas a materiais organizadas em `src/modulos/material/entidades`.
- Arquivos `__init__.py` adicionados aos pacotes Python necessários.

### Testes

- Estrutura inicial do diretório `tests` criada.
- Teste automatizado de validação da estrutura básica do projeto criado.
- Teste de importação dos pacotes `src` e `tests` implementado.
- Primeiro teste automatizado executado com sucesso utilizando `unittest`.

### Desenvolvimento orientado a objetos

- Estrutura inicial das entidades do domínio criada.
- Estrutura preparada para evolução das classes conforme a implementação das 16 missões.
- Estrutura preparada para utilização de herança entre `Material`, `Livro` e `Revista`.
- Estrutura preparada para utilização de polimorfismo através do ORM SQLAlchemy.

### API e regras de negócio

- API em FastAPI com routers para `livro`, `revista`, `autor`, `categoria`, `editora`, `material`, `cliente`, `reserva` e `emprestimo`, registrados em `src/main.py`.
- Services com as regras de cadastro, empréstimo, devolução e reserva, incluindo a fila de reservas atendida na devolução.
- Rotas de relatório em `/material` (totais, disponíveis, emprestados, quantidade por tipo e por categoria).
- Scheduler (APScheduler) que marca empréstimos atrasados e reservas expiradas ao iniciar a API e a cada 60 minutos.
- Testes unitários das entidades e testes de integração dos services, executados com `python -m unittest`.

### Padronização dos módulos

- Padronização dos módulos `Material`, `Autor`, `Cliente`, `Reserva`, `Livro`, `Revista` e `Empréstimo`, além dos componentes compartilhados.
- Reorganização das entidades, dependências, routers, schemas, services e testes, conforme a estrutura de cada módulo.
- Implementação da `BaseService` para centralizar operações e comportamentos comuns dos serviços.
- Implementação de handlers de erro no `main.py` para padronizar o tratamento de exceções da API.
- Implementação do `TradutorValidacao` para apresentar mensagens de erro HTTP 422 em português.
- Aplicação de validações e normalização de dados nas entidades do sistema.
- Encapsulamento dos atributos `_status` e `_is_active`, com controle de alterações por meio dos métodos das entidades.

### Atualizações do banco de dados

- Adicionada a migração `98ea26be709f` para inclusão do campo `status` na tabela `reserva`.
- Definido o status inicial `ABERTA` para reservas existentes ativas e `CANCELADA` para reservas existentes inativas.
- Adicionada a migração `eb118a43784a` para definir `id` como única chave primária de `revista`, mantendo `issn` como campo único.
- Adicionada a migração `dbf83686c72c` para definir `id` como única chave primária de `livro`, mantendo `isbn` como campo único.
- Implementação do enum `StatusReserva`, com os estados `ABERTA`, `ATENDIDA`, `CANCELADA` e `EXPIRADA`.
- Atualização da entidade `Reserva` para utilizar o campo `status`, permitindo controlar o ciclo de vida das reservas.

### Frontend

- Novo front-end em HTML, CSS e JavaScript puro em `src/frontend`, substituindo a primeira versão (classes JavaScript e modo de demonstração).
- Página única com menu lateral; cada tela é uma `<section>` exibida conforme o `#` do endereço (`navegacao.js`).
- Um arquivo JavaScript por tela: painel, livros, revistas, empréstimos, reservas, relatórios, clientes e catálogo (autores, editoras e categorias).
- Comunicação com a API pela função `chamarApi()` (`fetch`), em `js/geral.js`, com mensagens de erro lidas do formato padronizado pelos handlers.
- Linhas das tabelas geradas a partir de `<template>` e validação dos formulários com as mesmas regras do back-end.
- Tela de relatórios com totais do acervo, ranking dos mais emprestados, devoluções em atraso e gráficos por tipo e por categoria.
- Painel "Conceitos de POO" e balões de ajuda ligando cada tela às classes do back-end.
- README do front-end em `src/frontend/README.md`, com execução, arquitetura e rotas usadas por tela.

### Evolução da documentação

- Documentação das missões 01 a 16 em `docs/missao/`.
- Diagrama de classes do sistema em `docs/classes/diagrama/`.
- Diagrama do banco de dados atualizado em `docs/database/diagrama/`.
- Regras de negócio atualizadas para a versão 2.0.
- Requisitos funcionais atualizados para a versão 2.0.
- README principal com instruções de execução da API, dos testes e do front-end.

---

## [0.1.0] - Estrutura inicial

### Adicionado

- Estrutura inicial do repositório.
- `.gitignore`.
- `README.md`.
- `CHANGELOG.md`.
- Diretório `docs`.
- Diretório `src`.
- Diretório `tests`.
- Estrutura inicial das 16 missões.
- Estrutura inicial dos requisitos.
- Estrutura inicial das regras de negócio.
- Pacotes Python iniciais.
- Primeiro teste automatizado de estrutura.
- Ambiente virtual Python.
- Configuração inicial do Alembic.

### Git

- Repositório Git inicializado.
- Branch principal `main` criada.
- Primeiro commit funcional realizado.
- Repositório remoto configurado no GitHub.
- Autenticação SSH configurada para acesso ao GitHub.
- Branch `main` publicada no repositório remoto.

### Primeiro commit

`chore: cria estrutura inicial do projeto`

---

## Convenção

As alterações deverão ser classificadas conforme sua natureza:

- `Added` — novas funcionalidades ou componentes.
- `Changed` — alterações em funcionalidades existentes.
- `Deprecated` — funcionalidades que serão removidas futuramente.
- `Removed` — funcionalidades removidas.
- `Fixed` — correções de problemas.
- `Security` — correções relacionadas à segurança.

As alterações deverão ser registradas de forma incremental durante o desenvolvimento do projeto.


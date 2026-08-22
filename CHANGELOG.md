# Changelog

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

O formato segue uma organização baseada em versões e etapas de desenvolvimento do projeto.

---

## [Unreleased]

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
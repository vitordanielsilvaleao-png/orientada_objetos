# Missão 15 — Arquivos e Persistência

## Objetivo e planejamento

O objetivo desta missão foi implementar a persistência dos dados do sistema, permitindo que as informações utilizadas pela aplicação sejam armazenadas de forma permanente e possam ser recuperadas posteriormente.

Para isso, foi planejada a utilização de um banco de dados relacional MySQL, integrado à aplicação Python por meio do SQLAlchemy com ORM.

Também foi adotado o Alembic para controle e versionamento das alterações realizadas na estrutura do banco de dados.

---

## O que foi implementado e por quê

Foi implementada a estrutura inicial de persistência do projeto, utilizando o SQLAlchemy como camada de mapeamento objeto-relacional entre as classes Python e as tabelas do banco de dados.

As principais entidades do sistema foram estruturadas como entidades ORM, permitindo que seus atributos sejam associados às respectivas colunas do banco de dados.

Entre as entidades inicialmente estruturadas estão:

- Material;
- Livro;
- Revista;
- Autor;
- Editora;
- Categoria;
- Cliente;
- Empréstimo;
- Reserva.

Também foi criada a estrutura de conexão com o banco de dados em:

**src/database/**

O controle das alterações estruturais do banco foi implementado utilizando o Alembic, com as configurações principais em:

**alembic.ini**

E as migrações organizadas em:

**src/migrations/**

As migrações permitem registrar de forma incremental as alterações realizadas no modelo do banco de dados durante a evolução do projeto.

---

## Decisões técnicas e trade-offs

A principal decisão técnica desta etapa foi utilizar o SQLAlchemy com ORM para realizar o mapeamento entre as classes Python e as tabelas do banco de dados.

Essa abordagem foi escolhida porque permite representar as entidades do domínio por meio de classes Python e, ao mesmo tempo, persistir seus dados no banco relacional.

Também foi adotado o Alembic para versionamento das alterações do banco de dados.

A utilização de uma ferramenta de migração permite que a estrutura do banco acompanhe a evolução das entidades do sistema sem depender exclusivamente de alterações manuais no banco de dados.

---

## Dificuldades encontradas e soluções

Uma das principais dificuldades encontradas foi estabelecer a correspondência entre as entidades identificadas durante a modelagem do domínio e sua representação como entidades persistentes no banco de dados.

Também foi necessário definir como representar a especialização entre Material, Livro e Revista utilizando o SQLAlchemy.

A solução adotada foi utilizar o mapeamento de herança do SQLAlchemy, permitindo que Livro e Revista sejam especializações de Material e que suas informações específicas sejam armazenadas em suas respectivas estruturas.

---

## Reflexão sobre o conceito aprendido

A implementação da persistência permitiu compreender a diferença entre manter informações apenas durante a execução de um programa e armazená-las de forma permanente.

Também foi possível compreender na prática a relação entre o modelo orientado a objetos utilizado pela aplicação e o modelo relacional utilizado pelo banco de dados.

A utilização do SQLAlchemy demonstrou como uma classe Python pode ser mapeada para uma estrutura persistente, reduzindo a necessidade de realizar manualmente todas as operações de conversão entre objetos e registros do banco.

---

## Commit(s) associado(s)

chore: Criação e configuração da Base de Dados e Entidades (daf8636ab24248cd496f6fcb93d29e336b7e6f2a)
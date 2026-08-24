# Missão 02 — Classes, Objetos e Atributos

## Objetivo e planejamento

O objetivo desta missão foi transformar as abstrações identificadas durante a Missão 01 em classes e entidades que pudessem ser utilizadas na implementação do sistema de gestão de biblioteca.

A partir do domínio previamente definido, foram planejadas classes responsáveis por representar os principais elementos do sistema, considerando seus atributos e relacionamentos.

O planejamento também considerou a utilização do SQLAlchemy com ORM, permitindo que as classes Python fossem utilizadas como representação das entidades persistidas no banco de dados.

---

## O que foi implementado e por quê

Foram implementadas as classes responsáveis por representar as principais entidades do sistema.

### Material

A classe **Material** representa a entidade base dos materiais pertencentes ao acervo da biblioteca.

Entre seus principais atributos estão:

- id;
- titulo;
- ano_publi;
- categoria_id;
- editora_id;
- tipo;
- status;
- is_active.

A classe foi definida como entidade base porque livros e revistas possuem diversas características em comum.

### Livro

A classe **Livro** representa os materiais do tipo livro.

Além dos atributos herdados de **Material**, foram definidos atributos específicos:

- isbn;
- autor_id.

### Revista

A classe **Revista** representa os materiais do tipo revista.

Além dos atributos herdados de **Material**, foram definidos:

- issn;
- edicao.

### Autor

A classe **Autor** representa os autores associados aos livros cadastrados no sistema.

### Editora

A classe **Editora** representa as editoras associadas aos materiais do acervo.

### Categoria

A classe **Categoria** representa as categorias utilizadas para organização dos materiais.

### Cliente

A classe **Cliente** representa as pessoas relacionadas às operações de empréstimo e reserva realizadas no sistema.

No MVP, essa entidade não representa um usuário com acesso ao sistema, mas sim a pessoa vinculada às movimentações da biblioteca.

### Empréstimo

A classe **Emprestimo** representa o registro de empréstimo de um material para um cliente.

### Reserva

A classe **Reserva** representa o registro de uma reserva de material realizada para um cliente.

A implementação dessas classes foi necessária para transformar o modelo conceitual definido anteriormente em estruturas concretas de programação orientada a objetos.

---

## Decisões técnicas e trade-offs

Uma das principais decisões técnicas desta missão foi a utilização do SQLAlchemy com ORM.

Em vez de criar classes independentes do banco de dados e posteriormente realizar manualmente o mapeamento entre objetos e tabelas, optou-se por utilizar as classes Python como entidades mapeadas pelo SQLAlchemy.

Dessa forma, os atributos das classes também representam as colunas correspondentes no banco de dados.

Por exemplo, a entidade **Material** possui atributos como **titulo**, **ano_publi**, **status** e **is_active**, que são definidos utilizando os recursos de mapeamento do SQLAlchemy.

Outro ponto importante foi a utilização de herança entre as classes Material, Livro e Revista.

A estrutura adotada foi:

```text
Material
├── Livro
└── Revista
```
Essa decisão permite centralizar os atributos comuns em **Material** e manter nas classes especializadas apenas os atributos específicos de cada tipo de material.

Também foi utilizado o campo tipo em **Material** para permitir a identificação do tipo especializado pelo SQLAlchemy, utilizando os recursos de mapeamento polimórfico da biblioteca.

---

## Dificuldades encontradas e soluções

Uma das principais dificuldades encontradas foi definir quais informações deveriam pertencer à entidade geral **Material** e quais deveriam ser específicas de **Livro** e **Revista**.

A solução adotada foi separar as características comuns das características específicas.

Dessa forma, informações como título, ano de publicação, categoria, editora, status e situação de atividade foram associadas à entidade **Material**.

Já informações específicas foram atribuídas às classes especializadas:

* **Livro**: ISBN e autor;
* **Revista**: ISSN e edição.

Outra dificuldade foi definir como representar essa especialização no banco de dados utilizando SQLAlchemy.

Para solucionar essa questão, foi utilizada a herança entre as classes e o mapeamento polimórfico do SQLAlchemy, permitindo que **Livro** e **Revista** fossem representados como especializações de Material.

---

## Reflexão sobre o conceito aprendido

A Missão 02 permitiu compreender de forma prática a diferença entre identificar uma entidade durante a análise de um problema e efetivamente representá-la por meio de uma classe.

Na Missão 01, os elementos do domínio foram identificados de forma conceitual. Nesta etapa, esses elementos passaram a possuir uma representação concreta dentro do código.

Também foi possível compreender que uma classe não precisa representar apenas uma tabela de forma isolada. No projeto, a utilização do SQLAlchemy permite que as classes Python representem entidades persistidas no banco de dados, mantendo seus atributos relacionados às respectivas colunas.

---

## Commit(s) associado(s)

chore: Criação e configuração da Base de Dados e Entidades (daf8636ab24248cd496f6fcb93d29e336b7e6f2a)

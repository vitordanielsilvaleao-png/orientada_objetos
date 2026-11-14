# Missão 12 — Interfaces

## Objetivo e planejamento

O objetivo desta missão foi compreender e aplicar o conceito de interfaces por meio da definição de contratos que estabelecem como diferentes partes do sistema devem se comportar e trocar informações.

Este conceito pode ser observado em dois pontos principais: na classe `BaseService`, que define um contrato comum para os serviços da aplicação, e nos schemas Pydantic, que estabelecem os formatos e as validações dos dados utilizados pela API.

## O que foi implementado e por quê

Foram utilizados dois mecanismos para estabelecer contratos no sistema.

O primeiro está na classe `BaseService`, localizada em:

**src/compartilhado/base_service.py**

Ela define uma estrutura comum para os services, estabelecendo os métodos `cadastrar(self, data)` e `visualizar(self)` como operações que devem ser implementadas pelas classes que herdam dela.

Assim, os serviços seguem uma interface comum, mesmo que cada um tenha suas próprias regras de negócio e trabalhe com entidades diferentes.

O segundo mecanismo está nos schemas Pydantic, utilizados para definir os formatos dos dados recebidos e retornados pela API.

Esses schemas são organizados por módulo e possuem diferentes finalidades:

- **Schemas de cadastro:** definem os campos necessários para criar registros, como `SchemaClienteCadastro`, `SchemaLivroCadastro` e `SchemaReservaCadastro`.
- **Schemas de atualização:** definem os dados permitidos durante alterações, como `SchemaClienteAtualizacao`, `SchemaLivroAtualizacao` e `SchemaRevistaAtualizacao`.
- **Schemas de resposta:** definem a estrutura dos dados apresentados pela API, como `SchemaClienteResposta`, `SchemaLivroResposta` e `SchemaReservaResposta`.

Também existem schemas específicos para informações agregadas, como `SchemaQuantidadeMaterial`, `SchemaQuantidadePorCategoria` e `SchemaQuantidadePorTipo`, utilizados para representar quantidades de materiais.

Os schemas utilizam `BaseModel` do Pydantic e, quando necessário, `Field` para estabelecer restrições nos atributos. Entre as validações implementadas estão:

- Comprimento mínimo e máximo de textos, por meio de `min_length` e `max_length`;
- Limites numéricos, por meio de `gt` e `le`;
- Valores opcionais, utilizando tipos como `str | None` e valores padrão com `default=None`;
- Tipos específicos para datas, identificadores e status.

Nos schemas de resposta que utilizam `ConfigDict(from_attributes=True)`, o Pydantic pode construir os objetos de resposta a partir dos atributos das entidades, facilitando a conversão dos dados retornados pelo ORM.

## Decisões técnicas e trade-offs

A utilização do `BaseService` permite estabelecer um padrão de comportamento para os serviços sem exigir que todos implementem suas regras internas da mesma maneira.

Já a utilização do Pydantic permite separar a estrutura dos dados utilizados pela API da implementação das entidades e das regras de negócio.

Também foi importante separar os schemas de cadastro, atualização e resposta. Essa divisão permite que cada operação tenha um contrato adequado à sua finalidade.

Um exemplo dessa decisão aparece em `SchemaClienteAtualizacao`: o CPF não foi incluído entre os campos disponíveis para atualização, evitando que esse identificador seja alterado por essa operação.

Outro exemplo está em `SchemaRevistaAtualizacao`, no qual o ISSN também não é disponibilizado para alteração, pois identifica a publicação.

A utilização de campos opcionais nos schemas de atualização permite representar atributos que podem não ser enviados em uma operação, enquanto os limites definidos em `Field` ajudam a restringir os valores aceitos.

## Dificuldades encontradas e soluções

Uma das dificuldades foi compreender que o conceito de interface não precisa estar representado exclusivamente por uma palavra-chave específica da linguagem.

No Python, o contrato pode ser estabelecido por meio de uma classe base que define operações esperadas, como acontece com o `BaseService`.

Outra dificuldade foi definir quais informações deveriam ser aceitas em cada operação da API. A separação entre schemas de cadastro, atualização e resposta ajudou a resolver esse problema, deixando explícito quais dados são esperados e quais informações podem ser retornadas.

Também foi necessário definir validações adequadas para os diferentes tipos de atributos, utilizando os recursos do Pydantic para restringir valores e evitar dados incompatíveis com o formato esperado.

## Reflexão sobre o conceito aprendido

A implementação permitiu compreender que interfaces e contratos são importantes para estabelecer padrões de comunicação entre diferentes partes de um sistema.

O `BaseService` demonstra como diferentes classes podem compartilhar um conjunto de operações esperadas, enquanto os schemas Pydantic demonstram como estabelecer contratos para os dados que entram e saem da API.

Com isso, foi possível perceber que contratos bem definidos facilitam a organização do código, reduzem ambiguidades e tornam a integração entre componentes mais previsível.

## Commit(s) associado(s)

feat: Mapeamento da API da classe ClienteRouter e criação da classe ClinteService (13f20e24a138914946d028da447dfba84ab70107)

refact: adiciona cpf obrigatorio no schema de cadastro de cliente (22bb8640db0c8f864595b1d04f1e59ac176563c9)

feat: Mapeamento da API da classe EmprestimoRouter e criação da classe EmprestimoService (630c4e9b96d1473b871f1ff24dbcacbddb2f6acf)

refactor: Exclusão da classe SchemaDevolucaoEmprestimo e criação da classe SchemaEmprestimoResposta (8d740b46bd4c31d64e13aab714a411952db70a32)

feat: Mapeamento das rotas de API de Livros (1e70670adee32e83c4fe009c14def3f4784d5d91)

feat: Atualização do mapeamento de API de Livro (b9901c36f76d75db7e7d8f0bb27d9adaea005517)

refactor: retirada do campo isbn da classe SchemaLivroAtualizacao (a6451c4238ddda68aa2cd04fc124bbf33a93a560)

Mapeamento da API da classe RevistaRouter e criação da classe RevistaService (54dafb1c6dcbeb3b37a82f2b90b885f91c82f755)

feat: Adiciona as classes SchemaCategoriaCadastro e SchemaCategoriaAtualizacao (f8f339d79b5de1bca3a5f5889b0ae5898a2aa681)

feat: Adiciona a classe CategoriaService com atributos e métodos e seus respectivos testes (fb7be173441364290493a0ff3215ca3397666ec3)

feat: Mapeamento da API da classe ReservaRouter e criação da classe ReservaService (14c6d760afc4c437911557502ddeeafc8d40c7a2)

refactor: retira o campo material_id:int da classe SchemaReservaCadastro (aa04b5ee5f50bc2937b75d79274aedc00bfd5b5c)

refactor: Estabelece o método SchemaAutorCadastro como o meio padrão para armazenamento do nome do autor que será cadastrado (33e7235c16039fb4be06de2cdaedf739fcc226f7)

refactor: Estabelece o método SchemaEditoraCadastro como padrão para criação de novas editoras (0aa635c00da1ab85b1d6f5209b0b13d40bc7e1a5)


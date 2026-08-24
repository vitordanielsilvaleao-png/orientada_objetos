# Missão 01 — Do Mundo Real ao Objeto

## Objetivo e planejamento

A primeira missão teve como objetivo realizar a transição entre um problema existente no mundo real e sua representação por meio de abstrações utilizadas no desenvolvimento de software.

Neste projeto, o domínio escolhido foi o gerenciamento de bibliotecas. A partir da análise das necessidades e dos processos envolvidos em uma biblioteca, foram identificados os principais elementos que deverão ser representados pelo sistema.

O objetivo desta etapa foi compreender o problema antes da implementação, identificando entidades, responsabilidades, relacionamentos e regras presentes no domínio.

---

## O que foi implementado e por quê

Nessa missão foi feito o todo o planejamento relacionado ao domínio escolhido, como:

* Objetivos;
* MVP do projeto;
* Futuras funcionalidades;
* Funcionalidades fora do escopo do projeto;
* Diferencial;
* Público-Alvo;
* Identificação e modelagem visual das classes, atributos e métodos;
* Identificação e modelagem visual das entidades do Banco de Dados;

A implementação dessa missão, teve como objetivo definir o planejamento que irá guiar o processo de desenvolvimento de forma organizada e estruturada.

---

## Decisões técnicas e trade-offs

Durante esta etapa, algumas decisões foram tomadas para manter o projeto adequado ao escopo e ao tempo disponível para desenvolvimento.

* Classe/Entidade Material:

Inicialmente foi considerada uma estrutura separando material e exemplar:

Material
└── Livro
    └── Exemplar

Entretanto, essa estrutura adicionaria uma camada de complexidade ao sistema.

Foi decidido que o controle relacionado às unidades físicas do acervo será incorporado diretamente à entidade Material.

Dessa forma, diferentes registros de Material podem representar materiais com o mesmo título, enquanto cada registro possui sua própria identificação e informações de estado.

A decisão simplifica a implementação sem eliminar os controles necessários para o MVP.

* Usuários do sistema:

O gerenciamento de usuários e a diferenciação entre perfis de acesso não fazem parte do MVP.

Por isso, foi definido o conceito de Cliente para representar as pessoas relacionadas aos empréstimos e reservas, sem implementar inicialmente um sistema de autenticação e controle de usuários.

* Tipos de material:

O MVP contempla inicialmente dois tipos de material:

* Livro;
* Revista.

Outros tipos, como mídias digitais, poderão ser incorporados posteriormente conforme a disponibilidade de tempo e a evolução do projeto.

---

## Dificuldades encontradas e soluções

Uma das principais dificuldades encontradas durante a análise foi determinar o nível adequado de detalhamento para representar os materiais do acervo.

Inicialmente, foi considerada a separação entre material e exemplar. Após analisar o impacto dessa decisão sobre o restante do sistema, foi identificado que essa abordagem aumentaria a complexidade do MVP.

Como solução, optou-se por incorporar o controle das unidades do acervo diretamente na entidade Material.

Outra decisão importante foi determinar quais informações pertencem ao conceito geral de material e quais são específicas de cada tipo. A partir dessa análise, características comuns foram associadas a Material, enquanto informações específicas foram direcionadas para Livro e Revista.

---

## Reflexão sobre o conceito aprendido

A primeira missão permitiu compreender a importância de analisar o problema antes de iniciar a implementação efetiva do código.

A principal aprendizagem foi perceber que a orientação a objetos começa antes da criação das classes. É necessário compreender o domínio, identificar seus elementos e determinar quais conceitos precisam ser representados pelo software.

Também foi possível perceber que uma boa abstração não significa necessariamente representar todos os elementos existentes no mundo real. É necessário encontrar um nível de abstração adequado aos objetivos e às limitações do sistema.

---

## Commit(s) associado(s)

chore: cria estrutura inicial do projeto (d30ad0b30c83f6441d22fd728bd3ec770ccd75da)

docs: adiciona changelog inicial (7bc62216b08f28ded24c2439a16d1a10142c32f4)

test: adiciona teste inicial da estrutura (381c579b4fef2d29645727e521865a901611732d)

docs: adiciona a documentação de requisitos funcionais, requisitos não funcionais, regras de negócios e altera os arquivos readme.md e CHANGELOG.md (8b52979683b2deea2b27bf771bbeb245d314ce7a)


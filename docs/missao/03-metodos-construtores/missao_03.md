# Missão 03 — Métodos e Construtores

## Objetivo e planejamento

O objetivo desta missão foi aplicar os conceitos de métodos e construtores da Programação Orientada a Objetos na entidade Material, responsável por representar os materiais do acervo do sistema APOLO.

Foi planejada a utilização de um construtor para inicializar os atributos essenciais de cada material e de métodos para controlar suas informações, seu estado de ativação e sua disponibilidade.

A implementação está localizada em:

**src/modulos/material/entidades/material.py**

---

## O que foi implementado e por quê

Foi implementado o construtor `__init__`, responsável por inicializar os objetos da classe Material.

O construtor recebe quatro parâmetros:

- `titulo`: título do material;
- `ano_publi`: ano de publicação;
- `categoria_id`: identificação da categoria;
- `editora_id`: identificação da editora.

Durante a inicialização, o material recebe automaticamente o estado ativo (`_is_active = True`) e o status disponível (`_status = StatusMaterial.DISPONIVEL`).

Também foram implementados métodos para controlar o comportamento da entidade:

- `ativar()`: ativa um material que está inativo;
- `inativar()`: inativa um material que está ativo;
- `esta_disponivel()`: verifica se o material está ativo e disponível;
- `emprestar()`: altera o status do material para EMPRESTADO;
- `reservar()`: altera o status para RESERVADO;
- `disponibilizar()`: altera o status para DISPONIVEL;
- `atualizar()`: permite modificar informações de um material ativo.

Os métodos `ativar()` e `inativar()` também verificam se o material já se encontra no estado solicitado, lançando uma exceção `ValueError` quando a operação não é válida.

O método `atualizar()` impede alterações em materiais inativos e permite atualizar apenas os atributos informados.

A classe também utiliza validadores do SQLAlchemy para verificar e normalizar os dados de título e ano de publicação.

---

## Decisões técnicas e trade-offs

Uma das principais decisões técnicas foi concentrar os comportamentos relacionados ao estado do material dentro da própria entidade.

Essa abordagem permite que a classe Material represente não apenas os dados armazenados, mas também as operações relacionadas ao seu comportamento.

Outra decisão foi utilizar os atributos `_status` e `_is_active` com propriedades de leitura, permitindo consultar seus valores sem disponibilizar setters públicos.

O construtor foi definido para receber os dados essenciais do material e estabelecer valores iniciais para ativação e disponibilidade.

Os métodos de alteração de status foram mantidos simples, realizando diretamente a mudança do estado. Como consequência, as verificações das transições permitidas não estão implementadas nesses métodos e precisam ser consideradas nas regras de negócio das demais camadas da aplicação.

---

## Dificuldades encontradas e soluções

Um dos desafios desta etapa foi organizar a responsabilidade do construtor e dos métodos da classe, diferenciando a inicialização dos atributos das operações realizadas durante o funcionamento do sistema.

O construtor foi utilizado para estabelecer o estado inicial dos objetos, enquanto os métodos ficaram responsáveis pelas alterações posteriores.

Outro ponto importante foi o tratamento das operações de ativação e inativação, evitando que um material já ativo fosse ativado novamente ou que um material inativo fosse inativado pela segunda vez.

Para isso, foram utilizadas verificações condicionais e exceções `ValueError`.

---

## Reflexão sobre o conceito aprendido

Esta missão permitiu compreender como os construtores e métodos contribuem para a organização de um sistema orientado a objetos.

O construtor `__init__` estabelece os valores iniciais de um objeto no momento de sua criação, enquanto os métodos representam os comportamentos que esse objeto pode executar.

Na classe Material, esses conceitos foram aplicados para organizar o controle de ativação, atualização e disponibilidade dos materiais do acervo.

Também foi possível compreender a importância de manter os comportamentos relacionados a uma entidade próximos de seus atributos, facilitando a manutenção e a compreensão do código.

---

## Commit(s) associado(s)

- ef60b8e — fix: adiciona métodos e abstração de Material.
- 78a29b5 — refactor: Padroniza o modulo Material (entidade, service, router e testes).
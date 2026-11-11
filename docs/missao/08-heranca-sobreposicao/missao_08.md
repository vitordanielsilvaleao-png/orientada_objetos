# Missão 08 — Herança e Sobreposição

**Responsável:** Heitor

## Objetivo e planejamento

O objetivo desta missão é compreender e documentar os conceitos de herança e sobreposição de métodos na programação orientada a objetos, utilizando como referência o sistema APOLO, desenvolvido em Python para gerenciamento de biblioteca.

O planejamento consiste em analisar as classes Material, Livro e Revista, identificando como a herança permite reutilizar atributos e métodos e como a sobreposição possibilita adaptar comportamentos herdados.

## O que foi implementado e por quê

No projeto APOLO, a classe Material funciona como classe base para Livro e Revista.

A herança permite que essas classes aproveitem características comuns, como título, ano de publicação, categoria e editora, evitando a repetição de código.

Em Python, a herança é representada pela declaração de uma classe que recebe outra como referência.

Por exemplo, `class Livro(Material)` indica que Livro herda funcionalidades de Material.

A sobreposição de métodos ocorre quando uma classe filha redefine um método existente na classe pai, permitindo adaptar seu comportamento às necessidades específicas.

## Exemplos práticos encontrados no projeto

Na classe Livro, o construtor utiliza `super().__init__()` para aproveitar a inicialização dos atributos herdados de Material.

Além disso, Livro possui atributos específicos, como ISBN e autor.

Na classe Revista, também é utilizado `super().__init__()` para inicializar os atributos comuns. A classe acrescenta características próprias, como ISSN e edição.

As duas classes apresentam o método `atualizar()`, que aproveita a implementação da classe Material por meio de `super().atualizar()`.

Na classe Livro, o método permite atualizar informações específicas, como o autor. Na classe Revista, permite atualizar a edição.

Esse comportamento demonstra a sobreposição de métodos, pois as classes filhas adaptam uma funcionalidade herdada.

## Decisões técnicas e trade-offs

A utilização de herança contribui para a reutilização de código e facilita a manutenção do sistema.

O uso de `super()` permite aproveitar funcionalidades da classe pai sem precisar reescrever toda a implementação.

Como contrapartida, uma estrutura de herança muito complexa pode dificultar a compreensão das relações entre as classes.

Por isso, é importante manter uma organização clara e utilizar a herança quando existir uma relação adequada entre as classes.

## Dificuldades encontradas e soluções

Um dos principais pontos de atenção é compreender a diferença entre herdar um método e sobrescrever seu comportamento.

Outra dificuldade é entender o funcionamento de `super()`, que permite acessar métodos da classe pai.

A análise das classes Livro e Revista ajuda a compreender esses conceitos por meio de exemplos presentes no sistema APOLO.

## Reflexão sobre o conceito aprendido

Esta missão permite compreender como a herança e a sobreposição ajudam a organizar e reutilizar funcionalidades na programação orientada a objetos.

A herança possibilita compartilhar características entre classes relacionadas, enquanto a sobreposição permite personalizar comportamentos.

Esses conceitos são importantes para desenvolver sistemas mais organizados, reutilizáveis e de fácil manutenção.

## Commit(s) associado(s)

A preencher após o registro da documentação no GitHub.

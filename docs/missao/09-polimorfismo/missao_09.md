# Missão 09 — Polimorfismo

**Responsável:** Heitor

## Objetivo e planejamento

O objetivo desta missão é compreender e documentar o conceito de polimorfismo na programação orientada a objetos, utilizando como referência o sistema APOLO, desenvolvido em Python para gerenciamento de biblioteca.

O planejamento consiste em analisar a relação entre a classe Material e suas subclasses Livro e Revista, compreendendo como objetos de diferentes tipos podem utilizar métodos com o mesmo nome, apresentando comportamentos específicos.

## O que foi implementado e por quê

O polimorfismo permite que objetos de diferentes classes sejam tratados por meio de uma interface comum, respeitando o comportamento definido por cada classe.

No sistema APOLO, as classes Livro e Revista herdam funcionalidades da classe Material e apresentam especializações de métodos, como atualizar().

A utilização desse conceito contribui para a reutilização de código e facilita a manutenção do sistema, pois permite trabalhar com diferentes tipos de materiais de maneira organizada.

Em Python, o polimorfismo pode ocorrer por meio da herança e da sobrescrita de métodos, permitindo que uma chamada ao mesmo método produza comportamentos diferentes conforme o objeto utilizado.

## Exemplos práticos relacionados ao projeto

A classe Material representa características e funcionalidades comuns aos materiais da biblioteca.

As classes Livro e Revista herdam de Material e podem adaptar o método atualizar() às necessidades específicas de cada tipo de material.

Na classe Livro, o método atualizar() permite modificar informações próprias de livros, como o autor.

Na classe Revista, o método atualizar() permite modificar informações próprias de revistas, como a edição.

Dessa forma, embora os objetos pertençam a classes diferentes, ambos disponibilizam o método atualizar(), respeitando suas particularidades.

O uso de super().atualizar() permite reaproveitar a implementação da classe Material e complementar o comportamento nas subclasses.

Esse exemplo ilustra como a sobrescrita de métodos pode contribuir para o polimorfismo.

## Decisões técnicas e trade-offs

A utilização de uma classe base permite concentrar funcionalidades comuns e evitar duplicação de código.

A especialização dos métodos nas subclasses oferece flexibilidade para atender às características específicas de cada material.

Como contrapartida, é importante manter contratos de métodos consistentes, evitando diferenças inesperadas de comportamento entre as subclasses.

## Dificuldades encontradas e soluções

Uma das principais dificuldades conceituais é compreender a diferença entre herança, sobrescrita e polimorfismo.

A herança permite compartilhar características, enquanto a sobrescrita permite modificar o comportamento de um método herdado.

O polimorfismo permite utilizar objetos diferentes por meio de operações comuns, com comportamentos determinados pelo tipo de objeto.

A análise das classes Material, Livro e Revista ajuda a compreender a relação entre esses conceitos no contexto do sistema APOLO.

## Reflexão sobre o conceito aprendido

Esta missão permite compreender como o polimorfismo contribui para a flexibilidade e a organização de sistemas orientados a objetos.

A possibilidade de trabalhar com diferentes tipos de materiais por meio de métodos comuns facilita a evolução do sistema.

O polimorfismo, associado à herança e à sobrescrita, é importante para desenvolver aplicações reutilizáveis, extensíveis e de fácil manutenção.

## Commit(s) associado(s)

- `d996325` — Criação da documentação da Missão 09 — Polimorfismo.

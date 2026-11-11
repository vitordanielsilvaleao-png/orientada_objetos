# Missão 04 — Estáticos e Sobrecarga

**Responsável:** Heitor

## Objetivo e planejamento

O objetivo desta missão é compreender e documentar a utilização de métodos estáticos e o conceito de sobrecarga de métodos na programação orientada a objetos, utilizando como referência o sistema APOLO, desenvolvido em Python para gerenciamento de biblioteca.

O planejamento consiste em analisar as classes Livro e Revista, identificar a utilização do decorador `@staticmethod` e compreender como os parâmetros opcionais permitem diferentes formas de atualização dos objetos.

## O que foi implementado e por quê

No projeto APOLO, as classes Livro e Revista utilizam métodos estáticos, identificados pelo decorador `@staticmethod`.

Um método estático pertence à organização da classe, mas não precisa receber automaticamente uma instância por meio do parâmetro `self`. Esse recurso é útil para operações auxiliares que não dependem diretamente dos atributos de um objeto específico.

Outro conceito abordado é a sobrecarga de métodos. Em linguagens como Java, é possível declarar métodos com o mesmo nome e diferentes listas de parâmetros.

Em Python, a redefinição de um método com o mesmo nome não produz esse tipo de sobrecarga tradicional. Por isso, o projeto utiliza parâmetros opcionais no método `atualizar()`, permitindo diferentes chamadas sem a necessidade de criar vários métodos com o mesmo nome.

### Exemplos práticos encontrados no projeto

Na classe Livro, o método estático normalizar_isbn() remove espaços e hífens do ISBN. O método _validar_isbn() verifica se o código possui 13 dígitos numéricos e gera um ValueError caso seja inválido.

Na classe Revista, o método normalizar_issn() remove espaços e hífens do ISSN. O método _validar_issn() verifica se ele possui 8 dígitos numéricos, enquanto _validar_edicao() verifica se a edição informada é maior que zero.

Nas duas classes, o método atualizar() utiliza parâmetros opcionais definidos como None, permitindo atualizar somente os campos informados.

As classes também utilizam super().atualizar() para reaproveitar a implementação da classe Material. Livro permite atualizar o autor, enquanto Revista permite atualizar a edição.

Dessa forma, o projeto demonstra o uso de métodos estáticos e parâmetros opcionais para organizar e reutilizar código em Python.

## Decisões técnicas e trade-offs

A utilização de métodos estáticos permite organizar funcionalidades auxiliares dentro das classes relacionadas, sem exigir a criação de objetos para executá-las.

A escolha por parâmetros opcionais no método `atualizar()` também contribui para a flexibilidade do sistema, pois permite trabalhar com diferentes informações em uma mesma operação.

Como contrapartida, métodos com muitos parâmetros opcionais podem se tornar mais difíceis de compreender e manter. Por isso, é importante utilizar nomes claros e validar os dados recebidos.

## Dificuldades encontradas e soluções

Um dos pontos que exigem maior atenção neste conceito é compreender a diferença entre métodos de instância e métodos estáticos.

Outra questão importante é entender que Python não utiliza a sobrecarga tradicional baseada apenas em diferentes assinaturas de métodos.

A análise das classes Livro e Revista permite estudar essas diferenças e compreender a alternativa adotada no projeto.

## Reflexão sobre o conceito aprendido

Esta missão permite compreender como a programação orientada a objetos oferece recursos para organizar e reutilizar funcionalidades.

Os métodos estáticos são úteis quando uma operação está relacionada a uma classe, mas não depende de uma instância específica.

Já os parâmetros opcionais oferecem flexibilidade na execução dos métodos e representam uma alternativa à sobrecarga tradicional em Python.

Esses conhecimentos são importantes para desenvolver sistemas mais organizados, reutilizáveis e de fácil manutenção.

## Commit(s) associado(s)

A preencher após o registro da documentação no GitHub.

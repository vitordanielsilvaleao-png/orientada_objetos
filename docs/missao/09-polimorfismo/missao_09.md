 
# Missão 09 — Polimorfismo

**Responsável:** Heitor

## Objetivo e planejamento

O objetivo desta missão é compreender e documentar o polimorfismo na programação orientada a objetos, utilizando exemplos reais do sistema APOLO, desenvolvido em Python para gerenciamento de biblioteca.

O planejamento consiste em analisar como o SQLAlchemy permite trabalhar com diferentes tipos de materiais por meio de uma classe base comum.

## O que foi implementado e por quê

No sistema APOLO, a classe `Material` é a classe base das classes `Livro` e `Revista`.

O projeto utiliza o recurso de herança polimórfica do SQLAlchemy, configurado por meio de `polymorphic_on` e `polymorphic_identity`.

Essa configuração permite que o ORM identifique o tipo concreto de cada material e crie objetos da classe correspondente.

## Exemplos práticos relacionados ao projeto

### Polimorfismo com SQLAlchemy

Na classe `Material`, localizada em `src/modulos/material/entidades/material.py`, existe a configuração:

```python
__mapper_args__ = {
    "polymorphic_on": tipo,
    "polymorphic_identity": "material"
}
```

Na classe `Livro`, localizada em `src/modulos/livro/entidades/livro.py`, existe:

```python
__mapper_args__ = {
    "polymorphic_identity": "livro"
}
```

Na classe `Revista`, localizada em `src/modulos/revista/entidades/revista.py`, existe:

```python
__mapper_args__ = {
    "polymorphic_identity": "revista"
}
```

O atributo `tipo` permite ao SQLAlchemy identificar qual classe deve representar cada registro.

Por exemplo, uma consulta pela classe base pode retornar objetos de diferentes subclasses:

```python
materiais = session.query(Material).all()

for material in materiais:
    print(type(material).__name__, material.titulo)
```

Esse exemplo é ilustrativo e demonstra o comportamento esperado do mapeamento polimórfico.

Quando a consulta encontra um registro de livro, o SQLAlchemy pode construir um objeto `Livro`. Quando encontra um registro de revista, pode construir um objeto `Revista`.

Assim, o mesmo código trabalha com diferentes tipos de objetos por meio da classe `Material`.

### Diferença entre sobrescrita e polimorfismo

A sobrescrita acontece quando uma subclasse redefine um método herdado, como ocorre com `atualizar()` nas classes `Livro` e `Revista`.

O uso de `super().atualizar()` permite reutilizar a implementação da classe base.

Já o polimorfismo demonstrado nesta missão ocorre quando uma operação sobre `Material` pode trabalhar com instâncias concretas de `Livro` e `Revista`, sem precisar selecionar manualmente a classe de cada objeto.

## Decisões técnicas e trade-offs

O mapeamento polimórfico foi utilizado para representar diferentes tipos de materiais de maneira organizada.

A principal vantagem é permitir consultas e operações utilizando uma classe base comum.

Como contrapartida, é necessário manter as configurações de mapeamento e os valores de identificação das subclasses consistentes.

## Dificuldades encontradas e soluções

Uma dificuldade foi compreender a diferença entre herança, sobrescrita e polimorfismo.

A herança permite compartilhar atributos e métodos entre classes.

A sobrescrita permite redefinir comportamentos herdados.

O polimorfismo permite tratar objetos de tipos diferentes por meio de uma interface ou classe base comum.

A análise das configurações `polymorphic_on` e `polymorphic_identity` ajudou a identificar um exemplo concreto de polimorfismo no sistema APOLO.

## Reflexão sobre o conceito aprendido

Esta missão permitiu compreender que o polimorfismo vai além da simples sobrescrita de métodos.

No sistema APOLO, o SQLAlchemy utiliza informações do mapeamento para representar livros e revistas como objetos de suas respectivas classes, mesmo quando a consulta é realizada pela classe base `Material`.

Esse recurso facilita a organização e a evolução do sistema, permitindo trabalhar com diferentes tipos de materiais de maneira uniforme.

## Commit(s) associado(s)

- `d996325` — Criação da documentação original da Missão 09 — Polimorfismo.

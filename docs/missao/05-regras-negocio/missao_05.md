# Missão 02 — Classes, Objetos e Atributos

## Objetivo e planejamento

O objetivo desta missão foi identificar e formalizar as regras de negócio que determinam o comportamento esperado do sistema de gestão de biblioteca.

As regras foram definidas a partir do levantamento dos requisitos e da análise das operações que fazem parte do MVP, buscando garantir que as funcionalidades implementadas respeitem as condições e restrições estabelecidas para o domínio.

Para facilitar a manutenção e a organização da documentação, as regras de negócio foram separadas por funcionalidade do sistema.

---

## O que foi implementado e por quê

As regras de negócio foram documentadas e organizadas de acordo com as principais operações do sistema.

A documentação foi dividida nos seguintes grupos:

- Controle de acervo;
- Disponibilidade;
- Empréstimos;
- Reservas;
- Devoluções;
- Relatórios.

A documentação completa das regras de negócio encontra-se no diretório:


**docs/regras_de_negocio/Versão 1_0/**

Os arquivos correspondentes são:

```text
docs/regras_de_negocio/Versão 1_0/
├── acervo.md
├── devolucao.md
├── disponibilidade.md
├── emprestimo.md
├── relatorio.md
└── reserva.md
```

---

## Decisões técnicas e trade-offs

Foi decidido manter as regras de negócio em documentação própria, separada da documentação geral das missões e do código-fonte.

Essa abordagem evita a duplicação das regras em diferentes documentos e permite que a documentação específica seja atualizada independentemente conforme o sistema evolua.

Também foi adotado o versionamento da documentação por meio do diretório:

docs/regras_de_negocio/Versão 1_0/

Essa organização permite registrar futuras alterações nas regras sem perder o histórico das versões anteriores.

---

## Dificuldades encontradas e soluções

Uma das principais dificuldades encontradas foi transformar as necessidades identificadas durante o levantamento de requisitos em regras que pudessem determinar de forma objetiva o comportamento do sistema.

Também foi necessário definir regras relacionadas às situações de empréstimo, reserva, disponibilidade e devolução, considerando diferentes estados possíveis dos materiais e das operações.

Para solucionar essas questões, as regras foram analisadas durante a definição do escopo e posteriormente organizadas por funcionalidade, permitindo que cada grupo de regras possua uma documentação específica.

---

## Reflexão sobre o conceito aprendido

A elaboração das regras de negócio permitiu compreender que os requisitos funcionais descrevem o que o sistema deve permitir realizar, enquanto as regras de negócio determinam as condições e restrições que devem ser respeitadas durante essas operações.

No projeto, essa distinção foi importante para evitar que as funcionalidades fossem implementadas apenas considerando o fluxo esperado, sem considerar situações que poderiam gerar comportamentos inconsistentes.

---

## Commit(s) associado(s)

docs: adiciona a documentação de requisitos funcionais, requisitos não funcionais, regras de negócios e altera os arquivos readme.md e CHANGELOG.md (8b52979683b2deea2b27bf771bbeb245d314ce7a)

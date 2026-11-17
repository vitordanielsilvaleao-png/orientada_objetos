# Missão 13 — Arrays e Strings

## Objetivo e planejamento

O objetivo desta missão foi compreender e documentar a utilização de strings e suas operações no projeto APOLO, com foco na validação e normalização dos dados textuais das entidades.

Foi planejada a análise da função compartilhada `normalizar_texto()` e dos métodos de tratamento de nomes e títulos presentes nas classes `Autor`, `Editora`, `Categoria` e `Material`.

Os arquivos analisados foram:

- `src/compartilhado/normalizador.py`
- `src/modulos/livro/entidades/autor.py`
- `src/modulos/material/entidades/editora.py`
- `src/modulos/material/entidades/categoria.py`
- `src/modulos/material/entidades/material.py`

---

## O que foi implementado e por quê

O sistema APOLO utiliza operações com strings para validar e padronizar informações textuais antes de armazená-las no banco de dados.

Foi identificada a função compartilhada `normalizar_texto()`, que recebe uma string e aplica duas operações:

```python
def normalizar_texto(texto: str):
    texto = texto.strip().lower()
    return texto
```

O método `strip()` remove espaços em branco no início e no final da string, enquanto `lower()` converte seus caracteres para letras minúsculas.

Por exemplo, o texto `"  ROMANCE  "` é transformado em `"romance"`.

As entidades `Autor`, `Editora` e `Categoria` utilizam essa função por meio do método `normalizar_nome()`.

Essas classes também possuem o método `_validar_nome_existente()`, responsável por impedir nomes vazios ou compostos apenas por espaços.

A validação é integrada ao SQLAlchemy pelo decorador `@validates("nome")`, que executa o tratamento quando o atributo recebe um valor.

Na classe `Material`, foi identificado o método `_normalizar_titulo()`, que aplica diretamente as operações `strip()` e `lower()` ao título.

O método `validar_titulo()` verifica se o título é válido e retorna sua versão normalizada.

Essas operações contribuem para a padronização dos dados cadastrados no acervo.

Em relação aos arrays, os arquivos analisados nesta missão não apresentaram uma implementação específica de listas ou arrays relacionada à normalização textual. Assim, a análise prática concentrou-se nas operações com strings identificadas no código.

---

## Decisões técnicas e trade-offs

Uma das principais decisões técnicas identificadas foi a centralização da normalização de nomes na função `normalizar_texto()`.

Essa abordagem reduz a duplicação de código nas entidades `Autor`, `Editora` e `Categoria`, facilitando a manutenção e a padronização do comportamento.

A classe `Material`, por sua vez, implementa a normalização do título diretamente no método `_normalizar_titulo()`.

Embora as duas abordagens produzam o mesmo resultado para os exemplos analisados, a utilização de uma função compartilhada facilita futuras alterações nas regras de normalização.

Outra decisão importante foi utilizar os validadores do SQLAlchemy para integrar a validação e a normalização à atribuição dos atributos.

A normalização atual é simples: remove espaços nas extremidades e converte letras para minúsculas. Ela não remove acentos nem elimina espaços internos entre palavras.

---

## Dificuldades encontradas e soluções

Um dos desafios desta missão foi compreender a diferença entre validar e normalizar uma string.

A validação verifica se o valor recebido atende às regras estabelecidas, enquanto a normalização transforma o texto em um formato padronizado.

A análise dos métodos `_validar_nome_existente()`, `normalizar_nome()` e `validar_nome()` permitiu identificar a responsabilidade de cada operação.

Outra dificuldade foi compreender como o decorador `@validates` do SQLAlchemy participa desse processo.

Foi observado que os métodos de validação são associados aos atributos mapeados, permitindo aplicar as regras quando esses atributos recebem novos valores.

Também foi identificada uma diferença de implementação entre as entidades: `Autor`, `Editora` e `Categoria` utilizam a função compartilhada, enquanto `Material` realiza a normalização diretamente.

---

## Reflexão sobre o conceito aprendido

Esta missão permitiu compreender a importância do tratamento de strings em sistemas orientados a objetos.

As operações `strip()` e `lower()` demonstram como métodos de strings podem ser utilizados para padronizar informações recebidas dos usuários.

Também foi possível compreender a importância de reutilizar funções compartilhadas para evitar a repetição de código.

A análise das entidades mostrou como a validação e a normalização podem ser integradas às classes, contribuindo para a consistência das informações armazenadas.

Quanto aos arrays, foi possível distinguir esse conceito do tratamento de strings, reconhecendo que a implementação analisada apresenta principalmente operações textuais, sem evidenciar uma aplicação específica de arrays nesse processo.

---

## Commit(s) associado(s)

- c16da2c — feat: Adiciona a função normalizador_texto para executar a normalização de nomes recebidos pelas classes de serviço.
- 88cff3f — refactor: retira normalização de acentuação em normalizador.py.
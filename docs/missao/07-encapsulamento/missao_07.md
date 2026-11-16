# Missão 07 — Encapsulamento

## Objetivo e planejamento

O objetivo desta missão foi aplicar o conceito de encapsulamento na programação orientada a objetos, restringindo o acesso direto a determinados atributos da entidade Cliente e garantindo maior controle sobre a manipulação dos dados.

Para isso, foi planejada a utilização de atributos privados, propriedades de leitura e métodos responsáveis pela validação e normalização das informações recebidas.

---

## O que foi implementado e por quê

Foi implementado o encapsulamento dos atributos CPF e status de atividade do cliente, utilizando os atributos privados `_cpf` e `_is_active`.

O atributo `_cpf` foi associado à coluna `cpf` do banco de dados e disponibilizado para leitura por meio de `@hybrid_property`. Dessa forma, o CPF pode ser consultado, mas não alterado diretamente após sua definição.

Da mesma maneira, o atributo `_is_active` foi disponibilizado por meio de uma propriedade somente de leitura. Sua alteração deve ser realizada pelos métodos `ativar_cliente()` e `inativar_cliente()`, que controlam as operações permitidas conforme o estado atual do cliente.

Também foram implementados métodos validadores utilizando o decorador `@validates`, responsáveis por controlar os valores atribuídos aos atributos da entidade.

Entre as validações implementadas estão:

- CPF: verifica se possui 11 dígitos numéricos e realiza a normalização, removendo pontos e traços.
- Nome: remove espaços desnecessários e verifica se possui pelo menos três caracteres.
- Telefone: remove caracteres não numéricos e verifica se possui 10 ou 11 dígitos.
- Número: converte o valor para inteiro e verifica se é maior que zero.
- Rua e bairro: verificam se os valores informados não estão vazios.
- Complemento: normaliza o texto e permite valores nulos.

Também foram implementados os métodos `atualizar_cliente()`, `ativar_cliente()` e `inativar_cliente()`, que controlam as alterações permitidas conforme o estado do cliente.

Essa implementação foi realizada para proteger os dados da entidade, evitar alterações inválidas e centralizar as regras de manipulação dos atributos.

---

## Decisões técnicas e trade-offs

A principal decisão técnica foi utilizar atributos privados representados pelo prefixo `_`, seguindo a convenção de encapsulamento do Python.

Para disponibilizar os atributos CPF e status de atividade somente para leitura, foi utilizado o decorador `@hybrid_property` do SQLAlchemy.

Outra decisão foi utilizar o decorador `@validates` para executar automaticamente as validações sempre que determinados atributos recebem novos valores.

Também foram separados os métodos de normalização dos métodos de validação. Essa organização permite que os dados sejam padronizados antes de serem verificados, facilitando a manutenção e a reutilização do código.

Como trade-off, a implementação exige métodos específicos para determinadas operações, em vez de permitir alterações diretas nos atributos. Entretanto, essa abordagem oferece maior controle e segurança sobre as informações armazenadas.

---

## Dificuldades encontradas e soluções

Uma das dificuldades encontradas foi garantir que os atributos considerados privados não fossem modificados de maneira inadequada, principalmente o CPF e o status de atividade do cliente.

A solução adotada foi disponibilizar esses atributos por meio de propriedades somente de leitura e utilizar métodos específicos para controlar suas alterações.

Outra dificuldade foi organizar as validações para evitar a repetição de código e garantir que os dados fossem tratados corretamente antes de serem armazenados.

Para solucionar esse problema, foram criados métodos específicos de normalização e validação, utilizados pelos validadores associados aos atributos da entidade.

Também foram implementadas verificações no método `atualizar_cliente()`, impedindo que clientes inativos sejam modificados, além de verificações nos métodos de ativação e inativação para evitar operações repetidas.

---

## Reflexão sobre o conceito aprendido

A implementação do encapsulamento permitiu compreender a importância de controlar o acesso aos atributos de uma classe, evitando modificações indevidas e garantindo que os dados permaneçam consistentes.

Foi possível observar na prática como atributos privados, propriedades e métodos específicos podem trabalhar em conjunto para proteger as informações de uma entidade.

Além disso, a utilização dos decoradores `@hybrid_property` e `@validates` demonstrou como os recursos do SQLAlchemy podem auxiliar na aplicação dos princípios da programação orientada a objetos.

Dessa forma, o encapsulamento contribuiu para tornar a entidade Cliente mais organizada, segura e confiável, centralizando as regras de acesso, alteração e validação de seus dados.

---

## Commit(s) associado(s)

feat: implementa métodos de Cliente (abaa2b3edb326978d6fde114c39b571e2f2c2076)
refactor: Padroniza o módulo Cliente (entidade, service, router e testes) (d9793bb2d9001e28f1a823e7d5e13aa0d0c00195)
# Missão 11 — Classes Abstratas

## Objetivo e planejamento

O objetivo desta missão foi aplicar o conceito de classes abstratas na estrutura dos serviços do sistema APOLO, estabelecendo uma classe base que reúna comportamentos comuns e defina métodos obrigatórios para suas classes derivadas.

Para isso, foi planejada a criação da classe `BaseService`, utilizando os recursos `ABC` e `abstractmethod` do módulo `abc` do Python. A classe serviria como estrutura comum para os serviços da aplicação, estabelecendo um padrão para as operações de cadastro e visualização.

## O que foi implementado e por quê

Foi implementada a classe abstrata `BaseService`, localizada em:

**src/compartilhado/base_service.py**

A classe herda de `ABC`, permitindo definir métodos abstratos que devem ser implementados pelas classes derivadas.

Foram definidos dois métodos abstratos:

- `cadastrar(self, data)`: estabelece a operação de cadastro como parte obrigatória dos serviços que herdam de `BaseService`.
- `visualizar(self)`: estabelece a operação de visualização dos registros como parte obrigatória desses serviços.

Os dois métodos foram decorados com `@abstractmethod`, indicando que suas implementações devem ser fornecidas pelas subclasses.

Também foi implementado o método concreto `salvar(self, entidade)`, responsável por adicionar uma entidade à sessão do SQLAlchemy e confirmar a transação com `commit()`.

O construtor da classe recebe uma sessão do SQLAlchemy e a armazena no atributo `self.session`, permitindo que os serviços derivados utilizem a mesma estrutura de acesso à persistência.

A classe `BaseService` é herdada pelos oito services previstos para essa estrutura. Dessa forma, cada serviço implementa os métodos abstratos de acordo com as necessidades de seu respectivo módulo, mantendo um padrão comum sem impedir que cada um tenha suas próprias regras de negócio.

## Decisões técnicas e trade-offs

A principal decisão técnica desta etapa foi utilizar uma classe abstrata como estrutura base dos serviços, em vez de manter cada serviço completamente independente.

Essa abordagem permite estabelecer um contrato comum para as operações essenciais, reduzindo diferenças estruturais entre os serviços e facilitando a manutenção do código.

A utilização de `ABC` e `@abstractmethod` também impede que a classe base seja instanciada sem que os métodos obrigatórios tenham sido implementados. Assim, o próprio Python auxilia na identificação de subclasses que não cumprem o contrato definido.

Outra decisão importante foi manter o método `salvar()` como método concreto. Como a operação de adicionar uma entidade à sessão e confirmar a transação é compartilhada pelos serviços, sua implementação foi centralizada na classe base, evitando repetição de código.

Também foi considerada a relação entre classes abstratas e o SQLAlchemy. Embora a classe `Material` represente uma estrutura base para `Livro` e `Revista`, optou-se por não torná-la uma classe abstrata do Python, devido ao conflito dessa abordagem com o mapeamento ORM utilizado pelo SQLAlchemy. Dessa forma, foi mantida a estrutura de herança e persistência definida para essas entidades, sem aplicar a abstração de maneira incompatível com o mapeamento existente.

## Dificuldades encontradas e soluções

Uma das decisões que exigiu atenção foi identificar quais comportamentos deveriam ser obrigatórios para todos os serviços e quais poderiam permanecer específicos de cada módulo.

A solução foi definir `cadastrar()` e `visualizar()` como métodos abstratos, pois representam operações comuns aos serviços, enquanto as regras e os procedimentos de cada operação permanecem implementados nas respectivas subclasses.

Outro ponto de atenção foi diferenciar a aplicação de classes abstratas na camada de serviços da estrutura de herança utilizada nas entidades ORM.

No caso de `Material`, a solução foi preservar sua estrutura de herança com `Livro` e `Revista`, sem torná-la abstrata, evitando o conflito identificado com o SQLAlchemy.

## Reflexão sobre o conceito aprendido

A implementação permitiu compreender que classes abstratas são úteis para definir estruturas comuns e estabelecer contratos que devem ser respeitados pelas classes derivadas.

Também foi possível observar que a abstração contribui para a organização do projeto, pois permite centralizar comportamentos compartilhados e exigir que as subclasses implementem operações essenciais.

A utilização de `ABC` e `@abstractmethod` demonstrou como o Python pode auxiliar na construção de uma arquitetura mais consistente, identificando implementações incompletas antes que sejam utilizadas por meio da instanciação das classes.

Por fim, a missão evidenciou que a aplicação de conceitos de orientação a objetos deve considerar as características das bibliotecas utilizadas no projeto. Neste caso, foi necessário distinguir a abstração aplicada aos serviços daquela utilizada na herança das entidades mapeadas pelo SQLAlchemy.

## Commit(s) associado(s)

Criação da classe com métodos compartilhados BaseService (929cdebe75483cabd600855b7d81d896f08f2943)

refactor: Adição do método abstrato visualizar na classe BaseService (d59420a8825b20dd9ecba21e39b045e8718c16ca)

feat: Mapeia as API's para a classe Autor (bd1ca15d82a30c1f686d3042c2eff111d56ff324)

implementa métodos de AutorService (912712f7b39c282bd173b29cbeb89d968633f71d)

feat: Mapeamento da API da classe ClienteRouter e criação da classe ClinteService (13f20e24a138914946d028da447dfba84ab70107)

feat: implemente os métodos da classe ClienteService (b2db6359b3c4df17e3e89c7e95b420018d08fa82)

feat: Mapeamento da API da classe EmprestimoRouter e criação da classe EmprestimoService (630c4e9b96d1473b871f1ff24dbcacbddb2f6acf)

feat: Elabora os métodos da classe EmprestimoService (bba895a8ac1d6ed535173ab5121da1db425cb0e3)

Mapeamento da API da classe RevistaRouter e criação da classe RevistaService (54dafb1c6dcbeb3b37a82f2b90b885f91c82f755)

feat: implementa service e testes de integracao de revista (a72f1e34872773479447b1a2fc29dd75b36980c4)

feat: Criação da classe LivroService (441bc92805f4ece973365ce2af4cc4321b776bde)

feat: Mapeamento da API para a classe Categoria e criação da classe CategoriaService (c03b5a445746aa3c4b36364bd03e8dae3aeb101c)

feat: Adiciona a classe CategoriaService com atributos e métodos e seus respectivos testes (fb7be173441364290493a0ff3215ca3397666ec3)

feat: Mapeamento da API para a classe EditoraRouter e criação da classe EditoraService (a31b12a8a2e570194f22382b97457ba50b8f11c6)

feat: implementa métodos de EditoraService e validação de nome único (dfdc2d1625c18b03a1671fd9a7fc8f4d7db629ee)

feat: Mapeamento da API da classe ReservaRouter e criação da classe ReservaService (14c6d760afc4c437911557502ddeeafc8d40c7a2)

feat: implementa métodos de ReservaService (08b862776392c59a5c499ddcfc7a3d0629b956c8)
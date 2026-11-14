 
# Diagrama de Classes — Sistema APOLO

Este diagrama apresenta as principais entidades do sistema de gerenciamento de biblioteca APOLO, seus relacionamentos e a estrutura de serviços.

## 1. Diagrama das entidades

```mermaid
classDiagram
    direction TB

    class Material {
        +int id
        +str titulo
        +int ano_publi
        +int categoria_id
        +int editora_id
        +str tipo
        -StatusMaterial _status
        -bool _is_active
        +atualizar()
        +ativar()
        +inativar()
        +esta_disponivel()
        +disponibilizar()
        +reservar()
        +emprestar()
    }

    class Livro {
        +int id
        +str isbn
        +int autor_id
        +validar_isbn()
        +normalizar_isbn()
        +atualizar()
    }

    class Revista {
        +int id
        +str issn
        +int edicao
        +validar_issn()
        +validar_edicao()
        +normalizar_issn()
        +atualizar()
    }

    class Autor {
        +int id
        +str nome
        +validar_nome()
        +validar_nome_existente()
        +normalizar_nome()
        +renomear()
    }

    class Categoria {
        +int id
        +str nome
    }

    class Editora {
        +int id
        +str nome
    }

    class Cliente {
        +int id
        +str cpf
        +str nome
    }

    class Emprestimo {
        +int id
        +int cliente_id
        +int material_id
    }

    class Reserva {
        +int id
        +str titulo
        +int cliente_id
        +int material_id
        +datetime data
        -StatusReserva _status
        -bool _is_active
        +verificar_expiracao()
        +cancelar()
        +concluir()
        +vincular_material()
    }

    Material <|-- Livro
    Material <|-- Revista

    Livro --> Autor : autor_id
    Material --> Categoria : categoria_id
    Material --> Editora : editora_id

    Emprestimo --> Cliente : cliente_id
    Emprestimo --> Material : material_id

    Reserva --> Cliente : cliente_id
    Reserva --> Material : material_id
```

## 2. Diagrama dos serviços

```mermaid
classDiagram
    direction TB

    class BaseService {
        &lt;&lt;abstract&gt;&gt;
        +Session session
        +salvar(entidade)
        +cadastrar(data)
        +visualizar()
    }

    class ClienteService
    class LivroService
    class RevistaService
    class EmprestimoService
    class ReservaService
    class AutorService
    class CategoriaService
    class EditoraService

    BaseService <|-- ClienteService
    BaseService <|-- LivroService
    BaseService <|-- RevistaService
    BaseService <|-- EmprestimoService
    BaseService <|-- ReservaService
    BaseService <|-- AutorService
    BaseService <|-- CategoriaService
    BaseService <|-- EditoraService
```

## 3. Descrição dos relacionamentos

- **Material, Livro e Revista:** Livro e Revista herdam os atributos e métodos de Material.
- **Livro e Autor:** cada livro possui uma referência a um autor por meio de `autor_id`.
- **Material, Categoria e Editora:** os materiais possuem referências à categoria e à editora.
- **Empréstimo:** relaciona um cliente ao material emprestado.
- **Reserva:** relaciona um cliente ao material reservado, permitindo acompanhar o estado da reserva.
- **BaseService:** classe abstrata que centraliza operações compartilhadas, como salvar entidades, e define os métodos abstratos `cadastrar()` e `visualizar()`.
- **Services:** os serviços especializados herdam de BaseService e implementam as operações específicas de cada módulo.

## 4. Conclusão

A modelagem apresenta a estrutura principal do sistema APOLO, demonstrando herança, associações entre entidades e reutilização de código por meio da classe BaseService.

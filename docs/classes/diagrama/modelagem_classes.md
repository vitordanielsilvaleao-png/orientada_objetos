
# Diagrama de Classes — Sistema APOLO

Este diagrama representa a herança entre as classes Material, Livro e Revista do sistema de gerenciamento de biblioteca APOLO.

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

    Material <|-- Livro
    Material <|-- Revista

    Livro --> Autor : autor_id

```

## Descrição

A classe Material contém os atributos e métodos comuns aos materiais da biblioteca.

A classe Livro herda de Material e acrescenta os atributos ISBN e autor.

A classe Revista também herda de Material e acrescenta ISSN e edição.


A classe Autor representa os autores cadastrados no sistema, contendo os atributos id e nome, além de métodos de validação, normalização e alteração do nome.

A classe Livro possui o atributo autor_id, que referencia a classe Autor.

As classes Livro e Revista sobrescrevem o método atualizar(), utilizando super() para reaproveitar a implementação da classe Material.
  

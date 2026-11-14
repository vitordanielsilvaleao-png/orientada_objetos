Versão 2.0 - 11/11/2026

# Controle de Acervo

## Identificação

### [RN-ACER-001] Identificação Única de Livro
Um ISBN não poderá estar associado a dois livros diferentes.

### [RN-ACER-002] Identificação Única de Revista
Um ISSN não poderá estar associado a duas revistas diferentes.

## Dados Obrigatórios

### [RN-ACER-003] Dados Obrigatórios de Livro
Um livro deverá possuir obrigatoriamente título, autor, editora, ISBN e ano de publicação.

### [RN-ACER-004] Dados Obrigatórios de Revista
Uma revista deverá possuir obrigatoriamente título, edição, editora, ISSN e ano de publicação.

## Relacionamentos

### [RN-ACER-005] Autor do Material
Cada Livro deverá possuir obrigatoriamente um autor. Revistas não possuem autor associado.

### [RN-ACER-006] Materiais do Autor
Um autor poderá estar associado a mais de um material.

### [RN-ACER-007] Materiais da Editora
Uma editora poderá estar associada a mais de um material.

### [RN-ACER-008] Materiais da Categoria
Uma categoria poderá ser utilizada por vários materiais.

### [RN-ACER-009] Categoria do Material
Cada material deverá pertencer a somente uma categoria.

## Gestão por Exemplares e Status

### [RN-ACER-010] Controle por Exemplares Individuais
O acervo é gerido através de exemplares individuais de cada material, eliminando o controle baseado em contadores numéricos de quantidade.

### [RN-ACER-011] Status do Exemplar
O exemplar de um material poderá assumir exclusivamente os status de `DISPONIVEL`, `EMPRESTADO` ou `RESERVADO`.

### [RN-ACER-012] Inativação do Material
Um material que já esteja inativo não poderá ser inativado novamente.
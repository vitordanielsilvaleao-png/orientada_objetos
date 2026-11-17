# Apolo | Front-end

Front-end em HTML, CSS e JavaScript puro para a API Apolo.
Interface web do **Apolo**, sistema de gerenciamento de biblioteca. O front-end é feito só com HTML, CSS e JavaScript puro (sem frameworks e sem etapa de build) e conversa com a API em FastAPI por meio de `fetch` e JSON.

## Funcionalidades

- **Painel:** céu com sol ou lua conforme a hora do dia, números do acervo e listas de atenção (empréstimos atrasados, reservas abertas).
- **Livros e Revistas:** cadastro, busca, edição, inativação e reativação.
- **Empréstimos:** registro em 2 etapas (cliente, depois material), filtros por situação e devolução.
- **Reservas:** reserva por título, filtros, atender e cancelar.
- **Relatórios:** totais do acervo, ranking, atrasos e gráficos de barras.
- **Clientes:** cadastro com CPF e endereço, edição, inativação e reativação.
- **Autores, Editoras e Categorias:** cadastro e edição de nomes.
- **Validação nos formulários** com as mesmas regras do back-end (ISBN, ISSN, CPF, telefone, ano etc.).
- **Balões "?"** ao lado dos campos e painel **"Conceitos de POO"**, que explica qual classe Python está por trás de cada tela.

## Tecnologias

| Item | Uso |
|---|---|
| HTML5 | Estrutura de todas as telas, `<template>` das linhas e janelas (modais) |
| CSS3 | Identidade visual "a luz de Delfos" (lápis-lazúli, ouro e mármore) |
| JavaScript (ES6+) | Funções simples, `async/await`, `fetch`, sem classes e sem `import`/`export` |
| Google Fonts | Marcellus (títulos) e Commissioner (texto) |
| Font Awesome 6.5.1 | Ícones |

> As fontes e os ícones são carregados por CDN, então é preciso ter internet para vê-los.

## Estrutura de pastas

```
frontend/
├── index.html          # Página única: menu, 10 seções, templates e janelas
├── css/
│   └── style.css       # Estilos e identidade visual
├── js/
│   ├── geral.js        # API, avisos, formatação, validação e janelas (carregado primeiro)
│   ├── painel.js       # Painel com céu, números e listas
│   ├── livros.js       # Tela de livros
│   ├── revistas.js     # Tela de revistas
│   ├── emprestimos.js  # Empréstimos e devolução
│   ├── reservas.js     # Reservas
│   ├── relatorios.js   # Relatórios e gráficos
│   ├── clientes.js     # Tela de clientes
│   ├── catalogo.js     # Autores, editoras e categorias
│   └── navegacao.js    # Menu lateral e início do sistema (carregado por último)
└── README.md
```

## Como rodar

1. Suba a API na raiz do projeto:

```bash
uvicorn src.main:app --reload
```

2. Sirva a pasta do front-end:

```bash
python -m http.server 5500 --directory src/frontend
```

Ajuste o caminho se a pasta estiver em outro lugar. Se preferir, abra o index.html com o Live Server do VS Code.

3. Acesse `http://localhost:5500`.

## Configuração

O endereço da API fica no início do `js/geral.js`:

```js
const API = "http://localhost:8000";
```

Se a API rodar em outra porta ou máquina, altere só essa constante.

## Arquitetura

```
Navegador (HTML/CSS/JS)  <-- HTTP/JSON -->  FastAPI  -->  Router → Service → Entidade → MySQL
```

- O **HTML** fica todo no `index.html`; o **JavaScript** só preenche e reage aos eventos.
- Cada tela é uma `<section id="secao-NOME" hidden>`. O menu usa links `#livros`, `#clientes`... e o `navegacao.js` mostra uma seção por vez conforme o `#` do endereço, sem recarregar a página.
- As linhas das tabelas vêm de `<template>`, clonados com `template.content.cloneNode(true)` e preenchidos com `textContent`.
- Os scripts são comuns (não são módulos) e dividem o mesmo escopo global, por isso **a ordem das tags `<script>` importa**: `geral.js` primeiro e `navegacao.js` por último.

### Padrão de cada tela

1. `carregarX()` busca os dados com `chamarApi("GET", ...)`;
2. `renderizarX()` filtra pela busca e preenche a tabela a partir do `<template>`;
3. o `submit` do formulário valida, monta o `payload`, chama `chamarApi("POST", ...)`, mostra um aviso com `showToast` e recarrega a lista;
4. editar abre uma janela já preenchida e salva com `PATCH`;
5. inativar pede confirmação e faz `PATCH .../inativar`.

## Telas e rotas da API

| Tela | Rotas usadas |
|---|---|
| Painel | `GET /livro`, `/revista`, `/emprestimo/abertos`, `/emprestimo/atrasados`, `/reserva/abertas` |
| Livros | `GET/POST /livro`, `PATCH /livro/{id}`, `/livro/{id}/inativar`, `/livro/{id}/ativar` |
| Revistas | `GET/POST /revista`, `PATCH /revista/{id}`, `/revista/{id}/inativar`, `/revista/{id}/ativar` |
| Empréstimos | `GET /emprestimo`, `/emprestimo/abertos`, `/emprestimo/atrasados`, `POST /emprestimo`, `PATCH /emprestimo/{id}/devolver` |
| Reservas | `GET /reserva`, `/reserva/abertas`, `/reserva/expiradas`, `POST /reserva`, `PATCH /reserva/{id}`, `/reserva/{id}/cancelar` |
| Relatórios | `GET /material/quantidade/total`, `/quantidade/disponiveis`, `/emprestados`, `/quantidade/tipo`, `/quantidade/categoria` |
| Clientes | `GET/POST /cliente`, `PATCH /cliente/{id}`, `/cliente/{id}/inativar`, `/cliente/{id}/ativar` |
| Autores, Editoras, Categorias | `GET/POST /autor` (`/editora`, `/categoria`), `PATCH /autor/{id}` |

## Regras de validação no front

- ISBN com 13 dígitos, ISSN com 8, CPF com 11 e telefone com 10 ou 11 (pontos e hífens são aceitos);
- nome do cliente com pelo menos 3 letras;
- ano entre 1 e o ano atual; número e edição maiores que zero;
- nomes repetidos não são aceitos em autor, editora e categoria;
- empréstimo: o cliente não pode ter empréstimo atrasado nem 4 empréstimos ativos (prazo de 30 dias);
- reserva de título fora do acervo é aceita, e a coluna "Exemplar" indica que ele ainda não existe.

O campo com erro fica vermelho e recebe o foco. O back-end valida tudo novamente: a validação do front serve para avisar mais cedo, não para substituir a do servidor.
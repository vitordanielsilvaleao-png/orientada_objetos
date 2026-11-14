# Apolo | Front-end

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
├── docs/               # Um documento por arquivo do front
├── FRONTEND.md         # Como o front-end foi construído
└── README.md
```

## Como rodar

### Pré-requisitos

- A API do Apolo (FastAPI) rodando em `http://localhost:8000`
- Python 3 (para servir os arquivos) ou a extensão Live Server do VS Code

### Passo a passo

1. Suba a API na raiz do projeto:

   ```bash
   uvicorn src.main:app --reload
   ```

2. Sirva a pasta do front-end:

   ```bash
   python -m http.server 5500 --directory src/frontend
   ```

3. Acesse `http://localhost:5500`.

O indicador no rodapé do menu mostra **"Conectado à API"** (verde) quando o back-end responde e **"API indisponível"** (vermelho) quando não responde.

### Configuração

O endereço da API fica no início do `js/geral.js`:

```js
const API = "http://localhost:8000";
```

Se a API rodar em outra porta ou máquina, altere só essa constante. O back-end precisa ter o CORS liberado para a origem do front (no projeto, isso já está configurado no `main.py`).

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
3. o `submit` do formulário valida, monta o `payload`, chama `chamarApi("POST", ...)`, mostra um
   aviso com `showToast` e recarrega a lista;
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

## Documentação

- [`FRONTEND.md`](FRONTEND.md): como o front-end foi construído e por quê.
- [`docs/README.md`](docs/README.md): índice da documentação por arquivo. Cada documento explica variáveis, funções (com a linha), eventos, rotas usadas e perguntas que podem cair na defesa oral.

| Arquivo | Documentação |
|---|---|
| `index.html` | [docs/index-html.md](docs/index-html.md) |
| `css/style.css` | [docs/style-css.md](docs/style-css.md) |
| `js/geral.js` | [docs/geral-js.md](docs/geral-js.md) |
| `js/navegacao.js` | [docs/navegacao-js.md](docs/navegacao-js.md) |
| `js/painel.js` | [docs/painel-js.md](docs/painel-js.md) |
| `js/livros.js` | [docs/livros-js.md](docs/livros-js.md) |
| `js/revistas.js` | [docs/revistas-js.md](docs/revistas-js.md) |
| `js/emprestimos.js` | [docs/emprestimos-js.md](docs/emprestimos-js.md) |
| `js/reservas.js` | [docs/reservas-js.md](docs/reservas-js.md) |
| `js/relatorios.js` | [docs/relatorios-js.md](docs/relatorios-js.md) |
| `js/clientes.js` | [docs/clientes-js.md](docs/clientes-js.md) |
| `js/catalogo.js` | [docs/catalogo-js.md](docs/catalogo-js.md) |

## Solução de problemas

| Problema | O que verificar |
|---|---|
| Rodapé mostra "API indisponível" | A API está rodando em `http://localhost:8000`? O `API` em `js/geral.js` está correto? |
| Erro de CORS no console | O `main.py` do back-end precisa liberar a origem do front (ex.: `http://localhost:5500`) |
| Telas em branco ou funções "não definidas" | A ordem das tags `<script>` no `index.html` foi alterada? |
| Ícones e fontes não aparecem | Sem internet, as fontes e o Font Awesome (CDN) não carregam |

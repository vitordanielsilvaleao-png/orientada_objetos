# Apolo: front-end

Front-end em HTML, CSS e JavaScript puro para a API Apolo.

## Estrutura

```
index.html          página única (menu lateral + área de conteúdo)
css/styles.css      identidade visual
js/config.js        endereço da API e modo demonstração
js/api.js           ApiClient: toda a comunicação com o back-end
js/api-demo.js      ApiDemo: imita a API com dados em memória
js/ui.js            ícones, avisos (Toast), modais e formulários
js/paginas.js       uma classe por tela (herdando de PaginaLista)
js/app.js           App (rotas e menu) e Referencias (cache de nomes)
```

## Como rodar

1. Ajuste `API_URL` em `js/config.js` (padrão: `http://localhost:8000`).
2. Libere o CORS no FastAPI se o front for servido em outra porta:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # endereço onde o front roda
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Sirva a pasta com qualquer servidor estático, por exemplo `python -m http.server 5500`,
   ou monte-a no próprio FastAPI (assim não precisa de CORS):

```python
from fastapi.staticfiles import StaticFiles
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")
```

Para ver o front sem a API, abra `index.html?demo`.

## Formato da API

As telas seguem os schemas de resposta do back-end:

- Status chegam como enums em maiúsculas (`DISPONIVEL`, `ABERTO`, `ATRASADO`, `ABERTA`...); `ROTULOS_STATUS` em `js/ui.js` traduz para o rótulo exibido.
- Livros e revistas compartilham o `id` da tabela `material`; `Referencias.material()` em `js/app.js` resolve títulos pelo catálogo geral (`GET /material`).
- Reservas usam o campo `data`; empréstimos usam `data_emprestimo` e `data_devolucao`.
- O prazo de devolução (`PRAZO_EMPRESTIMO_DIAS` em `js/config.js`) precisa ser igual ao de `Emprestimo.verificar_atraso()` no back-end.

## Relatórios

A tela Relatórios usa o `MaterialRouter` (`/material/quantidade/*` e `/material/emprestados`) e as rotas de empréstimo:

- Materiais mais emprestados: contagem de `GET /emprestimo` por `material_id` (não há rota de ranking no back-end).
- Empréstimos em aberto: `GET /emprestimo/abertos`, com o prazo calculado no front.
- Devoluções atrasadas: `GET /emprestimo/atrasados`, com o telefone do cliente para contato.
- Acervo por tipo e por categoria: `GET /material/quantidade/tipo` e `/material/quantidade/categoria`.

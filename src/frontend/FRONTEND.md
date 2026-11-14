# Como o front-end foi construído: Apolo (versão 2)

## 1. Ponto de partida

O primeiro front do Apolo (`src/apolo-front/`) montava todas as telas dentro do JavaScript, com classes (`Pagina` → `PaginaLista` → `PaginaLivros`...). Funcionava bem, mas o HTML quase não existia: o `index.html` tinha 49 linhas e todo o resto era gerado em strings.

Esta versão segue o padrão do projeto de exemplo do professor (`oficina-mecanica`):

- **o HTML fica no `index.html`**: formulários, tabelas, janelas e `<template>` das linhas;
- **o JavaScript só preenche e reage**: `getElementById`, `addEventListener`, `fetch` e `template.content.cloneNode(true)`;
- **funções simples**, sem classes no JavaScript (quem tem classes é o back-end em Python);
- **balões "?"** ao lado dos campos e um painel **"Conceitos de POO"** explicando qual classe Python está por trás de cada tela.

A identidade visual (lápis-lazúli, ouro, mármore, o sol de Apolo e o menu lateral) foi mantida.

## 2. Arquitetura

```
Navegador (HTML/CSS/JS)  <-- HTTP/JSON -->  FastAPI (src/main.py)  -->  Router → Service → Entidade → MySQL
```

O front nunca acessa as classes Python. Ele só faz `fetch` para as rotas da API, que devolvem JSON. O endereço da API fica em `js/geral.js` (`const API = "http://localhost:8000"`).

Diferença para a oficina: lá o Flask serve a página e a API juntos. Aqui a API é o FastAPI, que já tem CORS liberado no `main.py`, então a página pode ser aberta por qualquer servidor estático.

## 3. Arquivos

| Arquivo | O que tem |
|---|---|
| `index.html` | Menu lateral, as 10 seções (uma por item do menu), templates das linhas, janelas de edição e confirmação, painel de conceitos |
| `css/style.css` | Identidade visual do Apolo + peças novas (balões, dicas, etapas, janelas) |
| `js/geral.js` | Endereço da API, `chamarApi()`, aviso (`showToast`), formatação, validação e janelas |
| `js/painel.js` | Céu com sol ou lua conforme a hora, números e listas de atenção |
| `js/livros.js` / `js/revistas.js` | Cadastro, lista, edição, inativação e reativação |
| `js/emprestimos.js` | Empréstimo em 2 etapas (cliente → material), filtros e devolução |
| `js/reservas.js` | Reserva por título, filtros, atender e cancelar |
| `js/relatorios.js` | Números do acervo, ranking, atrasos e gráficos de barras |
| `js/clientes.js` | Cadastro, lista, edição, inativação e reativação |
| `js/catalogo.js` | Autores, editoras e categorias (o mesmo código atende as três telas) |
| `js/navegacao.js` | Menu lateral: mostra uma seção por vez conforme o `#` do endereço |

Na oficina tudo fica num `script.js` só. Aqui o mesmo estilo foi dividido **um arquivo por tela**, porque o Apolo tem 10 telas e assim cada integrante cuida de um arquivo.

## 4. Telas e rotas da API

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

## 5. Fluxo de uma ação (registrar empréstimo)

1. **Etapa 1:** o bibliotecário escolhe o cliente e clica em "Avançar". O JavaScript confere as mesmas regras do `EmprestimoService.cadastrar()`: o cliente não pode ter empréstimo ATRASADO nem 4 empréstimos ativos.
2. **Etapa 2:** a lista de materiais mostra só os DISPONIVEL e os RESERVADOS para aquele cliente.
3. `emprestimos.js` monta `{ cliente_id, material_id }` e envia com `fetch(..., { method: "POST" })`.
4. O back-end cria o `Emprestimo`, chama `material.emprestar()` e devolve o JSON.
5. Se der certo, aparece o aviso com a data de devolução e a lista recarrega. Se der errado, o aviso vermelho mostra o `data.message` que a API mandou.

## 6. Validação nos formulários

Cada formulário valida em JavaScript antes de enviar, com as mesmas regras das entidades:

- ISBN com 13 dígitos, ISSN com 8, CPF com 11 e telefone com 10 ou 11 (pontos e hífens aceitos);
- nome do cliente com pelo menos 3 letras, ano entre 1 e o ano atual, número e edição maiores que zero;
- nome repetido em autor, editora ou categoria;
- reserva de título fora do acervo é aceita (o back-end vincula o exemplar quando o título for cadastrado), mas o aviso e a coluna "Exemplar" deixam claro que ele ainda não existe.

O campo com erro fica vermelho e recebe o foco. O back-end valida tudo de novo, então a validação do front serve para avisar mais cedo, não para substituir a do servidor.

## 7. Como rodar

1. Suba a API na raiz do projeto: `uvicorn src.main:app --reload`
2. Sirva esta pasta: `python -m http.server 5500 --directory src/frontend` (ou use a extensão Live Server do VS Code)
3. Abra `http://localhost:5500`

O indicador no rodapé do menu mostra "Conectado à API" quando o back-end responde.

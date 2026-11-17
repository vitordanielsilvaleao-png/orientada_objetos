# Missão 16 — Integração Final

## Objetivo e planejamento

O objetivo desta missão foi reunir em um único sistema funcional tudo o que foi construído nas missões anteriores: as entidades do domínio, os services com as regras de negócio, a persistência no banco de dados, a API e a interface web.

Para isso, foi planejado que o arquivo `src/main.py` seria o ponto de entrada da aplicação, responsável por criar a API, registrar as rotas de todos os módulos, padronizar as respostas de erro e iniciar as tarefas automáticas. O front-end, em `src/frontend/`, passaria a consumir essa API por HTTP, sem acessar o banco diretamente.

---

## O que foi implementado e por quê

### Ponto de entrada da API

Em `src/main.py`, a classe `FastAPI` é instanciada com o título `APOLO`, e cada módulo registra o seu router com um prefixo próprio:

| Prefixo | Router | Módulo |
|---|---|---|
| `/livro` | `LivroRouter` | `src/modulos/livro/` |
| `/revista` | `RevistaRouter` | `src/modulos/revista/` |
| `/autor` | `AutorRouter` | `src/modulos/livro/` |
| `/categoria` | `CategoriaRouter` | `src/modulos/material/` |
| `/editora` | `EditoraRouter` | `src/modulos/material/` |
| `/material` | `MaterialRouter` | `src/modulos/material/` |
| `/cliente` | `ClienteRouter` | `src/modulos/cliente/` |
| `/reserva` | `ReservaRouter` | `src/modulos/reserva/` |
| `/emprestimo` | `EmprestimoRouter` | `src/modulos/emprestimo/` |

Cada router é um objeto: o construtor cria um `APIRouter` e chama `adicionar_rotas()`, que liga cada caminho a um método. O `main.py` só instancia o objeto e chama `app.include_router(...)`.

### Caminho de uma requisição

Todos os módulos seguem as mesmas camadas, o que permitiu integrá-los da mesma forma:

```
Front-end (fetch)  →  Router  →  Depends  →  Service  →  Entidade  →  SQLAlchemy  →  MySQL
```

1. O **router** recebe a requisição e valida o corpo com o **schema** Pydantic (por exemplo, `SchemaEmprestimoCadastro`).
2. A função de **depends** (`obter_emprestimo_service`) cria o service com uma sessão aberta por `obter_sessao()`, em `src/database/depends.py`, que fecha a sessão ao final da requisição.
3. O **service** aplica as regras de negócio e chama os métodos da **entidade** (`emprestar()`, `devolver()`, `reservar()`...).
4. O `BaseService.salvar()` grava as alterações, e o router devolve a resposta no formato do schema de resposta.

Um exemplo que integra vários módulos ao mesmo tempo é o `EmprestimoService.registrar_devolucao()`: ele devolve o empréstimo, procura a reserva aberta mais antiga para o mesmo título e, se existir, chama `material.reservar()` e `reserva.vincular_material()`; se não existir, chama `material.disponibilizar()`. Empréstimo, Material e Reserva são atualizados no mesmo `commit`.

### Tratamento de erros padronizado

O `main.py` registra quatro `exception_handler`, para que o front-end receba sempre o mesmo formato `{ "success": false, "message": "...", "data": { "status_code": ... } }`:

- `ValueError` (regras das entidades) → 400;
- `RequestValidationError` (schemas) → 422, com a mensagem traduzida para o português pela classe `TradutorValidacao`, em `src/compartilhado/tradutor_validacao.py`;
- `HTTPException` (regras dos services: 404, 409...) → o status informado pelo service;
- `Exception` (erros inesperados) → 500, com "Erro interno no servidor.".

### Tarefas automáticas (scheduler)

A função `lifespan` do `main.py` usa o `BackgroundScheduler` do APScheduler. Ao iniciar a API, ela executa uma vez `atualizar_status_atrasados()` e `atualizar_expiradas()`, de `src/scheduler/funcoes_scheduler.py`, e agenda as duas para rodar a cada 60 minutos. Ao encerrar a API, o scheduler é desligado.

### Integração com o front-end

- O `CORSMiddleware` libera as requisições vindas de outra origem, já que o front é servido em outra porta (por exemplo, `http://localhost:5500`).
- No front, toda a comunicação passa pela função `chamarApi()`, em `src/frontend/js/geral.js`, que usa `fetch` com o endereço da constante `API` (`http://localhost:8000`) e devolve `{ ok, data }`.
- Os erros chegam pela função `mensagemDeErro()`, que lê o campo `message` do formato padronizado pelos handlers do `main.py`.
- Cada tela (`livros.js`, `revistas.js`, `emprestimos.js`, `reservas.js`, `relatorios.js`, `clientes.js`, `catalogo.js`, `painel.js`) chama as rotas do módulo correspondente. A lista completa de rotas por tela está em `src/frontend/README.md`.

### Verificação

A integração entre services, entidades e banco é conferida pelos testes em `tests/integracao/` (um arquivo por service), e as regras das entidades pelos testes em `tests/unitario/`. Todos rodam com:

```bash
python -m unittest
```

---

## Decisões técnicas e trade-offs

- **Um único ponto de entrada.** Deixar no `main.py` apenas a montagem da aplicação (routers, handlers, CORS e scheduler) mantém as regras de negócio nos services e nas entidades. O custo é que o arquivo cresce a cada módulo novo, já que cada router é registrado manualmente.
- **Erros no mesmo formato.** Os handlers globais evitam que cada router trate as próprias exceções e permitem que o front leia sempre `data.message`. Em troca, o handler genérico de `Exception` esconde o detalhe do erro do usuário, e o diagnóstico depende do log do servidor.
- **Scheduler dentro da API.** Rodar o APScheduler no mesmo processo do FastAPI dispensa um serviço separado. A limitação é que as atualizações só acontecem enquanto a API está no ar, e por isso elas também são executadas uma vez na inicialização.
- **Front-end separado e sem build.** O front é HTML, CSS e JavaScript puro, servido por qualquer servidor estático. Isso exige liberar o CORS no back-end. Para um projeto acadêmico, o `allow_origins=["*"]` foi aceito; em produção, seria restrito à origem do front.

---

## Dificuldades encontradas e soluções

- **Padronização dos módulos.** Os módulos foram criados em momentos diferentes e com estruturas diferentes (localização das entidades, nomes de arquivos e imports). A solução foi padronizar, módulo a módulo, as camadas (entidade, schemas, depends, service e router) e os testes, e depois ajustar o `main.py`, as migrações e o scheduler para a nova estrutura.
- **Mensagens de validação em inglês.** Os erros 422 do Pydantic chegavam em inglês e com a estrutura interna da biblioteca. A classe `TradutorValidacao` converte esses erros em uma mensagem em português, que o front exibe diretamente.
- **Regras que envolvem mais de um módulo.** A devolução precisa atualizar empréstimo, material e reserva juntos. A solução foi concentrar essa regra no `EmprestimoService`, usando a mesma sessão e um único `commit`, para que uma falha no meio não deixe o material com status inconsistente.
- **Front-end antigo.** A primeira versão do front usava classes JavaScript e um modo de demonstração com dados em memória. Ela foi substituída por uma versão mais simples, com um arquivo por tela, que chama a API real e trata os erros no formato padronizado.

---

## Reflexão sobre o conceito aprendido

A integração final mostrou na prática o valor da separação em camadas usada desde as primeiras missões. Como cada módulo segue o mesmo caminho (router, depends, service, entidade), juntá-los no `main.py` exigiu apenas registrar cada router, sem alterar as regras já implementadas.

Também ficou claro como os conceitos de orientação a objetos se combinam: herança e polimorfismo em `Material`, `Livro` e `Revista`; encapsulamento dos status nas entidades; a classe abstrata `BaseService` compartilhada pelos services; exceções convertidas em respostas HTTP; e persistência com o SQLAlchemy. O front-end, mesmo sem classes, consome esse modelo apenas pelo contrato da API, o que mostra que o domínio orientado a objetos fica isolado no back-end.

---

## Commit(s) associado(s)

feat: Implementação da biblioteca FastAPI (6f64d10bcb02cec46eb82941701a1d171109054d)

feat: Adiciona a chamada do scheduler na main e condiciona seu funcionamento junto ao FastAPI (5c76f385a04ae68910dbba3242849835bd50c5d9)

refactor: Define o tempo de execução das funções atualizar_status_atrasados e atualizar_expiradas para 60 minutos (e2fb5c40a386b5948e158beb262165a904bf07f8)

refactor: Adiciona um nome a biblioteca de API (2881c8f470483d91062bef16e12296d8430e8408)

refactor: Atualiza enum, main, migrations e scheduler para a padronização dos módulos (52c9e6aeb0b3f387e9851e949f8f4e63cbff50b1)

Merge pull request #61 from vitordanielsilvaleao-png/refactor/frontend (e550a770ddfe2031ae61d985debeaffbe7c39e9e)

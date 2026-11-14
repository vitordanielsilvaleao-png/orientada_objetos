
# Requisitos Funcionais — Versão 2.0

**Sistema:** APOLO — Sistema de Gerenciamento de Biblioteca  
**Versão:** 2.0  
**Data:** 14/11/2026  
**Versão de referência:** 1.0 — 22/08/2026  
**Branch de implementação analisada:** `develop`

## 1. Objetivo

Este documento apresenta a revisão dos requisitos funcionais do sistema APOLO, considerando os requisitos definidos na Versão 1.0 e as funcionalidades identificadas no código-fonte da branch `develop`.

A revisão tem como objetivos:

- Conferir cada requisito funcional com o que foi implementado.
- Registrar a utilização do CPF no cadastro de clientes.
- Documentar os status e as regras de funcionamento das reservas.
- Verificar a implementação dos relatórios no front-end.
- Identificar os requisitos que ficaram para versões posteriores.

A análise foi realizada por inspeção do código-fonte. A identificação de uma implementação não significa que a funcionalidade tenha sido validada por testes automatizados, testes manuais ou homologação.

## 2. Prioridades dos Requisitos

As prioridades estabelecidas na Versão 1.0 foram mantidas:

- **Essencial:** requisito imprescindível para o funcionamento do sistema.
- **Importante:** requisito que deve ser implementado, mas cuja ausência não impede o funcionamento básico do sistema.
- **Desejável:** requisito que não compromete as funcionalidades básicas e pode ser desenvolvido em versões posteriores, estando fora do MVP.

## 3. Classificação da Implementação

Para esta revisão, foram utilizadas as seguintes classificações:

- **Implementado no código:** foram identificados métodos, regras ou componentes que atendem ao requisito.
- **Não confirmado:** as evidências analisadas não são suficientes para confirmar o atendimento integral ao requisito.
- **Proposto para versão futura:** requisito desejável sem implementação específica identificada na análise, recomendado para desenvolvimento posterior.

As classificações representam o resultado da inspeção do código, não uma homologação funcional.

## 4. Índice dos Requisitos

| Sigla | Segmento |
|---|---|
| RF-ACER | Acervo |
| RF-RES | Reserva |
| RF-EMP | Empréstimo |
| RF-DEV | Devolução |
| RF-REL | Relatório |
| RF-CLI | Cliente |
| RF-MULT | Multa |
| RF-LEI | Área do Leitor |

---

## 5. Requisitos Funcionais

### 5.1. Acervo

#### [RF-ACER-001] Cadastro de Acervo

O sistema deverá permitir que o usuário cadastre um novo material do acervo, como livros e revistas, com suas devidas informações.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** Os serviços `LivroService` e `RevistaService` possuem métodos de cadastro. O sistema verifica a duplicidade de ISBN para livros e ISSN para revistas, além de validar as referências a autor, editora e categoria, conforme o tipo de material.

O cadastro também verifica a existência de reservas pendentes para associar o material recém-cadastrado quando aplicável.

#### [RF-ACER-002] Atualização do Acervo

O sistema deverá permitir que o usuário atualize os dados dos materiais do acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** Os serviços de livros e revistas possuem métodos de atualização dos dados cadastrais dos materiais.

#### [RF-ACER-003] Inativação do Acervo

O sistema deverá permitir que o usuário inative o registro de materiais do acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** Os serviços `LivroService` e `RevistaService` possuem métodos para inativar e reativar materiais. A efetiva aplicação das restrições depende das regras implementadas nas respectivas entidades.

#### [RF-ACER-004] Visualização do Acervo

O sistema deverá permitir que o usuário consulte o catálogo de materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `MaterialService` possui o método `consultar_catalogo_geral()`. Os serviços de livros e revistas também disponibilizam métodos de visualização.

#### [RF-ACER-005] Disponibilidade do Acervo

O sistema deverá permitir que o usuário consulte as quantidades totais e disponíveis em estoque dos materiais cadastrados no acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `MaterialService` possui métodos para consultar materiais disponíveis e emprestados, contar o total de materiais e contar os disponíveis.

Também existem consultas de quantidade por categoria e por tipo.

#### [RF-ACER-006] Cadastro de Categorias

O sistema deverá permitir que o usuário faça o cadastro de categorias para organização e catalogação do acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `CategoriaService` possui métodos de cadastro, visualização e atualização, incluindo normalização de nomes e verificação de duplicidade.

#### [RF-ACER-007] Cadastro de Editora

O sistema deverá permitir que o usuário faça o cadastro de editoras para organização e catalogação do acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `EditoraService` possui métodos de cadastro, visualização e atualização, com tratamento de registros duplicados.

#### [RF-ACER-008] Cadastro de Autor

O sistema deverá permitir que o usuário faça o cadastro de autores para organização e catalogação do acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `AutorService` possui métodos de cadastro, visualização e atualização, incluindo normalização de nomes e prevenção de duplicidades.

#### [RF-ACER-009] Cadastro de Mídia Digital

O sistema deverá permitir que o usuário cadastre uma nova mídia digital com suas devidas informações.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Proposto para versão futura.

**Verificação:** Não foi identificado um módulo específico de cadastro de mídias digitais entre os módulos examinados.

**Encaminhamento:** Manter o requisito no planejamento para uma versão posterior, sujeito à confirmação de que não existe implementação em outra parte do projeto.

---

### 5.2. Reserva

#### [RF-RES-001] Cadastro de Reserva

O sistema deverá permitir que o usuário faça a reserva dos materiais cadastrados no acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ReservaService` possui método de cadastro que verifica a existência e a situação do cliente, evita reservas ativas duplicadas para o mesmo título e pode vincular um material disponível.

Uma nova reserva recebe o status `ABERTA`.

#### [RF-RES-002] Visualização de Reserva

O sistema deverá permitir que o usuário faça a consulta das reservas dos materiais cadastrados no acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ReservaService` possui métodos para consultar todas as reservas, reservas abertas e reservas expiradas.

**Status identificados:**

- `ABERTA`: reserva cadastrada e ainda ativa.
- `ATENDIDA`: reserva concluída por meio do atendimento e registro de empréstimo.
- `CANCELADA`: reserva cancelada.
- `EXPIRADA`: reserva cujo prazo de validade foi ultrapassado.

O prazo identificado na entidade é de 10 dias.

#### [RF-RES-003] Cancelamento de Reserva

O sistema deverá permitir que o usuário faça o cancelamento das reservas dos materiais cadastrados no acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O serviço de reservas possui operação de cancelamento. A entidade altera o status para `CANCELADA` e encerra a reserva.

Quando aplicável, o serviço também libera o material vinculado.

---

### 5.3. Empréstimo

#### [RF-EMP-001] Cadastro de Empréstimo

O sistema deverá permitir que o usuário faça o empréstimo dos materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `EmprestimoService` possui método de cadastro com as seguintes regras:

- O cliente deve existir e estar ativo.
- O material deve existir e estar ativo.
- O material deve estar disponível ou reservado para o cliente correspondente.
- O cliente pode possuir, no máximo, quatro empréstimos ativos.
- O sistema impede novos empréstimos quando identifica empréstimo ativo com status `ATRASADO`.
- Quando há reserva correspondente, ela é concluída durante o registro do empréstimo.

O prazo de empréstimo identificado na entidade é de 30 dias.

#### [RF-EMP-002] Visualização de Empréstimo

O sistema deverá permitir que o usuário faça a consulta dos empréstimos dos materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `EmprestimoService` possui métodos para consultar todos os empréstimos, os empréstimos em aberto e os empréstimos atrasados.

---

### 5.4. Devolução

#### [RF-DEV-001] Registro de Devolução

O sistema deverá permitir que o usuário registre a devolução dos materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O método `registrar_devolucao()` localiza o empréstimo e o material associado, registra a devolução e atualiza a disponibilidade do material.

Se houver reserva pendente para o título, o material poderá ser vinculado à reserva mais antiga.

#### [RF-DEV-002] Devoluções Pendentes

O sistema deverá permitir que o usuário visualize as devoluções pendentes dos materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O método `visualizar_abertos()` consulta empréstimos ativos sem data de devolução, permitindo identificar os materiais cuja devolução permanece pendente.

#### [RF-DEV-003] Devoluções em Atraso

O sistema deverá permitir que o usuário visualize as devoluções em atraso dos materiais cadastrados no acervo.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O método `visualizar_atrasados()` consulta empréstimos ativos com status `ATRASADO`.

A entidade `Emprestimo` possui métodos para verificar o prazo de 30 dias e marcar os empréstimos atrasados.

O agendador do sistema está configurado para executar essa atualização ao iniciar a aplicação e a cada 60 minutos.

---

### 5.5. Relatório

#### [RF-REL-001] Relatório - Mais Emprestado

O sistema deverá permitir que o usuário visualize um relatório que contemple os materiais mais emprestados do acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código do front-end.

**Verificação:** A classe `PaginaRelatorios`, no arquivo `src/frontend/js/paginas.js`, possui a funcionalidade `desenharRanking()`.

O relatório consulta os empréstimos, contabiliza as ocorrências por material e apresenta um ranking dos dez materiais mais emprestados.

#### [RF-REL-002] Relatório - Empréstimos em Aberto

O sistema deverá permitir que o usuário visualize um relatório que contemple os empréstimos em aberto dos materiais do acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código do front-end.

**Verificação:** A classe `PaginaRelatorios` possui a funcionalidade `desenharAbertos()`, que consulta os empréstimos em aberto e apresenta informações como material, cliente, data do empréstimo, prazo de devolução e dias restantes.

#### [RF-REL-003] Relatório - Devoluções em Atraso

O sistema deverá permitir que o usuário visualize um relatório que contemple as devoluções em atraso dos materiais do acervo.

**Prioridade:** Importante  
**Situação na Versão 2.0:** Implementado no código do front-end.

**Verificação:** A classe `PaginaRelatorios` possui a funcionalidade `desenharAtrasados()`, que consulta os empréstimos atrasados e apresenta dados como material, cliente, telefone, prazo de devolução e dias de atraso.

**Observação geral dos relatórios:** A existência das funcionalidades foi confirmada no código do front-end da branch `develop`. Não foram executados testes de integração entre a interface e a API. Deve ser conferida a compatibilidade entre `CONFIG.PRAZO_EMPRESTIMO_DIAS`, utilizado no front-end, e o prazo de 30 dias definido na entidade `Emprestimo`.

---

### 5.6. Cliente

#### [RF-CLI-001] Cadastro de Cliente

O sistema deverá permitir que o usuário cadastre novos clientes.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ClienteService` possui método de cadastro com validação de CPF duplicado.

A entidade `Cliente` define o CPF como campo obrigatório e único, armazenado com 11 dígitos numéricos.

O sistema remove pontos e hífens do CPF antes do armazenamento.

**Observação:** Foi identificada validação de formato e quantidade de dígitos, mas não foi identificada validação dos dígitos verificadores do CPF.

#### [RF-CLI-002] Visualização de Cliente

O sistema deverá permitir que o usuário visualize novos clientes.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ClienteService` possui método para consultar os clientes cadastrados.

#### [RF-CLI-003] Atualização de Cliente

O sistema deverá permitir que o usuário atualize o cadastro de clientes cadastrados.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ClienteService` possui método de atualização dos dados cadastrais.

O CPF é tratado como identificador que não pode ser alterado após sua definição inicial na entidade.

#### [RF-CLI-004] Inativação de Cliente

O sistema deverá permitir que o usuário inative o cadastro de clientes.

**Prioridade:** Essencial  
**Situação na Versão 2.0:** Implementado no código.

**Verificação:** O `ClienteService` possui métodos de inativação e reativação de clientes.

As regras de empréstimo e reserva verificam se o cliente está ativo antes de permitir novas operações.

---

### 5.7. Multa

#### [RF-MULT-001] Multas Pendentes

O sistema deverá permitir que o usuário consulte multas pendentes de pagamento.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Proposto para versão futura.

**Verificação:** Não foi identificado um módulo específico de multas nem uma funcionalidade de consulta de multas pendentes nos códigos examinados.

**Encaminhamento:** Manter no planejamento de uma versão posterior.

#### [RF-MULT-002] Multas Pagas

O sistema deverá permitir que o usuário consulte multas pagas.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Proposto para versão futura.

**Verificação:** Não foi identificada uma funcionalidade específica de registro ou consulta de multas pagas nos códigos examinados.

**Encaminhamento:** Manter no planejamento de uma versão posterior.

---

### 5.8. Área do Leitor

#### [RF-LEI-001] Cadastro de Reserva

O sistema deverá permitir que um leitor faça a reserva de materiais cadastrados no acervo.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Não confirmado; proposto para versão futura.

**Verificação:** Existe cadastro de reservas no sistema, porém não foi confirmada uma funcionalidade específica que permita ao próprio leitor realizar reservas por meio de uma área destinada a ele.

**Encaminhamento:** Confirmar a existência de uma interface específica ou manter para versão posterior.

#### [RF-LEI-002] Vizualição de Empréstimo

O sistema deverá permitir que um leitor visualize os empréstimos de materiais ativos vinculados ao seu cadastro.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Não confirmado; proposto para versão futura.

**Verificação:** Existe consulta de empréstimos no backend, porém não foi confirmada uma área do leitor com acesso aos empréstimos vinculados ao próprio cadastro.

**Encaminhamento:** Confirmar a existência de uma interface específica ou manter para versão posterior.

#### [RF-LEI-003] Vizualição de Multas

O sistema deverá permitir que um leitor visualize as multas por atraso associadas a seu usuário.

**Prioridade:** Desejável  
**Situação na Versão 2.0:** Proposto para versão futura.

**Verificação:** Não foi identificada uma funcionalidade específica de consulta de multas pelo leitor.

**Encaminhamento:** Manter no planejamento de uma versão posterior.

---

## 6. Resumo da Revisão

A revisão contemplou os 29 requisitos funcionais definidos na Versão 1.0.

| Segmento | Requisitos | Implementação identificada | Não confirmados ou propostos para versão futura |
|---|---:|---:|---:|
| Acervo | 9 | 8 | 1 |
| Reserva | 3 | 3 | 0 |
| Empréstimo | 2 | 2 | 0 |
| Devolução | 3 | 3 | 0 |
| Relatório | 3 | 3 | 0 |
| Cliente | 4 | 4 | 0 |
| Multa | 2 | 0 | 2 |
| Área do Leitor | 3 | 0 | 3 |
| **Total** | **29** | **23** | **6** |

### 6.1. Funcionalidades identificadas na Versão 2.0

Foram identificadas implementações relacionadas a:

- Gerenciamento de livros e revistas.
- Cadastro de categorias, editoras e autores.
- Consulta e controle de disponibilidade do acervo.
- Cadastro de clientes com CPF obrigatório e único.
- Cadastro, visualização e cancelamento de reservas.
- Controle dos status das reservas.
- Cadastro e consulta de empréstimos.
- Registro de devoluções e controle de atrasos.
- Relatórios de materiais mais emprestados, empréstimos em aberto e devoluções em atraso no front-end.

### 6.2. Requisitos propostos para versões futuras

Os seguintes requisitos desejáveis não tiveram implementação específica confirmada na análise:

- RF-ACER-009 — Cadastro de Mídia Digital.
- RF-MULT-001 — Multas Pendentes.
- RF-MULT-002 — Multas Pagas.
- RF-LEI-001 — Cadastro de Reserva pelo Leitor.
- RF-LEI-002 — Visualização de Empréstimo pelo Leitor.
- RF-LEI-003 — Visualização de Multas pelo Leitor.

O adiamento definitivo desses requisitos deve ser confirmado pela equipe do projeto, pois a análise não incluiu uma verificação exaustiva de todos os arquivos e fluxos do sistema.

### 6.3. Pontos pendentes de validação

Embora as implementações tenham sido identificadas no código, ainda devem ser verificados:

1. Os testes automatizados e manuais dos requisitos funcionais.
2. O funcionamento das rotas da API em execução.
3. A integração dos relatórios do front-end com os dados retornados pelo backend.
4. A correspondência entre o prazo de empréstimo configurado no front-end e os 30 dias definidos na entidade.
5. A execução efetiva do scheduler no ambiente de implantação.
6. A existência de eventuais funcionalidades desejáveis em outras partes do projeto.

---

## 7. Conclusão

A análise da branch `develop` identificou implementações relacionadas aos 23 requisitos essenciais e importantes previstos para o sistema APOLO.

Os seis requisitos classificados como desejáveis não tiveram sua implementação específica confirmada nos componentes analisados e foram registrados como candidatos ao desenvolvimento em versões posteriores.

A Versão 2.0 documenta, especialmente, a utilização do CPF no cadastro de clientes, o controle dos status das reservas e a implementação dos relatórios no front-end.

A presente revisão registra evidências encontradas no código-fonte e não substitui a realização de testes ou a homologação das funcionalidades.

# Missão 06 — Repetição e Relatórios

# Objetivo e planejamento

O objetivo desta missão foi implementar laços de repetição e empréstimos e uma tela de relatórios no front-end.

Para isso, foram criadas funções de varredura e atualização em lote utilizando laços de repetição no backend `src\scheduler\funcoes_scheduler.py`, e uma interface dedicada a exibição de relatórios no frontend em `src\frontend\js\paginas.js`, capaz de exibir rankings de empréstimos de materiais, tabelas de controle de prazos, resumos quantitativos do acervo, além de permitir a impressão dos relatórios.

# O que foi implementado e por quê

No frontend, foi implementada a classe `PaginaRelatorios`, que gerencia a visualização da página de relatórios com base nos dados da API.

Já no backend, foram criadas as seguintes funções de varredura:

- `atualizar_status_atrasados()`: filtra empréstimos ativos com status `ABERTO` e aplica a função `marcar_atrasado()` para verificar o prazo e marcar atrasos em caso de necessidade.
- `atualizar_expiradas()`: varre reservas ativas, aplicando a função `verificar_expiracao()` para conferir prazos expirados.


# Decisões técnicas e trade-offs

A principal decisão técnica no frontend foi o uso de funções puras de manipulação de datas e coleções (Array.prototype.map, filter, sort, reduce) diretamente sobre os dados obtidos da API, garantindo alta reatividade e clareza no cálculo de prazos através de constantes como UM_DIA e funções utilitárias como diasDesde e prazoDevolucao.

No backend, optou-se por isolar a lógica de varredura periódica em funções dedicadas com tratamento robusto de transações (try/except/finally, commit e rollback), garantindo que falhas em um registro específico durante o loop de atualização em lote não corrompam o estado geral da sessão do banco de dados.


# Dificuldades encontradas e soluções

Uma das dificuldades foi lidar com a conversão de datas e o cálculo exato de prazos transcorridos, tanto no backend para a expiração quanto no frontend para a exibição de dias de atraso e status de vencimento (`diasDesde` e `prazoDevolucao`).

A solução adotada consistiu em padronizar o fator de cálculo utilizando constantes de tempo em milissegundos (`UM_DIA`) e funções auxiliares dedicadas a isolar a lógica de comparação de datas, garantindo consistência entre os relatórios exibidos na tela e as regras de negócio executadas pelo scheduler.


# Reflexão sobre o conceito aprendido

A implementação desta missão permitiu compreender a importância da repetição automatizada de tarefas no ciclo de vida de uma aplicação, saindo de um modelo puramente reativo (acionado apenas por cliques do usuário) para um modelo que também processa regras de tempo de forma autônoma.

No aspecto visual e de relatórios, ficou evidente como transformar dados brutos de tabelas relacionais em indicadores visuais claros (gráficos de barras, selos de urgência e rankings) melhora significativamente a experiência de monitoramento e a tomada de decisões no gerenciamento do acervo.


# Commit(s) associado(s)

feat: Adiciona o front-end com a tela de Relatórios (b0046e01a3f3081a6c359a342cc53c0a9d93fd5e)

refactor: Transforma o método atualizar_status_atrasdo da classe EmprestimoService e o método atualizar_expiracao da classe ReservaService em funções que serão executadas via scheduler (5da0c9851b6635d39f1b0bdb4500b168631b20c2)

feat: Adiciona um tratamento de erro nas funções do escheduler (f499dc9a215431b268b05ffd577cbf13d2c96141)

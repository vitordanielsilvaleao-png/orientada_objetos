/**
 * Configuração do front-end Apolo.
 *
 * API_URL: endereço onde a API Python (FastAPI) está rodando.
 * PRAZO_EMPRESTIMO_DIAS: prazo de devolução; o mesmo usado em Emprestimo.verificar_atraso() no back-end.
 * MODO_DEMO: quando ativo, o front usa dados fictícios em memória e não chama a API.
 *            Ative abrindo a página com ?demo no final do endereço (ex.: index.html?demo).
 */
const CONFIG = Object.freeze({
  API_URL: 'http://localhost:8000',
  PRAZO_EMPRESTIMO_DIAS: 30,
  MODO_DEMO: new URLSearchParams(window.location.search).has('demo'),
});

/**
 * Componentes de interface reutilizáveis: ícones, formatação, avisos, modais e formulários.
 */

const ICONES = {
  painel: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  livro: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
  revista: '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h8M8 11h8M8 15h5"/>',
  emprestimo: '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
  reserva: '<path d="M6 3h12v18l-6-4-6 4z"/>',
  cliente: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>',
  autor: '<path d="M20 4C13 4 7 8 5.5 15.5L4 20l4.5-1.5C16 17 20 11 20 4z"/><path d="M5.5 18.5 14 10"/>',
  editora: '<path d="M12 3 3 8h18zM3 21h18M4.5 18h15M6.5 8v10M10 8v10M14 8v10M17.5 8v10"/>',
  categoria: '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.4"/>',
  mais: '<path d="M12 5v14M5 12h14"/>',
  editar: '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
  inativar: '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
  ativar: '<path d="M12 3v8"/><path d="M6.3 7a8 8 0 1 0 11.4 0"/>',
  devolver: '<path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  x: '<path d="M6 6l12 12M18 6 6 18"/>',
  busca: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
  menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
  alerta: '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
  relatorio: '<path d="M4 20h16"/><path d="M7 16v-5M12 16V6M17 16v-8"/>',
  imprimir: '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="1.5"/><path d="M7 14h10v7H7z"/>',
  louro: '<path d="M9 20.5C5 18.5 3 14.5 3.6 9.5M15 20.5c4-2 6-6 5.4-11"/><path d="M4.4 16.5 7 15.6M3.6 13l2.7-.4M3.6 9.5 6 9.9M19.6 16.5 17 15.6M20.4 13l-2.7-.4M20.4 9.5 18 9.9"/>',
};

/** A lira, instrumento de Apolo, ilustra os estados vazios. */
const LIRA = `<svg class="lira" viewBox="0 0 64 64" aria-hidden="true">
  <path d="M22 54h20"/>
  <path d="M24 54c-9-5-12-15-9-26 2-6 0-11-5-14"/>
  <path d="M40 54c9-5 12-15 9-26-2-6 0-11 5-14"/>
  <path d="M15 22h34"/>
  <path d="M27 22v32M32 22v32M37 22v32"/>
  <circle cx="10" cy="14" r="2.5"/><circle cx="54" cy="14" r="2.5"/>
</svg>`;

function icone(nome, classe = '') {
  return `<svg class="ic ${classe}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONES[nome] || ''}</svg>`;
}

/** Escapa texto antes de inserir em HTML, evitando injeção de conteúdo. */
function esc(valor) {
  return String(valor ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function normalizar(texto) {
  return String(texto ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function estaAtivo(item) {
  return (item.is_active ?? item.ativo ?? true) !== false;
}

function formatarData(valor) {
  if (!valor) return '—';
  const data = new Date(valor);
  if (Number.isNaN(data.getTime())) return esc(valor);
  return data.toLocaleDateString('pt-BR');
}

function plural(n, singular, pluralTexto) {
  return `${n} ${n === 1 ? singular : pluralTexto}`;
}

function capitalizar(texto) {
  const t = String(texto ?? '');
  return t.charAt(0).toUpperCase() + t.slice(1);
}

/** Rótulos dos status da API, que chegam como enums em maiúsculas e sem acento. */
const ROTULOS_STATUS = {
  disponivel: 'Disponível', emprestado: 'Emprestado', reservado: 'Reservado',
  aberto: 'Aberto', devolvido: 'Devolvido', atrasado: 'Atrasado',
  aberta: 'Aberta', atendida: 'Atendida', cancelada: 'Cancelada', expirada: 'Expirada',
};

/** Selo de situação com cor conforme o significado. */
function selo(texto, tom) {
  return `<span class="selo selo-${tom}">${esc(texto)}</span>`;
}

function seloAtivo(item) {
  return estaAtivo(item) ? selo('Ativo', 'louro') : selo('Inativo', 'neutro');
}

function seloStatus(status) {
  const s = normalizar(status);
  if (!s) return selo('—', 'neutro');
  let tom = 'ouro';
  if (s.includes('indispon')) tom = 'neutro';
  else if (s.includes('disponiv')) tom = 'louro';
  else if (s.includes('reservad')) tom = 'lapis';
  else if (s.includes('atras')) tom = 'granada';
  else if (/devolv|atendid|conclu|finaliz/.test(s)) tom = 'louro';
  else if (/expir|cancel|inativ/.test(s)) tom = 'neutro';
  return selo(ROTULOS_STATUS[s] ?? capitalizar(status), tom);
}

/** Avisos temporários no canto da tela. */
class Toast {
  static mostrar(mensagem, tipo = 'sucesso') {
    const area = document.getElementById('toasts');
    const aviso = document.createElement('div');
    aviso.className = `toast toast-${tipo}`;
    aviso.setAttribute('role', tipo === 'erro' ? 'alert' : 'status');
    aviso.innerHTML = `${icone(tipo === 'erro' ? 'alerta' : 'check')}<span>${esc(mensagem)}</span>`;
    area.append(aviso);
    setTimeout(() => {
      aviso.classList.add('saindo');
      setTimeout(() => aviso.remove(), 300);
    }, tipo === 'erro' ? 6000 : 3500);
  }
}

/** Janela modal para formulários e confirmações, usando o elemento <dialog>. */
class Modal {
  static get elemento() { return document.getElementById('modal'); }

  static iniciar() {
    this.elemento.addEventListener('click', (e) => { if (e.target === this.elemento) this.elemento.close(); });
  }

  /**
   * campos: [{ nome, rotulo, tipo, obrigatorio, opcoes, inteiro, min, max, largura, dica, placeholder, sugestoes, vazioComo, avisoSemOpcoes }]
   * aoEnviar(dados): função assíncrona; se lançar erro, a mensagem aparece dentro do modal.
   */
  static formulario({ titulo, descricao, campos, valores = {}, textoBotao = 'Salvar', aoEnviar }) {
    const d = this.elemento;
    d.innerHTML = `
      <form class="modal-corpo" novalidate>
        <header class="modal-topo">
          <div>
            <h2>${esc(titulo)}</h2>
            ${descricao ? `<p>${esc(descricao)}</p>` : ''}
          </div>
          <button type="button" class="botao-icone" data-fechar aria-label="Fechar">${icone('x')}</button>
        </header>
        <div class="campos">${campos.map((c) => Modal.campoHtml(c, valores[c.nome])).join('')}</div>
        <p class="modal-erro" role="alert" hidden></p>
        <footer class="modal-acoes">
          <button type="button" class="botao botao-secundario" data-fechar>Cancelar</button>
          <button type="submit" class="botao botao-primario">${esc(textoBotao)}</button>
        </footer>
      </form>`;

    const form = d.querySelector('form');
    const erro = d.querySelector('.modal-erro');
    const enviar = form.querySelector('[type=submit]');
    d.querySelectorAll('[data-fechar]').forEach((b) => { b.onclick = () => d.close(); });

    form.onsubmit = async (e) => {
      e.preventDefault();
      erro.hidden = true;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      enviar.disabled = true;
      enviar.classList.add('carregando');
      try {
        await aoEnviar(Modal.lerCampos(form, campos));
        d.close();
      } catch (err) {
        erro.textContent = err.message;
        erro.hidden = false;
      } finally {
        enviar.disabled = false;
        enviar.classList.remove('carregando');
      }
    };

    d.showModal();
    form.querySelector('input, select')?.focus();
  }

  static campoHtml(c, valor) {
    const id = `campo-${c.nome}`;
    const obrigatorio = c.obrigatorio ? 'required' : '';
    let controle;
    let dica = c.dica || '';

    if (c.tipo === 'select') {
      const opcoes = (typeof c.opcoes === 'function' ? c.opcoes() : c.opcoes) || [];
      if (!opcoes.length && c.avisoSemOpcoes) dica = c.avisoSemOpcoes;
      controle = `
        <select id="${id}" name="${c.nome}" ${obrigatorio}>
          <option value="">${esc(c.placeholder || 'Selecione')}</option>
          ${opcoes.map((o) => `<option value="${esc(o.valor)}" ${String(o.valor) === String(valor ?? '') ? 'selected' : ''}>${esc(o.texto)}</option>`).join('')}
        </select>`;
    } else {
      const sugestoes = c.sugestoes ? c.sugestoes() : null;
      controle = `
        <input id="${id}" name="${c.nome}" type="${c.tipo || 'text'}" value="${esc(valor ?? '')}" ${obrigatorio}
          ${c.min != null ? `min="${c.min}"` : ''} ${c.max != null ? `max="${c.max}"` : ''}
          ${sugestoes ? `list="${id}-lista"` : ''} placeholder="${esc(c.placeholder || '')}" autocomplete="off">
        ${sugestoes ? `<datalist id="${id}-lista">${sugestoes.map((s) => `<option value="${esc(s)}">`).join('')}</datalist>` : ''}`;
    }

    return `
      <label class="campo ${c.largura === 'meia' ? 'campo-meia' : ''}" for="${id}">
        <span class="campo-rotulo">${esc(c.rotulo)}${c.obrigatorio ? '' : ' <em>opcional</em>'}</span>
        ${controle}
        ${dica ? `<small>${esc(dica)}</small>` : ''}
      </label>`;
  }

  /** Lê o formulário; campos vazios são omitidos (ou recebem vazioComo, se definido). */
  static lerCampos(form, campos) {
    const dados = {};
    for (const c of campos) {
      const valor = form.elements[c.nome].value.trim();
      if (valor === '') {
        if (c.vazioComo !== undefined) dados[c.nome] = c.vazioComo;
        continue;
      }
      dados[c.nome] = (c.tipo === 'number' || c.inteiro) ? Number(valor) : valor;
    }
    return dados;
  }

  /** Pergunta de confirmação; resolve true se a pessoa confirmar. */
  static confirmar({ titulo, mensagem, textoBotao = 'Confirmar', textoVoltar = 'Cancelar', perigo = false }) {
    return new Promise((resolver) => {
      const d = this.elemento;
      let resposta = false;
      d.innerHTML = `
        <div class="modal-corpo modal-confirmar">
          <header class="modal-topo"><div><h2>${esc(titulo)}</h2><p>${esc(mensagem)}</p></div></header>
          <footer class="modal-acoes">
            <button type="button" class="botao botao-secundario" data-resposta="nao">${esc(textoVoltar)}</button>
            <button type="button" class="botao ${perigo ? 'botao-perigo' : 'botao-primario'}" data-resposta="sim">${esc(textoBotao)}</button>
          </footer>
        </div>`;
      d.querySelectorAll('[data-resposta]').forEach((b) => {
        b.onclick = () => { resposta = b.dataset.resposta === 'sim'; d.close(); };
      });
      d.addEventListener('close', () => resolver(resposta), { once: true });
      d.showModal();
      d.querySelector('[data-resposta="sim"]').focus();
    });
  }
}

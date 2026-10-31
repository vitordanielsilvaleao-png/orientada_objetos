# Alterações na identidade visual

Registro das mudanças visuais ligadas ao tema de Apolo, com o código anterior para poder desfazer.
Para voltar, substitua o trecho "Depois" pelo trecho "Antes" no arquivo indicado.

## 2026-10-29: favicon com o sol da marca

Arquivo: `index.html` (tag `<link rel="icon">` dentro do `<head>`).

O favicon era um círculo dourado sobre fundo lápis-lazúli. Passou a ser o mesmo sol com 12 raios
(alternando longos e curtos) usado na marca da barra lateral.

Antes:

```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Ccircle cx='24' cy='24' r='22' fill='%2313203B'/%3E%3Ccircle cx='24' cy='24' r='9' fill='%23D6A93A'/%3E%3C/svg%3E">
```

Depois:

```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Ccircle cx='24' cy='24' r='23' fill='%2313203B'/%3E%3Ccircle cx='24' cy='24' r='8' fill='%23D6A93A'/%3E%3Cpath d='M36.0 24.0L43.0 24.0M34.4 30.0L38.3 32.2M30.0 34.4L33.5 40.5M24.0 36.0L24.0 40.5M18.0 34.4L14.5 40.5M13.6 30.0L9.7 32.2M12.0 24.0L5.0 24.0M13.6 18.0L9.7 15.8M18.0 13.6L14.5 7.5M24.0 12.0L24.0 7.5M30.0 13.6L33.5 7.5M34.4 18.0L38.3 15.7' stroke='%23D6A93A' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E">
```

## 2026-10-29: indicador de carregamento com o sol girando

Arquivo: `css/styles.css`.

O indicador `.girando` (usado em "Carregando…" nas tabelas, no painel e nos relatórios) era um
anel dourado girando. Passou a ser um sol de 8 raios girando devagar. O spinner dos botões
(`.botao.carregando::before`) não mudou.

Foram duas mudanças. Para desfazer, volte a regra `.girando` e apague a variável `--sol-girando`.

1. Variável nova no `:root`, logo antes de `--meandro` (apagar ao desfazer):

```css
--sol-girando: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='4.2' fill='%23D6A93A'/%3E%3Cpath d='M19.0 12.0L22.8 12.0M16.9 16.9L19.6 19.6M12.0 19.0L12.0 22.8M7.1 16.9L4.4 19.6M5.0 12.0L1.2 12.0M7.1 7.1L4.4 4.4M12.0 5.0L12.0 1.2M16.9 7.1L19.6 4.4' stroke='%23D6A93A' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
```

2. Regra `.girando`.

Antes:

```css
.girando {
  display: inline-block !important;
  width: 16px; height: 16px;
  margin: 0 10px -3px 0 !important;
  border: 2px solid var(--ouro);
  border-right-color: transparent;
  border-radius: 50%;
  animation: girar 0.8s linear infinite;
}
```

Depois:

```css
/* Carregamento: o sol de Apolo girando */
.girando {
  display: inline-block !important;
  width: 18px; height: 18px;
  margin: 0 10px -4px 0 !important;
  background: var(--sol-girando) center / contain no-repeat;
  animation: girar 1.6s linear infinite;
}
```

## 2026-10-29: coroa de louros no ranking (junto com a tela Relatórios)

Arquivos: `js/ui.js` (ícone `louro` em `ICONES`) e `js/paginas.js` (função `graficoBarras`).

O 1º lugar de "Materiais mais emprestados" mostra a coroa de louros no lugar do número.
Para desfazer só a coroa, troque em `graficoBarras`:

```js
${pos === 0 ? icone('louro') : pos + 1}
```

por:

```js
${pos + 1}
```

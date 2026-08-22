Versão 1.0 - 22/08/2026

## Prioridades dos Requisitos

Para estabelecer a prioridade dos requisitos foram adotadas as denominações “essencial”,
“importante” e “desejável”.

• **Essencial** é o requisito sem o qual o sistema não entra em funcionamento. Requisitos
essenciais são requisitos imprescindíveis, que têm que ser implementados
impreterivelmente.

• **Importante** é o requisito sem o qual o sistema entra em funcionamento, mas de forma
satisfatória. Requisitos importantes devem ser implementados, mas, se não forem, os
sistema poderá ser implantado e usado mesmo assim.

• **Desejável** é o requisito que não compromete as funcionalidades básicas do sistema, isto é,
o sistema pode funcionar de forma satisfatória sem ele. Requisitos desejáveis são requisitos
que podem ser deixados para versões posteriores do sistema, caso não haja tempo hábil
para implementá-los na versão que esta sendo especificada. Estão fora do MVP.


---

## Indices

| Sigla  |       Segmento | 
|--------|---------------:|
| RF-ACER|         Acervo | 
| RF-RES |        Reserva | 
| RF-EMP |     Empréstimo | 
| RF-DEV |      Devolução | 
| RF-REL |      Relatório | 
| RF-CLI |        Cliente | 
| RF-MULT |          Multa |
| RF-LEI | Área do Leitor |

---

### [RF-ACER-001] Cadastro de Acervo

O sistema deverá permitir que o usuário cadastre um novo material do acervo, como livros e revistas com suas devidas informações.

**Prioridade**: Essencial

### [RF-ACER-002] Atualização do Acervo

O sistema deverá permitir que o usuário atualize os dados dos materiais do acervo.

**Prioridade**: Essencial

### [RF-ACER-003] Inativação do Acervo

O sistema deverá permitir que o usuário inative o registro de materiais do acervo.

**Prioridade**: Essencial

### [RF-ACER-004] Visualização do Acervo

O sistema deverá permitir que o usuário consulte o catálogo de materiais cadastrados no acervo.

**Prioridade**: Essencial

### [RF-ACER-005] Disponibilidade do Acervo

O sistema deverá permitir que o usuário consulte as quantidades totais e disponíveis em estoque dos materiais cadastrados no acervo.

**Prioridade**: Importante

### [RF-ACER-006] Cadastro de Categorias

O sistema deverá permitir que o usuário faça o cadastro de Categorias para organização e catalogação do acervo.

**Prioridade**: Essencial

### [RF-ACER-007] Cadastro de Editora

O sistema deverá permitir que o usuário faça o cadastro de Editoras para organização e catalogação do acervo.

**Prioridade**: Essencial

### [RF-ACER-008] Cadastro de Autor

O sistema deverá permitir que o usuário faça o cadastro de Autores para organização e catalogação do acervo.

**Prioridade**: Essencial

### [RF-ACER-009] Cadastro de Mídia Digital

O sistema deverá permitir que o usuário cadastre uma nova Mídia Digital com suas devidas informações.

**Prioridade**: Desejável

---

### [RF-RES-001] Cadastro de Reserva

O sistema deverá permitir que o usuário faça a reserva dos materiais cadastrados no acervo.

**Prioridade**: Importante

### [RF-RES-002] Visualização de Reserva

O sistema deverá permitir que o usuário faça a consulta das reservas dos materiais cadastrados no acervo.

**Prioridade**: Importante

### [RF-RES-003] Cancelamento de Reserva

O sistema deverá permitir que o usuário faça o cancelamento das reservas dos materiais cadastrados no acervo.

**Prioridade**: Importante

---

### [RF-EMP-001] Cadastro de Empréstimo

O sistema deverá permitir que o usuário faça o empréstimo dos materiais cadastrados no acervo.

**Prioridade**: Essencial

### [RF-EMP-002] Visualização de Empréstimo

O sistema deverá permitir que o usuário faça a consulta dos empréstimos dos materiais cadastrados no acervo.

**Prioridade**: Essencial

---

### [RF-DEV-001] Registro de Devolução

O sistema deverá permitir que o usuário registre a devolução dos materiais cadastrados no acervo.

**Prioridade**: Essencial

### [RF-DEV-002] Devoluções Pendentes

O sistema deverá permitir que o usuário visualize as devoluções pendentes dos materiais cadastrados no acervo.

**Prioridade**: Essencial

### [RF-DEV-003] Devoluções em Atraso

O sistema deverá permitir que o usuário visualize as devoluções em atraso dos materiais cadastrados no acervo.

**Prioridade**: Essencial

---

### [RF-REL-001] Relatório - Mais Emprestado

O sistema deverá permitir que o usuário visualize um relatório que contemple os materiais mais emprestado do acervo.

**Prioridade**: Importante

### [RF-REL-002] Relatório - Empréstimos em Aberto

O sistema deverá permitir que o usuário visualize um relatório que contemple os empréstimos em aberto dos materiais do acervo.

**Prioridade**: Importante

### [RF-REL-003] Relatório - Devoluções em Atraso

O sistema deverá permitir que o usuário visualize um relatório que contemple as devoluções em atraso dos materiais do acervo.

**Prioridade**: Importante

---

### [RF-CLI-001] Cadastro de Cliente

O sistema deverá permitir que o usuário cadastre novos clientes.

**Prioridade**: Essencial

### [RF-CLI-002] Visualização de Cliente

O sistema deverá permitir que o usuário visualize novos clientes.

**Prioridade**: Essencial

### [RF-CLI-003] Atualização de Cliente

O sistema deverá permitir que o usuário atualize o cadastro de clientes cadastrados.

**Prioridade**: Essencial

### [RF-CLI-004] Inativação de Cliente

O sistema deverá permitir que o usuário inative o cadastro de clientes.

**Prioridade**: Essencial

---

### [RF-MULT-001] Multas Pendentes

O sistema deverá permitir que o usuário consulte multas pendentes de pagamento.

**Prioridade**: Desejável

### [RF-MULT-002] Multas Pagas

O sistema deverá permitir que o usuário consulte multas pagas.

**Prioridade**: Desejável

---

### [RF-LEI-001] Cadastro de Reserva

O sistema deverá permitir que um leitor faça a reserva de materiais cadastrados no acervo.

**Prioridade**: Desejável

### [RF-LEI-002] Vizualição de Empréstimo

O sistema deverá permitir que um leitor visualize os empréstimos de materiais ativos vinculados ao seu cadastro.

**Prioridade**: Desejável

### [RF-LEI-003] Vizualição de Multas

O sistema deverá permitir que um leitor visualize as multas por atraso associadas a seu usuário.

**Prioridade**: Desejável
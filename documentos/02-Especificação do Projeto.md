# Especificações do Projeto

<span style="color:red">Pré-requisitos: <a href="../Documentação de contexto/introducao.md"> Documentação de Contexto</a></span>

Definição do problema e ideia de solução a partir da perspectiva do usuário. 

## Usuários

| Tipo de Usuário   | Descrição | Responsabilidades |
|------------------|-----------|------------------|
| **Administrador** | Dono(a) da loja de roupas que gerencia todo o sistema. | Cadastrar, editar e excluir produtos; gerenciar estoque; acompanhar pedidos; cadastrar clientes; gerar relatórios de vendas. |
| **Cliente** | Usuário que acessa o catálogo online de produtos. | Cadastrar-se, visualizar produtos em estoque, realizar pedidos e acompanhar status. |

---

## Arquitetura e Tecnologias

O sistema será baseado em uma arquitetura **Web MVC (Model-View-Controller)** utilizando **Django (Python)** no backend, banco de dados **SQLite** (ou PostgreSQL em produção) e **HTML/CSS/Tailwind/JavaScript** no frontend.  

A comunicação entre as camadas será feita através de views do Django, que retornarão templates renderizados dinamicamente com os dados da base de dados.  
 ''Para pagamento, será integrado o **Stripe** (cartão, Pix e boleto via API).  
Para cálculo de frete, será utilizada a **API dos Correios**. ''

**Resumo das Tecnologias:**
- **Backend:** Python 3.13, Django 5. 
- **Frontend:** HTML5, CSS3 (Tailwind), JavaScript  
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)  
- **Pagamentos:** Stripe API  
- **Frete:** API Correios  
- **Hospedagem:** GitHub + servidor  

---

## Project Model Canvas


## Requisitos

### Requisitos Funcionais

| ID     | Descrição do Requisito | Prioridade |
|--------|------------------------|------------|
| RF-001 | Permitir que o administrador cadastre, edite e exclua produtos. | ALTA |
| RF-002 | Permitir que o administrador controle o estoque (entrada e saída de itens). | ALTA |
| RF-003 | Disponibilizar um catálogo online de produtos para clientes. | ALTA |
| RF-004 | Permitir que clientes realizem pedidos online. | ALTA |
| RF-005 | Exibir apenas produtos disponíveis em estoque no catálogo. | ALTA |
| RF-006 | Permitir cadastro de clientes. | MÉDIA |
| RF-007 | Permitir que clientes acompanhem seus pedidos. | MÉDIA |
| RF-008 | Gerar relatórios de vendas para o administrador. | MÉDIA |

### Requisitos Não Funcionais

| ID      | Descrição do Requisito | Prioridade |
|---------|------------------------|------------|
| RNF-001 | O sistema deve ser responsivo, acessível em computadores e dispositivos móveis. | ALTA |
| RNF-002 | O sistema deve processar requisições do usuário em no máximo 3 segundos. | MÉDIA |
| RNF-003 | O sistema deve garantir segurança no armazenamento de senhas (hash + salt). | ALTA |
| RNF-004 | O sistema deve garantir que o catálogo só exiba produtos disponíveis. | ALTA |
| RNF-005 | O sistema deve utilizar autenticação para separar acessos de administrador e cliente. | ALTA |

---

## Restrições

| ID | Restrição |
|----|-----------|
| 01 | O projeto deverá ser entregue até o final do semestre. |
| 02 | A primeira versão deverá utilizar SQLite, podendo migrar para PostgreSQL em produção. |

---

## Diagrama de Caso de Uso

O diagrama abaixo representa as interações dos atores com o sistema:

![Diagrama de Caso de Uso](/documentos/img/Caso_de_uso_Socina.drawio.png)

---

## Projeto da Base de Dados

O modelo de banco de dados segue o padrão relacional, estruturado para dar suporte ao controle de estoque, catálogo de produtos e pedidos.

### Modelo Entidade-Relacionamento (MER)

Entidades principais:
- **Cliente** (id, nome, email, senha, endereço)  
- **Produto** (id, nome, descrição, preço, quantidade_estoque, categoria)  
- **Pedido** (id, cliente_id, data, status, total)  
- **ItemPedido** (id, pedido_id, produto_id, quantidade, subtotal)  

### Projeto Físico da Base de Dados

**Tabela Cliente**  
- id (PK, inteiro, autoincremento)  
- nome (varchar)  
- email (varchar, único)  
- senha (varchar, hash)  
- endereço (varchar)  

**Tabela Produto**  
- id (PK, inteiro, autoincremento)  
- nome (varchar)  
- descrição (text)  
- preço (decimal)  
- quantidade_estoque (inteiro)  
- categoria (varchar)  

**Tabela Pedido**  
- id (PK, inteiro, autoincremento)  
- cliente_id (FK -> Cliente.id)  
- data (datetime)  
- status (varchar: "em andamento", "concluído", "cancelado")  
- total (decimal)  

**Tabela ItemPedido**  
- id (PK, inteiro, autoincremento)  
- pedido_id (FK -> Pedido.id)  
- produto_id (FK -> Produto.id)  
- quantidade (inteiro)  
- subtotal (decimal)  

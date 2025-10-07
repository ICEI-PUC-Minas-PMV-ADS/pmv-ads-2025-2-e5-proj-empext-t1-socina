# Plano de Testes de Software

Os testes funcionais a serem realizados na aplicação são descritos a seguir.

| **Caso de Teste** | **CT-001-S - Login com credenciais válidas** |
| :--- | :--- |
| **Requisitos Associados** | RNF-005 (Autenticação); RF-001 (Acesso às funções de administrador) |
| **Objetivo do Teste** | Verificar que usuários autorizados conseguem acessar o sistema (admin). |
| **Passos** | 1. Abrir a página de login (127.0.0.1:8000/admin/).<br>2. Inserir usuário: `admin`.<br>3. Inserir senha: senha válida.<br>4. Clicar em "Acessar". |
| **Critérios de êxito** | Redirecionamento para o painel do Django Admin. |
| **Responsável pela elaborar do caso de Teste** | Victor Araújo |

| **Caso de Teste** | **CT-001-I01 - Login com credenciais inválidas** |
| :--- | :--- |
| **Requisitos Associados** | RNF-005 (Autenticação); RNF-003 (Segurança de senhas) |
| **Objetivo do Teste** | Verificar tratamento de erro e bloqueio de acesso com credenciais inválidas. |
| **Passos** | 1. Abrir a página de login.<br>2. Inserir usuário: `admin`.<br>3. Inserir senha: `senha_invalida`.<br>4. Clicar em "Acessar". |
| **Critérios de êxito** | Sistema apresenta mensagem de erro e não permite o acesso. |
| **Responsável pela elaborar do caso de Teste** | Victor Araújo |

| **Caso de Teste** | **CT-002-S - Cadastro de produto (Admin)** |
| :--- | :--- |
| **Requisitos Associados** | RF-001 (CRUD de produtos); RF-002 (Campo quantidade_estoque presente) |
| **Objetivo do Teste** | Verificar criação de produto pelo Admin e persistência dos dados. |
| **Passos** | 1. Logar como admin no Django Admin.<br>2. Acessar *Loja → Produtos → Adicionar Produto*.<br>3. Preencher: Nome, Descrição, Preço, Quantidade estoque, Categoria.<br>4. Salvar. |
| **Critérios de êxito** | Produto salvo com sucesso e aparece na lista de produtos no Admin. |
| **Responsável pela elaborar do caso de Teste** | Victor Araújo |

| **Caso de Teste** | **CT-003-S - Exibição do produto no catálogo público** |
| :--- | :--- |
| **Requisitos Associados** | RF-003 (Catálogo); RF-005 (Mostrar apenas produtos com estoque > 0) |
| **Objetivo do Teste** | Verificar que o produto cadastrado aparece no catálogo público quando em estoque. |
| **Passos** | 1. Abrir a página do catálogo público (ex.: `/catalogo/`).<br>2. Confirmar presença do produto `Camisa teste` e do produto `calça cargo` com preço exibido. |
| **Critérios de êxito** | Produtos com estoque > 0 são exibidos com nome e preço formatado. |
| **Responsável pela elaborar do caso de Teste** | Victor Araújo |
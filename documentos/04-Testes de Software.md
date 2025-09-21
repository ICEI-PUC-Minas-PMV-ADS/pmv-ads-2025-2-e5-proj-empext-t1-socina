# Plano de Testes de Software 

> Documento no padrão PUC: associação de requisitos aos casos de teste e evidências para anexar na entrega da Sprint.

**Pré-requisito:** este plano refere-se **apenas** às funcionalidades desenvolvidas na Etapa 2 (login e cadastro/exibição de produtos).

---

# 1. Resumo — Associação Requisitos × Casos de Teste

| Caso de Teste                           | Código       | Tipo      | Requisitos verificados                                                 | Objetivo                                                                          |
| --------------------------------------- | ------------ | --------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Login com credenciais válidas           | CT-001 - S   | Sucesso   | RNF-005 (Autenticação); RF-001 (Acesso às funções de administrador)    | Verificar que usuários autorizados conseguem acessar o sistema (admin).           |
| Login com credenciais inválidas         | CT-001 - I01 | Insucesso | RNF-005 (Autenticação); RNF-003 (Segurança de senhas)                  | Verificar tratamento de erro e bloqueio de acesso com credenciais inválidas.      |
| Cadastro de produto (Admin)             | CT-002 - S   | Sucesso   | RF-001 (CRUD de produtos); RF-002 (Campo quantidade\_estoque presente) | Verificar criação de produto pelo Admin e persistência dos dados.                 |
| Exibição do produto no catálogo público | CT-003 - S   | Sucesso   | RF-003 (Catálogo); RF-005 (Mostrar apenas produtos com estoque > 0)    | Verificar que o produto cadastrado aparece no catálogo público quando em estoque. |

---

# 2. Casos de Teste (detalhados)

## CT-001 - S — Login com credenciais válidas

* **Descrição:** Verificar autenticação de usuário administrador.
* **Responsável:** Victor Araújo
* **Tipo:** Sucesso
* **Requisitos associados:** RNF-005, RF-001
* **Passos:**

  1. Abrir a página de login (127.0.0.1:8000/admin/).
  2. Inserir usuário: `admin`.
  3. Inserir senha: senha válida.
  4. Clicar em "Acessar".
* **Dados de teste:** usuário `admin` (existente no banco).
* **Critério de êxito:** Redirecionamento para o painel do Django Admin.
* **Evidência:** ![alt text](<img/tela login sucesso.png>) (screenshot do admin após login).

---

## CT-001 - I01 — Login com credenciais inválidas

* **Descrição:** Verificar tratamento quando são fornecidas credenciais inválidas.
* **Responsável:** Victor Araújo
* **Tipo:** Insucesso
* **Requisitos associados:** RNF-005, RNF-003
* **Passos:**

  1. Abrir a página de login.
  2. Inserir usuário: `admin`.
  3. Inserir senha: `senha_invalida`.
  4. Clicar em "Acessar".
* **Dados de teste:** usuário/senha inexistentes.
* **Critério de êxito:** Sistema apresenta mensagem de erro e não permite o acesso.
* **Evidência:** ![alt text](<img/tela login sem sucesso.png>) (screenshot da tentativa de login com erro).

---

## CT-002 - S — Cadastro de Produto (Admin)

* **Descrição:** Validar cadastro de produto via Django Admin.
* **Responsável:** Victor Araújo
* **Tipo:** Sucesso
* **Requisitos associados:** RF-001, RF-002
* **Passos:**

  1. Logar como admin no Django Admin.
  2. Acessar *Loja → Produtos → Adicionar Produto*.
  3. Preencher: Nome, Descrição, Preço, Quantidade estoque, Categoria.
  4. Salvar.
* **Dados de teste:** Nome: `Camisa teste`; Preço: `15.00`; Quantidade: `13`; Categoria: `camisa`.
* **Critério de êxito:** Produto salvo com sucesso e aparece na lista de produtos no Admin.
* **Evidências:**

  * ![alt text](<img/adição de produto.png>) (formulário de adicionar produto com campos preenchidos).
  * ![alt text](<img/adição de produto adição.png>)(mensagem de sucesso: produto adicionado).

---

## CT-003 - S — Exibição do produto no catálogo público

* **Descrição:** Verificar que o produto cadastrado aparece no catálogo público.
* **Responsável:** Victor Araújo
* **Tipo:** Sucesso
* **Requisitos associados:** RF-003, RF-005
* **Passos:**

  1. Abrir a página do catálogo público (ex.: `/catalogo/`).
  2. Confirmar presença do produto `Camisa teste` e do produto `calça cargo` com preço exibido.
* **Dados de teste:** catálogo da aplicação com produtos cadastrados.
* **Critério de êxito:** Produtos com estoque > 0 são exibidos com nome e preço formatado.
* **Evidência:** ![alt text](<img/catalogo após atualização de adição do produto dinamico.png>) (catálogo com os produtos listados).

---

# 3. Testes por Pares (Peer Testing)

* **Objetivo:** outro membro da equipe reexecuta os mesmos CT criados pelo desenvolvedor e registra suas observações.

### Exemplo de preenchimento (peer test)

* **Caso testado:** CT-002 — Cadastro de Produto
* **Responsável (desenvolvedor):** \[Seu Nome]
* **Tester (par):** \[Nome do colega]
* **Data:** 21/09/2025
* **Resultado:** Produto cadastrado com sucesso; observação: validar obrigatoriedade do campo `categoria`.
* **Evidência Peer:** `14362085-3600-441a-a3d3-30b3833d03de.png` (lista de produtos) e `1872cedc-4f60-455d-a924-15f3dfd5b21c.png` (formulário).

---

# 4. Instruções para anexar ao repositório e gerar o documento final

1. Copie este arquivo para `documentacao/plano_de_testes_etapa2.md`.
2. Crie a pasta `documentacao/evidencias/` e coloque aqui todos os PNGs enviados (renomeie se desejar).
3. Atualize os nomes dos arquivos nas seções de Evidências, se renomear.
4. Gere PDF / .docx (VS Code: usar extensão Markdown PDF ou exportar pelo editor).

---

# 5. Controle de Versões

* **Versão:** 1.0
* **Autor:** Victor Araújo
* **Data:** 21/09/2025

---


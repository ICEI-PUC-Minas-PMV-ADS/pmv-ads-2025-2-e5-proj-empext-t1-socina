# Implantação do Software

1. Documentação de Implantação
Planejamento da Implantação
A implantação da aplicação Socina - Natural Beauty foi realizada utilizando uma arquitetura em nuvem (PaaS - Platform as a Service), visando escalabilidade, facilidade de manutenção e integração contínua.

Tecnologias Utilizadas:

Hospedagem (Cloud): Render (plataforma de nuvem para hospedagem de aplicações web).

Linguagem/Framework: Python 3.x com Django Framework.

Servidor de Aplicação: Gunicorn (para servir a aplicação WSGI em produção).

Gerenciamento de Arquivos Estáticos: WhiteNoise (para servir arquivos CSS/JS/Imagens diretamente da aplicação Django sem necessidade de servidor dedicado).

Banco de Dados: SQLite (ambiente de desenvolvimento/MVP) / PostgreSQL (recomendado para produção final).

Controle de Versão: Git e GitHub.

Processo de Implantação (Pipeline):

Versionamento: O código-fonte final foi commitado e enviado (push) para o repositório principal no GitHub.

Integração Contínua (CI/CD): A plataforma Render foi conectada ao repositório do GitHub. Configutou-se o deploy automático, ou seja, a cada nova atualização na branch main, o Render inicia um novo processo de build.

Build e Dependências: Durante o deploy, o servidor executa a instalação das bibliotecas listadas no arquivo requirements.txt.

Configuração de Ambiente: Foram configuradas as variáveis de ambiente sensíveis (Environment Variables) no painel do Render, como SECRET_KEY, DEBUG=False e ALLOWED_HOSTS.

Execução: O comando de inicialização definido foi o gunicorn loja_socina.wsgi:application, colocando o site no ar.

Link da Aplicação em Produção
O projeto encontra-se implantado e acessível publicamente através da URL:

🔗 https://socina.onrender.com

Planejamento de Evolução da Aplicação
Para as próximas etapas do ciclo de vida do software, visando transformar o MVP (Produto Viável Mínimo) em um produto comercial robusto, o planejamento de evolução inclui:

Integração com Gateway de Pagamento:

Substituir o fechamento via WhatsApp por uma integração direta com APIs de pagamento (ex: Stripe, Mercado Pago ou Pagar.me), permitindo transações automáticas via Cartão de Crédito e Pix com baixa automática de estoque.

Área do Cliente (Minha Conta):

Desenvolver um painel para o usuário logado visualizar histórico de pedidos, status de entrega e salvar múltiplos endereços de entrega.

Gestão de Estoque Avançada:

Implementar alertas automáticos para o administrador quando o estoque de um produto atingir níveis críticos.

Sistema de Avaliações:

Permitir que clientes que compraram produtos deixem comentários e avaliações (estrelas) nas páginas de detalhe.

Migração de Banco de Dados:

Migrar definitivamente do SQLite para PostgreSQL para garantir maior integridade de dados e performance com múltiplos acessos simultâneos.
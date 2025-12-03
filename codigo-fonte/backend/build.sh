#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar as dependências
# (Ajuste o caminho se o requirements.txt estiver dentro de backend)
pip install -r codigo-fonte/backend/requirements.txt

# 2. Entrar na pasta onde está o manage.py
cd codigo-fonte/backend

# 3. Coletar os arquivos estáticos (CSS/Imagens)
python manage.py collectstatic --noinput

# 4. Criar/Atualizar as tabelas do banco
python manage.py migrate
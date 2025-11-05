#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Coleta os arquivos estáticos (CSS, JS, etc.)
python manage.py collectstatic --no-input

# Roda as migrações do banco de dados
python manage.py migrate
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# Roda as migrações do banco de dados
python manage.py migrate

# --- NOVO CÓDIGO AQUI ---
# Cria o superusuário lendo as variáveis de ambiente que você acabou de criar.
# O '|| true' no final é um truque para o build não falhar se o usuário já existir.
python manage.py createsuperuser --noinput || true
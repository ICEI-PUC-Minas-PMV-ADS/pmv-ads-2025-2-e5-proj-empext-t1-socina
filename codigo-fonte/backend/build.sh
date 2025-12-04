#!/usr/bin/env bash
# sai do script se der erro
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Coleta os arquivos estáticos (CSS/Imagens)
python manage.py collectstatic --no-input

# Aplica as migrações no banco de dados
python manage.py migrate

# --- A MÁGICA ACONTECE AQUI ---
# Roda o script que cria o usuário admin automaticamente
python criar_superusuario.py
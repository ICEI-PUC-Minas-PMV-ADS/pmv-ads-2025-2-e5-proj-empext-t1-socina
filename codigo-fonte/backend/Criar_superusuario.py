import os
import django

# Configura o ambiente do Django
# TROQUE 'setup.settings' PELO NOME DA PASTA DO SEU PROJETO ONDE FICA O SETTINGS
# Exemplo: se sua pasta principal chama 'loja', coloque 'loja.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings") 
django.setup()

from django.contrib.auth.models import User

def criar_usuario():
    # Defina aqui o usuário e senha que você quer
    USERNAME = 'socina'
    EMAIL = 'socina@socina.com'
    PASSWORD = 'socina@2025' # Troque por uma senha forte depois

    if User.objects.filter(username=USERNAME).exists():
        print(f"O usuário '{USERNAME}' já existe. Nenhuma ação necessária.")
    else:
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"Superusuário '{USERNAME}' criado com sucesso!")

if __name__ == "__main__":
    criar_usuario()
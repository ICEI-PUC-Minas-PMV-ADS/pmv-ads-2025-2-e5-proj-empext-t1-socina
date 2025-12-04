import os
import django

# --- CONFIGURAÇÃO EXATA BASEADA NO SEU CAMINHO ---
# Como o settings.py está dentro da pasta 'loja', o caminho é este:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loja.settings")

try:
    django.setup()
except Exception as e:
    print(f"ERRO CRÍTICO AO CONFIGURAR DJANGO: {e}")
    exit(1)

from django.contrib.auth.models import User

def criar_superusuario_automatico():
    USERNAME = 'admin'
    EMAIL = 'admin@socina.com'
    PASSWORD = 'admin' 

    print("--> Iniciando verificação de superusuário...")

    try:
        if User.objects.filter(username=USERNAME).exists():
            user = User.objects.get(username=USERNAME)
            user.set_password(PASSWORD)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"--> SUCESSO! Usuário '{USERNAME}' já existia. Senha resetada para '{PASSWORD}'.")
        else:
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            print(f"--> SUCESSO! Usuário '{USERNAME}' criado do zero. Senha: {PASSWORD}")
    except Exception as e:
        print(f"--> ERRO NO BANCO DE DADOS: {e}")

if __name__ == "__main__":
    criar_superusuario_automatico()
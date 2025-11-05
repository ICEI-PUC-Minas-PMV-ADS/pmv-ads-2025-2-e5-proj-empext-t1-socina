from pathlib import Path
import os
import dj_database_url  # NOVO: Importa o helper do banco de dados

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# CHAVE SECRETA (ALTERADO)
# Vamos ler a chave do ambiente do Render. É mais seguro.
SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_padrao_insegura_para_testes_locais')

# MODO DEBUG (ALTERADO)
# Render vai definir DEBUG = False. Localmente, será False a menos que você defina DEBUG=True.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# DOMÍNIOS PERMITIDOS (ALTERADO)
# O Render vai te dar um domínio .onrender.com.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # NOVO: Whitenoise para servir arquivos estáticos
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.staticfiles',
    'loja',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # NOVO: Whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loja.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'loja/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'loja.wsgi.application'

# BANCO DE DADOS (ALTERADO)
# O Render vai fornecer uma DATABASE_URL. Se não encontrar, usa o sqlite3.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ARQUIVOS ESTÁTICOS (ALTERADO)
# Onde o Django vai procurar seus assets (css, js, imagens)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent, 'frontend/assets'), # Caminho para sua pasta assets
]
# Onde o Render vai COLETAR todos os arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# NOVO: Armazenamento para o Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ARQUIVOS DE MÍDIA (Fotos dos produtos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CHAVE DO MERCADO PAGO (Vamos ler do ambiente)
MERCADO_PAGO_ACCESS_TOKEN = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN', 'SUA_CHAVE_DE_TESTE_AQUI')
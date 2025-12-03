from pathlib import Path
import os
import dj_database_url

# --- CAMINHOS ---
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
# Em produção (Render), a chave vem das variáveis de ambiente. Localmente usa a fake.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-padrao-para-desenvolvimento-local')

# DEBUG:
# No Render, defina a variável de ambiente DEBUG = True para ver os erros.
# Se não estiver definido, assume False (Produção).
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    '.onrender.com' # Aceita qualquer subdomínio do Render
]

# Adiciona o host externo do Render se existir
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# --- APPS INSTALADOS ---
INSTALLED_APPS = [
    'jazzmin',  # <--- OBRIGATÓRIO: Deve ser o primeiro da lista
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seus Apps
    'loja',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- Essencial para estáticos no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loja.urls'

# --- TEMPLATES (HTML) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Garante que o Django ache a pasta templates dentro da pasta loja
            os.path.join(BASE_DIR, 'loja', 'templates'),
        ],
        'APP_DIRS': True, # Procura templates dentro de cada app instalado
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


# --- BANCO DE DADOS ---
# Tenta pegar do Render (DATABASE_URL). Se não tiver, usa SQLite local.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# --- VALIDAÇÃO DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CSS, JS, IMAGES) ---
STATIC_URL = '/static/'

# Onde o Django coleta os arquivos no deploy (Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Onde estão os arquivos estáticos do seu projeto (Desenvolvimento)
STATICFILES_DIRS = [
    # Ajuste este caminho se sua pasta frontend estiver em outro lugar
    # Aqui assume: raiz/codigo-fonte/frontend/assets
    os.path.join(BASE_DIR.parent, 'frontend', 'assets'),
]

# Configuração do Whitenoise para servir arquivos
# OBS: Usei 'CompressedStaticFilesStorage' que é mais seguro que 'Manifest' para evitar erros 500
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# --- ARQUIVOS DE MÍDIA (Uploads de Produtos) ---
MEDIA_URL = '/media/'
# Salva na pasta media fora do backend
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CONFIGURAÇÃO JAZZMIN (Painel Admin) ---
JAZZMIN_SETTINGS = {
    "site_title": "SOCINA Admin",
    "site_header": "SOCINA",
    "site_brand": "SOCINA",
    "welcome_sign": "Painel Gerencial - SOCINA",
    "copyright": "Socina Ltd",
    "search_model": "auth.User",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Loja (Site)", "url": "/", "new_window": True},
    ],
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-pink", 
    "accent": "accent-pink",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "theme": "default", 
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
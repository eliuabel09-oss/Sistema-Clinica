# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------
# SEGURIDAD
# ----------------------------------------------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-cambia-esto')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').strip() == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ----------------------------------------------------------------
# APLICACIONES
# ----------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del sistema
    'apps.pacientes',
    'apps.citas',
    'apps.consultas',
    'apps.core',   

    # Librerías extras
    'widget_tweaks',
    
]

# ----------------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ----------------------------------------------------------------
# TEMPLATES
# ----------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ----------------------------------------------------------------
# BASE DE DATOS — MySQL
# ----------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     os.getenv('DB_NAME',     'clinica_db'),
        'USER':     os.getenv('DB_USER',     'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST':     os.getenv('DB_HOST',     '127.0.0.1'),
        'PORT':     os.getenv('DB_PORT',     '3306').strip(),
        'OPTIONS': {
            'charset':      'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 60,
    }
}

# ----------------------------------------------------------------
# CONTRASEÑAS
# ----------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------------------
# INTERNACIONALIZACIÓN
# ----------------------------------------------------------------
LANGUAGE_CODE = 'es-pe'
TIME_ZONE     = 'America/Lima'
USE_I18N      = True
USE_TZ        = True

# ----------------------------------------------------------------
# ARCHIVOS ESTÁTICOS Y MEDIA
# ----------------------------------------------------------------
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------------------
# OTROS
# 
# Auth
LOGIN_URL           = '/login/'
LOGIN_REDIRECT_URL  = '/'
LOGOUT_REDIRECT_URL = '/login/'


ALLOWED_HOSTS = ['*']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
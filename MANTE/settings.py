"""
Django settings for MANTE project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ===== Path base =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Cargar variables de entorno =====
load_dotenv(BASE_DIR / '.env')

# ===== Seguridad =====
SECRET_KEY = os.getenv('SECRET_KEY', 'inseguro-default')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ALLOWED_HOSTS debe ser lista
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ===== Aplicaciones =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps Me
    'apps.users',
    'apps.core',
    'apps.dashboard',
    'apps.mantenimiento',
    'apps.equipo', 
    'apps.lugar',
    
]



# ===== Middleware =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MANTE.urls'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===== Templates =====
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'MANTE.wsgi.application'

# ===== Base de Datos (SQL Server) =====

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'OPTIONS': {
            'driver': os.getenv("DB_DRIVER"),
            'trusted_connection': 'yes' if os.getenv("DB_USER","") == "" else 'no',
        },
    }
}





# ===== Custom User =====
AUTH_USER_MODEL = 'users.UsersCustomUser'
# ===== Password Validators =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ===== Internacionalización =====
LANGUAGE_CODE = 'es-bo'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_L10N = True
USE_TZ = False 
# ===== Static =====
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# ===== Auto Field =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
    Django settings for boox project.
    Generated by 'django-admin startproject' using Django 4.0.3.
    For more information on this file, see
    https://docs.djangoproject.com/en/4.0/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.0/ref/settings/

"""
from pathlib import Path
import environ


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

APPS_DIR = ROOT_DIR
env = environ.Env()
env.read_env(str(ROOT_DIR / ".env"))


ENV = env("ENV")
DEBUG = env.bool("DJANGO_DEBUG", False)
LOCAL = env.bool("DJANGO_LOCAL", False)
SECRET_KEY = env("DJANGO_SECRET_KEY")
IS_PRODUCTION = ENV == "PRODUCTION"

USE_TZ = True
TIME_ZONE = "Africa/Algiers"

ALLOWED_HOSTS = ["*"]

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'boox_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = "boox_app.User"

ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "3306",
        "ATOMIC_REQUESTS": True,
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        "TEST": {"CHARSET": "utf8", "COLLATION": "utf8_general_ci",},
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

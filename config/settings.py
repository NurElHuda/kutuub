"""
    Django settings for boox project.
    Generated by 'django-admin startproject' using Django 4.0.3.
    For more information on this file, see
    https://docs.djangoproject.com/en/4.0/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.0/ref/settings/

"""
import os
from pathlib import Path

import environ
import firebase_admin

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

APPS_DIR = ROOT_DIR
BASE_DIR = os.path.join(ROOT_DIR, "boox_app")

env = environ.Env()

ENV_FILE_PATH = f"{ROOT_DIR}/.env"
if os.path.isfile(ENV_FILE_PATH):
    env.read_env(f"{ROOT_DIR}/.env")
    

ENV = env("ENV")
DEBUG = env.bool("DJANGO_DEBUG", False)
LOCAL = env.bool("DJANGO_LOCAL", False)
SECRET_KEY = env("DJANGO_SECRET_KEY")
IS_PRODUCTION = ENV == "PRODUCTION"
BASE_URL=env("BASE_URL")

USE_TZ = True
TIME_ZONE = "Africa/Algiers"

ALLOWED_HOSTS = ["*"]

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "corsheaders",
    "whitenoise.runserver_nostatic",  
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "django_extensions",
    "boox_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "boox_app.User"

AUTHENTICATION_BACKENDS = [
    "boox_app.middlewares.CustomAuthBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "sign-in"
LOGOUT_REDIRECT_URL = "sign-out"


ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
os.environ.get("DATABASE_URL")
if env("HOST", default="LOCAL") == "DO":
    DATABASES = {
        'default': os.environ.get("DATABASE_URL")
    }
else:
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
            "TEST": {
                "CHARSET": "utf8",
                "COLLATION": "utf8_general_ci",
            },
        }
    }

STATIC_ROOT = "static"
STATIC_URL = "static/"


MEDIA_ROOT = f"{ROOT_DIR}/media"
MEDIA_URL = "/media/"
BOOK_COVERS_PATH = os.path.join(MEDIA_ROOT, "book_covers")
BOOK_COVERS_URL = f"{MEDIA_URL}book_covers"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    ROOT_DIR, "config", "boox-e1a40-firebase-adminsdk.json"
)
firebase_admin.initialize_app()

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "kawarir_app.paginators.CustomPagination",
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
}

CORS_ALLOW_ALL_ORIGINS = True
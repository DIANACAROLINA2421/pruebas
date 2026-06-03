"""
Django settings for BacketMpforall project.
Configurado para despliegue en Render.
"""

from pathlib import Path
from decouple import config
import dj_database_url

# 📁 Directorio base
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Clave secreta y modo debug
SECRET_KEY = config("SECRET_KEY", "")
DEBUG = config("DEBUG", default=False, cast=bool)

if SECRET_KEY == "":
    raise KeyError("SECRET_KEY cannot be empty")

# 🌐 Hosts y seguridad
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://127.0.0.1:8000"
).split(",")

# 🔗 Variables externas (API LOBEES)
LOBEES_URL = config("LOBEES_URL", default="")
LOBEES_TOKEN = config("LOBEES_TOKEN", default="")

# 📦 Aplicaciones instaladas
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "call_api",
    "rest_framework",
    "rest_framework.authtoken",
]

# ⚙️ Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 🌍 Configuración de URLs y WSGI
ROOT_URLCONF = "BacketMpforall.urls"

# 🧩 Configuración de plantillas
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "BacketMpforall.wsgi.application"

# 🗄️ Base de datos — PostgreSQL en Render, SQLite en local
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# 🔐 Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 🌎 Internacionalización
LANGUAGE_CODE = "es-ES"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# 📂 Archivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🔓 CORS
CORS_ALLOW_ALL_ORIGINS = True

# ⚙️ Configuración de Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
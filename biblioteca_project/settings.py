from pathlib import Path
from datetime import timedelta 
import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-itx_s8ff9p##yy_cb(at0f00sjkmv7#9t@gkvl7f3x!72)-cxe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'daphne',  # ← AGREGAR
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_simplejwt',
    'oauth2_provider',
    'allauth',  # ← AGREGAR
    'allauth.account',  # ← AGREGAR
    'allauth.socialaccount',  # ← AGREGAR
    'allauth.socialaccount.providers.google',  # ← AGREGAR
    
    # Tu aplicación
    'libros',

    'channels',  # ← AGREGAR para WebSockets
    'graphene_django',  # ← AGREGAR para GraphQL
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'libros.middleware.SecurityMiddleware',
    'libros.middleware.RateLimitMiddleware',
]

ROOT_URLCONF = 'biblioteca_project.urls'

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

WSGI_APPLICATION = 'biblioteca_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'biblioteca_uni4',
        'USER': 'root',
        'PASSWORD': '2026L#un',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Hermosillo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# CONFIGURACIÓN DE CORS
# ==============================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True


# ==============================
# CONFIGURACIÓN DE REST FRAMEWORK
# ==============================
REST_FRAMEWORK = {
    # AUTENTICACIÓN: Qué métodos acepta tu API
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT (Token moderno)
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # ← AGREGAR para OAuth 2.0
        'rest_framework.authentication.TokenAuthentication',          # Token tradicional
        'rest_framework.authentication.SessionAuthentication',      # Sesión (para admin)
        'DEFAULT_THROTTLE_CLASSES': [
        'libros.throttles.BurstRateThrottle',
        'libros.throttles.SustainedRateThrottle',
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',        # 60 por minuto
        'sustained': '1000/day',  # 1000 por día
        'anon_burst': '20/min',   # Anónimos: 20 por minuto
        'premium': '10000/day',   # Premium: 10000 por día
    }  
    ],
    
    # PERMISOS: Qué pueden hacer los usuarios
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # PAGINACIÓN: Cuántos resultados por página
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # FILTROS: Permitir búsquedas y ordenamiento
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# =======================
# SIMPLE JWT CONFIG
# =======================

SIMPLE_JWT = {
    # ⏱️ DURACIÓN DE TOKENS
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),    # Token de acceso válido 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Token de refresco válido 7 días
    
    # 🔄 ROTACIÓN DE TOKENS (Seguridad extra)
    'ROTATE_REFRESH_TOKENS': True,                  # Genera nuevo refresh al refrescar
    'BLACKLIST_AFTER_ROTATION': True,               # Invalida el refresh anterior
    'UPDATE_LAST_LOGIN': True,                      # Actualiza last_login del usuario
    
    # 🔐 ALGORITMO Y CLAVE DE FIRMA
    'ALGORITHM': 'HS256',                           # HMAC SHA-256 (más común)
    'SIGNING_KEY': SECRET_KEY,                      # Usa la SECRET_KEY de Django
    'VERIFYING_KEY': None,                          # Solo para algoritmos asimétricos (RSA)
    
    # 📋 CONFIGURACIÓN DE HEADERS
    'AUTH_HEADER_TYPES': ('Bearer',),               # Tipo: "Authorization: Bearer TOKEN"
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',       # Nombre del header
    
    # 👤 CLAIMS DEL USUARIO
    'USER_ID_FIELD': 'id',                          # Campo del modelo User para ID
    'USER_ID_CLAIM': 'user_id',                     # Nombre del claim en el payload
    
    # 🎫 CONFIGURACIÓN DEL TOKEN
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',               # Claim que identifica tipo de token
    'JTI_CLAIM': 'jti',                             # JWT ID (identificador único)
}

# =======================
# SITE CONFIGURATION
# =======================
SITE_ID = 1  # ← AGREGAR

# =======================
# AUTHENTICATION BACKENDS
# =======================
AUTHENTICATION_BACKENDS = [
    # Backend por defecto de Django (username/password)
    'django.contrib.auth.backends.ModelBackend',
    
    # Backend de allauth para OAuth social
    'allauth.account.auth_backends.AuthenticationBackend',
]

# =======================
# DJANGO ALLAUTH CONFIG
# =======================

# Configuración de cuentas
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Solo email para login social
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Para desarrollo: 'mandatory' en producción

# Configuración de login social
SOCIALACCOUNT_AUTO_SIGNUP = True  # Crear usuario automáticamente
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # No verificar email en OAuth

# Proveedores OAuth configurados
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': getattr(settings, 'GOOGLE_CLIENT_ID'),
            'secret': getattr(settings, 'GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# =======================
# OAUTH 2.0 PROVIDER SETTINGS
# =======================
# Configuración para django-oauth-toolkit
OAUTH2_PROVIDER = {
    # Tiempo de vida de los tokens
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 hora
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 7,  # 7 días

    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 hora
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,  # 1 día
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,  # 10 minutos
    'ROTATE_REFRESH_TOKEN': True,
    
    # Scopes disponibles
    'SCOPES': {
        'read': 'Acceso de lectura',
        'write': 'Acceso de escritura',
        'groups': 'Access to groups - Acceso a grupos de usuario',
    },
    
    # Tipo de token por defecto
    'ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
    
}

ACCOUNT_EMAIL_MAX_LENGTH = 190

ASGI_APPLICATION = 'biblioteca_project.asgi.application'

# Channel Layers - Opción 1: Con Redis (RECOMENDADO para producción)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# GraphQL Settings
GRAPHENE = {
    'SCHEMA': 'libros.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ],
}

# Solo para PRODUCCIÓN (no desarrollo)
if not DEBUG:
    # Forzar HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Headers de seguridad
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Proxy SSL headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Orígenes permitidos para CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tudominio.com",
    "https://www.tudominio.com",
]

# Permitir credenciales
CORS_ALLOW_CREDENTIALS = True

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Orígenes confiables para CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]

# Cookie CSRF segura en producción
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'
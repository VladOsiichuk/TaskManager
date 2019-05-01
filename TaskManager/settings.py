"""
Django settings for TaskManager project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_heroku
import redis
from redis import Redis
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p%z_0!2_zk$hrx@+!m+&zyb@sz*^uo@xb=gb)kl%vf7!qr403g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = DEBUG
PORT = os.environ.get('PORT')
url = "127.0.0.1:" + "10000"
print(url)
DOMAIN_FRONT = "protected-mountain-24825.herokuapp.com"
CSRF_COOKIE_DOMAIN = DOMAIN_FRONT
SESSION_COOKIE_DOMAIN = DOMAIN_FRONT
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_HTTPONLY = False

#CSRF_TRUSTED_ORIGINS = [DOMAIN_FRONT]


ALLOWED_HOSTS = (
    "*",
    "127.0.0.1",
    DOMAIN_FRONT
)


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    "*",
    "127.0.0.1",
    DOMAIN_FRONT
)

CORS_ALLOW_HEADERS = (
  'accept',
  'cors',
  'accept-encoding',
  'authorization',
  'content-type',
  'dnt',
  'origin',
  'sessionid',
  'user-agent',
  'x-csrftoken',
  "csrftoken",
  'x-requested-with',
)

CORS_ALLOW_METHODS = (
  'DELETE',
  'GET',
  'OPTIONS',
  'PATCH',
  'POST',
  'PUT',
)


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user_auth.apps.UserConfig',
    'desk.apps.DeskConfig',
    'api_rules.apps.RulesConfig',
    'debug_toolbar'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'querycount.middleware.QueryCountMiddleware',
    'middleware.PermissionCache.PermissionCacheMiddleware',
]

ROOT_URLCONF = 'TaskManager.urls'

QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG':0,
        'MIN_QUERY_COUNT_TO_LOG':0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

DEBUG_SQL = True

WSGI_APPLICATION = 'TaskManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "user_auth.User"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ()

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = "/media/"

CACHE_TTL = 3
REDIS_URL = 'redis://h:p2d702b5c7911598eac4db7013d7d9d4d8e750b065f0b2db0b472457152085599@ec2-34-193-212-83.compute-1.amazonaws.com:15289'
r = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
print(type(r))
# development url redis = redis://127.0.0.1:6379/1
# redis_url = os.getenv('REDISTOGO_URL')

# urlparse.uses_netloc.append('redis')
# url = urlparse.urlparse(redis_url)
# conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://h:p2d702b5c7911598eac4db7013d7d9d4d8e750b065f0b2db0b472457152085599@ec2-34-193-212-83.compute-1.amazonaws.com:15289",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "PASSWORD": "mysecret"
#         }
#         # "CONFIG": {
#         #     "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
#         # },
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://h:p2d702b5c7911598eac4db7013d7d9d4d8e750b065f0b2db0b472457152085599@ec2-34-193-212-83.compute-1.amazonaws.com:15289",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
    ]
SHOW_TOOLBAR_CALLBACK = True

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', "evening-inlet-45238.herokuapp.com")
django_heroku.settings(locals())
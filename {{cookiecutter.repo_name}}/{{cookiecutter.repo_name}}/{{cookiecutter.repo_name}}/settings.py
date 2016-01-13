from __future__ import absolute_import
"""
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

Format look strange?  We're using class based settings and ENV variables
Checkout this project: https://github.com/jezdez/django-configurations

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Make everything in apps/ appear as if at project root
APPS_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, APPS_ROOT)


class BaseSettings(Configuration):

    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = '{{cookiecutter.repo_name}}.urls'
    WSGI_APPLICATION = '{{cookiecutter.repo_name}}.wsgi.application'

    # In production use values.SecretValue()
    SECRET_KEY = 'CHANGEME!!NOW!!PLEASE!!'

    ADMINS = (
        ("Nam Ngo", "nam@kogan.com.au"),
    )
    MANAGERS = ADMINS

    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DATABASE_NAME', '{{cookiecutter.repo_name}}_db'),
            'USER': os.environ.get('DATABASE_USER', ''),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': '5432',
            'CONN_MAX_AGE': 300,
        }
    }

    REDIS_CACHE_URL = os.environ.get('REDIS_CACHE_URL', 'localhost:6379:1')
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': REDIS_CACHE_URL,
            'TIMEOUT': 0,
        }
    }

    BROKER_URL = values.Value(
        "redis://localhost:6379/2", environ_prefix="{{cookiecutter.repo_name}}".upper()
    )
    CELERY_RESULT_BACKEND = values.Value(
        "redis://localhost:6379/3", environ_prefix="{{cookiecutter.repo_name}}".upper()
    )
    CELERYBEAT_SCHEDULE = {
    }

    # Celery settings
    CELERY_REDIS_MAX_CONNECTIONS = 256
    CELERYD_MAX_TASKS_PER_CHILD = 100
    CELERY_SEND_TASK_ERROR_EMAILS = True

    ### Internationalization
    LANGUAGE_CODE = 'en-Au'
    TIME_ZONE = 'Australia/Melbourne'
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True

    ### Template Configuration
    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    ### Static files (CSS, JavaScript, Images)
    STATIC_ROOT = os.path.join(
        PROJECT_ROOT, '{{static_root}}'
    )
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    ### Media Configuration    
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, '{{static_root}}/media')
    MEDIA_URL = '/media/'

    ### Logging Configuration
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            },
            # Warning messages are sent to admin emails
            'mail_admins': {
                'level': 'WARNING',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
            },
            # Send all messages to console
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            # Sentry handler
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            }
        },
        'loggers': {
            # Catch all
            '': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }

    # Site Domain
    DOMAIN_NAME = values.Value('{{cookiecutter.repo_name}}.local', environ_prefix="{{cookiecutter.repo_name}}".upper())
    ALLOWED_HOSTS = ['*']


class Local(BaseSettings):

    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value(
        'django.core.mail.backends.console.EmailBackend'
    )

    BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6379/1")
    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }


class Production(BaseSettings):

    DEBUG = values.BooleanValue(False)
    ALLOWED_HOSTS = values.ListValue(
        ['*'], environ_prefix="{{cookiecutter.repo_name}}".upper()
    )
    SECRET_KEY = values.SecretValue(environ_prefix="{{cookiecutter.repo_name}}".upper())
    DATABASES = values.DatabaseURLValue(
        'sqlite://dev.db', alias='default',
        environ_prefix="{{cookiecutter.repo_name}}".upper()
    )
    CACHES = values.CacheURLValue(
        'locmem://', alias='default', environ_prefix="{{cookiecutter.repo_name}}".upper()
    )

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
    TEMPLATE_LOADERS = (
        #'django.template.loaders.cached.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

    # GetSentry
    # RAVEN_CONFIG = {
    #     'dsn': 'https://70559c16f64f4c4f98b1c97ec417f6d9:3c16ca31307641fa884c55c1382f62b5@app.getsentry.com/52722',
    # }

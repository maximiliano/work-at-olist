"""
Django settings for calldetails project.

"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['CD_SECRET_KEY']

# By default debug is turned off, unless defined in environment variable.
# WARNING: Don't turn on in Production!
DEBUG = os.environ.get('CD_DEBUG') == 'true'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
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

ROOT_URLCONF = 'calldetails.urls'

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

WSGI_APPLICATION = 'calldetails.wsgi.application'


# Database
db_engine = os.environ.get('CD_DB_ENGINE')

if not db_engine or (db_engine == 'sqlite3'):
    db_config = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
else:
    db_config = {
        'ENGINE': 'django.db.backends.%s' % os.environ.get('CD_DB_ENGINE'),
        'NAME': os.environ.get('CD_DB_NAME'),
        'USER': os.environ.get('CD_DB_USER'),
        'PASSWORD': os.environ.get('CD_DB_PASSWORD'),
        'HOST': os.environ.get('CD_DB_HOST'),
        'PORT': os.environ.get('CD_DB_PORT'),
    }

DATABASES = {
    'default': db_config
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# Settings exclusive for Heroku usage
# This will automatically configure DATABASE_URL, ALLOWED_HOSTS,
# WhiteNoise (for static assets), Logging, and Heroku CI for your application.

django_heroku.settings(locals())

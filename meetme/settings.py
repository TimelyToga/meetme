"""
Django settings for meetme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ENVIRONMENT = os.environ['ENVIRONMENT']
DEBUG = bool(ENVIRONMENT == 'development')
PRODUCTION = bool(ENVIRONMENT == 'production')

WWW_HOST_URL = 'https://www.boutch.com' if PRODUCTION else 'http://localhost:5000'


## BIG DIRECTORIES
WEB_DIR = os.path.abspath(os.path.join(BASE_DIR, 'webfiles'))
TEMPLATE_DIRS = (os.path.abspath(os.path.join(WEB_DIR, 'templates')), )
STATIC_DIR = os.path.abspath(os.path.join(WEB_DIR, 'static'))

## LESSER DIRECTORIES
FAVICON = os.path.abspath(os.path.join(STATIC_DIR, 'favicon.ico'))
JS_DIR = os.path.abspath(os.path.join(STATIC_DIR, 'js'))
CSS_DIR = os.path.abspath(os.path.join(STATIC_DIR, 'css'))
IMG_DIR = os.path.abspath(os.path.join(STATIC_DIR, 'img'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vs8igh73!-vksudtqza(!i+lzxvk$h9redqqpux3u%e^bllbzp'



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'meetme.urls'
WSGI_APPLICATION = 'meetme.wsgi.application'


## SENDGRID
SENDGRID_USERNAME = os.environ['SENDGRID_USERNAME']
SENDGRID_PASSWORD = os.environ['SENDGRID_PASSWORD']


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

MONGODB_URI = os.environ['MONGODB_DEVELOPMENT_URI']
DB_NAME = os.environ['MONGODB_DEVELOPMENT_DB']
MAIN_COLLECTION_NAME = os.environ['MAIN_COLLECTION_NAME']

DATABASES = {
   'default' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : os.environ['MONGODB_DEVELOPMENT_DB'],
      'USERNAME': os.environ['MONGODB_DEVELOPMENT_USER'],
      'PASSWORD': os.environ['MONGODB_DEVELOPMENT_PASSWORD'],
      'HOST': os.environ['MONGODB_DEVELOPMENT_HOST'],
      'PORT': os.environ['MONGODB_DEVELOPMENT_PORT'],
   }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

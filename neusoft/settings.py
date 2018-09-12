"""
Django settings for neusoft project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ojn@!#rv#sxxt=031r987y7p)gxy^lc-#o%9(^9e+teif)a*l+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

ALLOWED_HOSTS = ['*']

# Logging

ADMINS = (
    ('Admins','1510180157@qq.com'),
)
 
#
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS
 
#Email设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.exmail.qq.com'
EMAIL_PORT= 465        
EMAIL_HOST_USER = 'i@zxh326.cn'  
EMAIL_HOST_PASSWORD = 'Zxh326//' 
EMAIL_SUBJECT_PREFIX = 'website' 
EMAIL_USE_SSL = True 
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER 

SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple':{
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'backup':{
            'format': "%(asctime)s %(message)s'"
        }
    },
    'filters': {
        'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
    },
    'handlers': {
        'file':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename': BASE_DIR + '/logs/tmp.log',
            'formatter':'simple'
        },
        'file_backup':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/backup.log',
            'formatter': 'backup'
        },
        'request_info':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'filename':BASE_DIR + '/logs/request.log',
            'formatter':'simple'
        },
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console','request_info'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'app.custom': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'app.backup' :{
            'handlers': ['file_backup'],
            'level': 'INFO'
        }
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecard',
    'course',
    'utils',
    'band'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'neusoft.urls'

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

WSGI_APPLICATION = 'neusoft.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neusoft',
        'USER': 'neusoft',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# Proposed other projects are set to True, 
# this project is for groups so special No need to set
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'

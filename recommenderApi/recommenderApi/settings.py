"""
Django settings for recommenderApi project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from dj_database_url import parse as dburl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
MONGODB_LINK = config('MONGODB_LINK', default='')
MONGODB_UPDATE_TRAINING_TIME = config('MONGODB_UPDATE_TRAINING_TIME', default='')
MONGODB_NAME = config('MONGODB_NAME', default='')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', f'{config("API_HOST", default="")}']
CSRF_TRUSTED_ORIGINS = [f'https://{config("API_HOST", default="")}']

ROUND_NUM_OF_REVIEWS = config('ROUND_NUM_OF_ITEMS', default=20, cast=int)
REMOVE_FROM_SEEN_TABLE_AFTER_DAYS = config('REMOVE_FROM_SEEN_TABLE_AFTER_DAYS', default=5, cast=int)
DAILY_DECREASE_FOR_OLD_TRACKERS = config('DAILY_DECREASE_FOR_OLD_TRACKERS', default=0.1, cast=float)
MIN_LEVEL_OLD_TRACKERS_REACH = config('MIN_LEVEL_OLD_TRACKERS_REACH', default=0.1, cast=float)
EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE = config('EVERY_ITERATION_EPOCHS_AMOUNT_INCREASE', default=50, cast=int)

MIN_ITEM = max([ROUND_NUM_OF_REVIEWS//10, 1])
MAX_PREVIEW = max([7*ROUND_NUM_OF_REVIEWS//10, 7])
MAX_CREVIEW = max([5*ROUND_NUM_OF_REVIEWS//10, 5])
MAX_PQUESTION = max([3*ROUND_NUM_OF_REVIEWS//10, 3])
MAX_CQUESTION = max([3*ROUND_NUM_OF_REVIEWS//10, 3])

# Review Trackers
REVIEW_FULL_SCREEN = config('REVIEW_FULL_SCREEN', default=0.2, cast=float)
REVIEW_LIKE = config('REVIEW_LIKE', default=0.3, cast=float)
REVIEW_UNLIKE = config('REVIEW_UNLIKE', default=-0.3, cast=float)
REVIEW_SEE_MORE = config('REVIEW_SEE_MORE', default=0.1, cast=float)
REVIEW_COMMENT = config('REVIEW_COMMENT', default=0.4, cast=float)
REVIEW_DONT_LIKE = config('REVIEW_DONT_LIKE', default=-1, cast=float)

# Question Trackers
QUESTION_FULL_SCREEN = config('QUESTION_FULL_SCREEN', default=0.25, cast=float)
QUESTION_UPVOTE = config('QUESTION_UPVOTE', default=0.25, cast=float)
QUESTION_DOWNVOTE = config('QUESTION_DOWNVOTE', default=-0.25, cast=float)
QUESTION_ANSWER = config('QUESTION_ANSWER', default=0.33, cast=float)
QUESTION_MY_PRODUCT_PAGE = config('QUESTION_MY_PRODUCT_PAGE', default=0.17, cast=float)
QUESTION_DONT_LIKE = config('QUESTION_DONT_LIKE', default=-1, cast=float)

# Mobile Trackers
MOBILE_PROFILE = config('MOBILE_PROFILE', default=0.3, cast=float)
MOBILE_COMPARE = config('MOBILE_COMPARE', default=0.2, cast=float)
MOBILE_QUESTION = config('MOBILE_QUESTION', default=0.5, cast=float)

# HOUR = config('HOUR', default=19, cast=int)
# MINUTE = config('MINUTE', default=21, cast=int)


# Mobile Specs (76%)
SPECS_PRICE = config('SPECS_PRICE', default=15, cast=int)
SPECS_RELEASE_DATE = config('SPECS_RELEASE_DATE', default=9, cast=int)
SPECS_COMPANY = config('SPECS_COMPANY', default=9, cast=int)
SPECS_DIMENSIONS = config('SPECS_DIMENSIONS', default=4, cast=int)
SPECS_BATTERY_CAPACITY = config('SPECS_BATTERY_CAPACITY', default=4, cast=int)
SPECS_OS = config('SPECS_OS', default=4, cast=int)
SPECS_WEIGHT = config('SPECS_WEIGHT', default=2, cast=int)
SPECS_HAS_FAST_CHARGING = config('SPECS_HAS_FAST_CHARGING', default=2, cast=int)
SPECS_SCREEN_TYPE = config('SPECS_SCREEN_TYPE', default=2, cast=int)
SPECS_SCREEN_SIZE = config('SPECS_SCREEN_SIZE', default=2, cast=int)
SPECS_SCREEN_2BODY_RATIO = config('SPECS_SCREEN_2BODY_RATIO', default=2, cast=int)
SPECS_SCREEN_RESOLUTION = config('SPECS_SCREEN_RESOLUTION', default=2, cast=int)
SPECS_RESOLUTION_DENSITY = config('SPECS_RESOLUTION_DENSITY', default=2, cast=int)
SPECS_INT_MEM = config('SPECS_INT_MEM', default=5, cast=int)
SPECS_MAIN_CAM = config('SPECS_MAIN_CAM', default=4, cast=int)
SPECS_SELFIE_CAM = config('SPECS_SELFIE_CAM', default=2, cast=int)
SPECS_HAS_LOUDSPEAKER = config('SPECS_HAS_LOUDSPEAKER', default=1, cast=int)
SPECS_HAS_STEREO = config('SPECS_HAS_STEREO', default=1, cast=int)
SPECS_HAS_3P5MM = config('SPECS_HAS_3P5MM', default=1, cast=int)
SPECS_HAS_NFC = config('SPECS_HAS_NFC', default=1, cast=int)
SPECS_HAS_GYRO = config('SPECS_HAS_GYRO', default=1, cast=int)
SPECS_HAS_PROXIMITY = config('SPECS_HAS_PROXIMITY', default=1, cast=int)
SPECS_NETWORK = config('SPECS_NETWORK', default=1, cast=int)
SPECS_BLUETOOTH_VERSION = config('SPECS_BLUETOOTH_VERSION', default=1, cast=int)
SPECS_USB_TYPE = config('SPECS_USB_TYPE', default=1, cast=int)
SPECS_USB_VERSION = config('SPECS_USB_VERSION', default=1, cast=int)
SPECS_CPU = config('SPECS_CPU', default=4, cast=int)
SPECS_GPU = config('SPECS_GPU', default=2, cast=int)

# Factor for decreasing values
SPECS_COMPANY_DECREASE_FACTOR = config('SPECS_COMPANY_DECREASE_FACTOR', default=2, cast=float)
SPECS_CPU_DECREASE_FACTOR = config('SPECS_CPU_DECREASE_FACTOR', default=1, cast=float)
SPECS_GPU_DECREASE_FACTOR = config('SPECS_GPU_DECREASE_FACTOR', default=1, cast=float)
SPECS_OS_DECREASE_FACTOR = config('SPECS_OS_DECREASE_FACTOR', default=1, cast=float)
SPECS_SCREEN_TYPE_DECREASE_FACTOR = config('SPECS_SCREEN_TYPE_DECREASE_FACTOR', default=1, cast=float)
SPECS_NETWORK_DECREASE_FACTOR = config('SPECS_NETWORK_DECREASE_FACTOR', default=1, cast=float)
SPECS_USB_TYPE_DECREASE_FACTOR = config('SPECS_USB_TYPE_DECREASE_FACTOR', default=1, cast=float)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'recommender',
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

# settings.py
API_KEY_SECRET = config('API_KEY_SECRET', default='')

ROOT_URLCONF = 'recommenderApi.urls'

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

WSGI_APPLICATION = 'recommenderApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': str(BASE_DIR / 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

# CELERY_BEAT_SCHEDULE = {
#     'TrainTask': {
#         'task': 'recommender.asyn_tasks.tasks.send_schedualed_emails',
#         'schedule': 10 # every 30 seconds
#         # 'schedule': crontab(hour=0, minute=0), # every day at midnight
#     },
# }
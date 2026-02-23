
from pathlib import Path
import os
from datetime import timedelta

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY KEY FOR PRODUCTIONS
SECRET_KEY = 'django-insecure-+^g(k*sczn+22x!#rgdod5q3dcw1k*xf*^x_(5bg8o_*tn8f!k'

# TURN OFF DURING PRODUCTIONS
DEBUG = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# CORS 

# CORS 
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True


# MEDIA URL

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT_RAW = os.path.join(MEDIA_ROOT, 'raw')
MEDIA_ROOT_PROCESSED = os.path.join(MEDIA_ROOT, 'cam')
MEDIA_ROOT_PROFILE = os.path.join(MEDIA_ROOT, 'profile')
MEDIA_ROOT_MODEL = os.path.join(MEDIA_ROOT, 'model_weight')

# INSTALLED APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'broilersDetail',
    'usersDetail',
    'corsheaders'

]

# MIDDLEWARES
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]





ROOT_URLCONF = 'back_end.urls'
AUTH_USER_MODEL = 'usersDetail.usersDetail'
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

WSGI_APPLICATION = 'back_end.wsgi.application'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
    }

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# AUTH PASSWORD VALIDATIONS
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
AUTHENTICATION_BACKENDS = [
    'usersDetail.backend.EmailBackend', 
    'django.contrib.auth.backends.ModelBackend',
]
# INTERNATIONALIZATIONS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
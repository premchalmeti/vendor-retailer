import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'rq6!g@s3mv0+dr)%c8*s6=+pbmql8)3o)cz#+-n%$nhb-5xnu='

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # `vendor` apps
    'shipments.apps.ShipmentsConfig',
    'retailers.apps.RetailersConfig'
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

ROOT_URLCONF = 'vendor_retailer.urls'

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

WSGI_APPLICATION = 'vendor_retailer.wsgi.application'

# `conf` is `.gitignored`d because of secret data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': './conf/db.cnf'
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/second',
        'user': '1000/second',
        'SHIPMENTS': '7/minute'
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# `vendor` configurations below
# below urls are dummy for obvious reasons
# Please substitute below urls with your own APIs

OAUTH_LOGIN_URL = 'https://login.vendor.com/token'

VENDOR_SHIPMENT_LIST_API = 'https://api.vendor.com/retailer/shipments/'
VENDOR_SHIPMENT_DETAIL_API = 'https://api.vendor.com/retailer/shipments/{shipment_id}'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# set default job expiry time to 5 minutes
REDIS_QUEUE_TIMEOUT = 5 * 60

VENDOR_TEST_CLIENT_ID = "redated"
VENDOR_TEST_CLIENT_SECRET = "redated"

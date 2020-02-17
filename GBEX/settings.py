import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = [os.environ.get('DOMAIN')]

if os.environ.get('dev_prod') == 'dev':
	DEBUG = True
	CSRF_COOKIE_SECURE = False
	SESSION_COOKIE_SECURE = False
elif os.environ.get('dev_prod') == 'docker_dev':
	DEBUG = True
	CSRF_COOKIE_SECURE = False
	SESSION_COOKIE_SECURE = False
else:
	DEBUG = False
	CSRF_COOKIE_SECURE = True
	SESSION_COOKIE_SECURE = True

SECRET_KEY = os.environ.get('secret_key')
STATIC_URL = '/static_mad7/'
STATIC_ROOT = os.path.join(BASE_DIR, "shared/static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

#MEDIA_URL = "/download/"
MEDIA_ROOT = os.environ.get('upload_permanent_location')

# logging setup
log = logging.getLogger(__name__)
min_level = 'WARNING'
min_django_level = 'WARNING'

# Reversion
ADD_REVERSION_ADMIN = True

# logging dictConfig configuration
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,  # keep Django's default loggers
	'formatters': {
		# see full list of attributes here:
		# https://docs.python.org/3/library/logging.html#logrecord-attributes
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
		'timestampthread': {
			'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)-20.20s]  %(message)s",
		},
	},
	'handlers': {
		'logfile': {
			# optionally raise to INFO to not fill the log file too quickly
			'level': min_level,  # this level or higher goes to the log file
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': f'{os.environ.get("log_root")}/django.log',
			'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
			'backupCount': 3,  # keep this many extra historical files
			'formatter': 'timestampthread'
		},
		'console': {
			'level': min_level,  # this level or higher goes to the console
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'django': {  # configure all of Django's loggers
			'handlers': ['logfile', 'console'],
			'level': min_django_level,  # this level or higher goes to the console
			'propagate': False,  # don't propagate further, to avoid duplication
		},
		'': {
			'handlers': ['logfile', 'console'],
			'level': min_level,  # this level or higher goes to the console,
		},
	},
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.SessionAuthentication',
	),
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticatedOrReadOnly',
	),
}

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'reversion',
	'reversion_compare',
	'rest_framework',
	'GBEX_bigfiles',
	'GBEX_app.apps.GbexAppConfig',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'GBEX.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'libraries': {
				'laeb_tags': 'GBEX_app.template_tags.tags',
			},
		},
	},
]

WSGI_APPLICATION = 'GBEX.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('db_name'),
		'USER': 'postgres',
		'PASSWORD': os.environ.get('PGPASS'),
		'HOST': os.environ.get('DB_HOST'),
	},
}


AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Copenhagen'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = 'c'

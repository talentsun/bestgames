# -*- coding: utf-8 -*-
# Django settings for GameRecommend project.
import os
from my_setting import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'content_engine',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'nameLR9969',                  # Not used with sqlite3.
        'HOST': '118.144.94.183',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'
FILE_CHARSET='UTF-8'
DEFAULT_CHARSET = 'UTF-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/data/media/'

GAME_PIC_ROOT = '/opt/bestgames/content_engine/scrapy_itunes/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = 'http://localhost:8080/game/'
MEDIA_URL = 'http://cow.bestgames7.com/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.normpath(__file__)))
STATIC_ROOT = PROJECT_ROOT + '/templates'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL =  'http://cow.bestgames7.com/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v0dwj7&amp;i@d!1lnd36-g+e5&amp;igr)n9y@6^wuh1jrgitv3r6c*(z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'content_engine.urls'


LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'
LOGOUT_URL = '/logout'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'content_engine.wsgi.application'

TEMPLATE_DIRS = (PROJECT_ROOT + '/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_tables2',
    'taggit',
    'datetimewidget',
    'ajax_upload',
    'social_auth',
    'django_select2',
    'portal',
    'weixin',
    'scrapy_itunes',
    'dajaxice',
    'dajax',
    'cronjobs',
    'sync',
    'analyse',
    'chartit',
    'ckeditor',
)


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':[
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-'],        
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],        
            ['Bold','Italic','Underline','Strike','-'],        
            ['NumberedList','BulletedList','-','Blockquote'],        
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],        
            ['Link','Unlink'],        
            ['Image','Flash','HorizontalRule','Smiley','SpecialChar'],        
            ['Styles','Format','Font','FontSize'],        
            ['TextColor','BGColor'],        
            ['Maximize','ShowBlocks','Preview']        
        ],
        'height': 500,
        'width':520,
    },
}

CKEDITOR_RESTRICT_BY_USER=True
CKEDITOR_UPLOAD_PATH = "/data/media/upload"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages'
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.weibo.WeiboBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }

    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','default.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'build_index': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','build_index.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'search': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','search.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'weixin': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','weixin.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'sync': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','sync.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'conversation': {
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('/data' + '/logs/','conversation.log'),
            'backupCount': 0,
            'when':'d',
            'interval': 1,
            'formatter':'standard',
        }

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'build_index': {
            'handlers': ['build_index'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'search': {
            'handlers': ['search'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'weixin': {
            'handlers': ['weixin'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sync': {
            'handlers': ['sync'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'conversation': {
            'handlers': ['conversation'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

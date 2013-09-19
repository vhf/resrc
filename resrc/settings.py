# -*- coding: utf-8 -*-:
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Victor Felder', 'victorfelder@gmail.com'),
)

MANAGERS = ADMINS

FROM_EMAIL = "victorfelder@gmail.com"

SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/base.db' % SITE_ROOT,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Zurich'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fi%on41(!pb6-wlh^+#p!urq$-b02d^ehj#1o6!!=%eqja_iv&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'resrc.utils.ThreadLocals',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'resrc.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'resrc.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Default context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Custom context processors
    #'resrc.utils.context_processors.analytics',
    'resrc.utils.context_processors.versions',
)

EXTERNAL_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.admin',

    'south',
    'crispy_forms',
    'crispy_forms_foundation',
    'captcha',
    'email_obfuscator',
    'debug_toolbar',
    'mptt',
    'mptt_comments',
    'floppyforms',
    'taggit',
    'mailer',
]

INTERNAL_APPS = [
    'resrc.userprofile',
    'resrc.link',
    'resrc.list',
    'resrc.page',
    'resrc.utils',
    'resrc.feedback',
    'resrc.tag',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

COMMENTS_APP = "mptt_comments"

# simple captcha
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_LETTER_ROTATION = (0, 1)

# debug toolbar
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_TEMPLATE_PACK = 'foundation'

MPTT_COMMENTS_OFFSET = 20
MPTT_COMMENTS_COLLAPSE_ABOVE = 4
MPTT_COMMENTS_CUTOFF = 5

AUTH_PROFILE_MODULE = 'userprofile.Profile'
LOGIN_URL = '/u/login'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/u/user/{0}'.format(u.username)
}

GOOGLE_ANALYTICS_KEY = ''

try:
    import mailer
    INSTALLED_APPS += ('mailer',)
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
except ImportError:
    pass

# Load the production settings, overwrite the existing ones if needed
try:
    from settings_prod import *
except ImportError:
    pass

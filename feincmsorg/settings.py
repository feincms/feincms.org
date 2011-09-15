# coding=utf-8
import sys, os

APP_BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if APP_BASEDIR not in sys.path:
    sys.path.insert(0, APP_BASEDIR)

execfile(os.path.join(APP_BASEDIR, 'secrets.py'))

if 'runserver' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEBUG = True
else:
    DEBUG = True


GOOGLE_ANALYTICS = 'UA-xxxxxxx-xx'

ADMINS = (
    (u'FEINHEIT Developers', 'dev@feinheit.ch'),
    (u'Matthias Kestenholz', 'mk@feinheit.ch'),
    (u'Fabian Germann', 'fg@feinheit.ch'),
)
MANAGERS = ADMINS
CONTACT_FORM_EMAIL = [mail for name, mail in ADMINS]

TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'
SITE_ID = 1

MEDIA_ROOT = os.path.join(APP_BASEDIR, 'media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = os.path.join(APP_BASEDIR, 'static')
STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'feincms.context_processors.add_page_if_missing',
    'feincmsorg.context_processors.meta_navigation',
)

ROOT_URLCONF = APP_MODULE+'.urls'

TEMPLATE_DIRS = (
    os.path.join(APP_BASEDIR, APP_MODULE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'form_designer',
    'elephantblog',
    #'pinging',
    #'disqus',

    APP_MODULE,

    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'feincms_oembed',
    'mptt',
    'feincmsorg.testimonial',
)

LANGUAGES = (
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(APP_BASEDIR, APP_MODULE, 'locale'),
)

FEINCMS_REVERSE_MONKEY_PATCH = False
FEINCMS_ADMIN_MEDIA = '/static/feincms/'
TINYMCE_JS_URL = '/static/tinymce/tiny_mce.js'
FEINCMS_RICHTEXT_INIT_CONTEXT  = {
    'TINYMCE_JS_URL': TINYMCE_JS_URL,
    'TINYMCE_CONTENT_CSS_URL': None,
    'TINYMCE_LINK_LIST_URL': None
}

GRID = {'column': 30, 'spacing': 10, 'vertical': 18}

#PINGING_WEBLOG_NAME = 'Mein grossartiger Blog!'
#PINGING_WEBLOG_URL = 'http://www.feinheit.ch/blog'

SERVER_EMAIL = 'root@oekohosting.ch'
DEFAULT_FROM_EMAIL = 'root@oekohosting.ch'

CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
    'KEY_PREFIX': APP_MODULE,
}}

SOUTH_MIGRATION_MODULES = dict((app, '%s.migrate.%s' % (APP_MODULE, app)) for app in (
    'page',
    'medialibrary',
    'elephantblog',
    ))

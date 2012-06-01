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
    DEBUG = False

GOOGLE_ANALYTICS = 'UA-xxxxxxx-xx'

ADMINS = (
    (u'FEINHEIT Developers', 'dev@feinheit.ch'),
    (u'Matthias Kestenholz', 'mk@feinheit.ch'),
   # (u'Fabian Germann', 'fg@feinheit.ch'),
    (u'Simon Bächler', 'sb@feinheit.ch'),
)
MANAGERS = ADMINS
CONTACT_FORM_EMAIL = [mail for name, mail in ADMINS]

TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Zurich'
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
    'feincmsorg.middleware.ForceDomainMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'feincms.context_processors.add_page_if_missing',
    'feincmsorg.context_processors.meta_navigation',
    'social_auth.context_processors.social_auth_backends',
)

ROOT_URLCONF = APP_MODULE+'.urls'

TEMPLATE_DIRS = (
    os.path.join(APP_BASEDIR, APP_MODULE, 'templates'),
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'feincmsorg.email_usernames.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
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
    'south',
    #'pinging',
    #'disqus',
    'social_auth',
    APP_MODULE,

    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'feincms_oembed',
    'mptt',
    'feincmsorg.testimonial',
    'feincmsorg.app_library',
    'registration',
    'feincmsorg.email_usernames',
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

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL          = 'accounts/login/'
LOGIN_REDIRECT_URL = '/plugins/submit/'
LOGIN_REDIRECT_URL = '/logged-in/'


SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_EXTRA_DATA = False
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = False
FACEBOOK_EXTENDED_PERMISSIONS = ['email']


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
    'feincmsorg',
    'feincmsorg.app_library',
    ))

FORCE_DOMAIN = 'feincms.org'

BLOG_TITLE = 'FeinCMS.org'
BLOG_DESCRIPTION = 'FeinCMS release notes, tips and stuff.'

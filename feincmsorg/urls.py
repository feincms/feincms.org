import sys

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from elephantblog.sitemap import EntrySitemap
from feincms.module.page.sitemap import PageSitemap


admin.autodiscover()

sitemaps = {
    'pages': PageSitemap,
    'blog': EntrySitemap,
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'', include('social_auth.urls')),
    url(r'apps', include('app_library.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps }),
)

if 'runserver' in sys.argv:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    )
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^blog/', include('elephantblog.urls')),
    url(r'', include('feincms.urls')),
)

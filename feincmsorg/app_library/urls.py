from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('app_library.views',
    url(r'^$', 'app_list', name="app_library_list"),
    url(r'^submit/$', 'app_submit', name="app_library_submit"),
    url(r'^edit/(?P<slug>[^/]+)/$', 'app_edit', name="app_library_edit"),
    url(r'^(?P<slug>[^/]+)/$', 'app_detail', name="app_library_detail"),
    url(r'^category/(?P<slug>[-\w]+)/$', 'app_category_list', name='app_library_category_detail'),
)



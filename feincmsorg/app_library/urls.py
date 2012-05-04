from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('app_library.views',
    url(r'^$', 'app_list', name="app_library_list"),
    url(r'^submit/$', 'app_submit', name="app_library_submit"),
    url(r'^(?P<slug>[^/]+)/$', 'app_detail', name="app_library_detail"),
)

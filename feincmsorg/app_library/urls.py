from django.conf.urls import *

urlpatterns = patterns('app_library.views',
    url(r'^$', 'app_list', name="app_library_list"),
    url(r'^(?P<slug>\w+)/$', 'app_detail', name="app_library_detail"),
)
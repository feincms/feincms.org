from django.conf.urls.defaults import *

urlpatterns = patterns('feincmsorg.email_usernames.views',
    url(r'^login/$', 'email_login', name="email-login"), 
)


from registration.views import register
from .forms import EmailRegistrationForm
urlpatterns += patterns('',
    url(r'^register/$', register,
            { 'form_class':EmailRegistrationForm,
              'backend': 'registration.backends.default.DefaultBackend'},
            name="email-register"),
)

urlpatterns += patterns('',
    url(r'', include('registration.backends.default.urls')),
)
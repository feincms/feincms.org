import sys

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class ForceDomainMiddleware(object):
    def process_request(self, request):
        if 'runserver' or 'test' in sys.argv:
            return

        if request.method != 'GET':
            return

        domain = getattr(settings, 'FORCE_DOMAIN', None)

        if not domain:
            return

        if request.META['HTTP_HOST'] != domain:
            target = 'http%s://%s%s' % (
                request.is_secure() and 's' or '',
                domain,
                request.get_full_path())
            return HttpResponsePermanentRedirect(target)


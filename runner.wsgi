#!/usr/bin/python
import os, sys, site

PATH = os.path.dirname(os.path.abspath(__file__))

site.addsitedir(os.path.join(PATH, 'lib', 'python%s' % sys.version[:3], 'site-packages'))

execfile(os.path.join(PATH, 'secrets.py'))

if PATH not in sys.path:
        sys.path.insert(0, PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % APP_MODULE

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

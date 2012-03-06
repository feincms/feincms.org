import os

import secrets as local_secrets

from fabric.api import *
from fabric.contrib import django
from fabric.contrib.project import rsync_project

from urlparse import urlparse

# requires GitPython to be installed: https://github.com/gitpython-developers/GitPython
from git import Repo
remote_url = Repo().remotes.origin.url
parsed = urlparse(remote_url)
remote_path = parsed.path
if parsed.netloc:
    remote_host = parsed.netloc
else:
    remote_host = parsed.scheme

django.settings_module('%s.settings' % local_secrets.APP_MODULE)
from django.conf import settings

south_installed = 'south' in settings.INSTALLED_APPS

env.hosts = [remote_host]


def update_db():
    get(os.path.join(remote_path, 'secrets.py') , 'remote_secrets.py')
    execfile('remote_secrets.py')
    remote_db = locals()['DATABASES']['default']

    run('mysqldump -u %(USER)s -p%(PASSWORD)s -h %(HOST)s %(NAME)s --ignore-table=%(NAME)s.django_session > /tmp/%(NAME)s.sql'
        % remote_db)
    get('/tmp/%(NAME)s.sql' % remote_db, '/tmp/%(NAME)s.sql' % remote_db)
    local('mysql -u root %(NAME)s < /tmp/%(NAME)s.sql' % remote_db)
    local('rm remote_secrets.py')


def update_media():
    local('rsync -pthrvz %(user)s@%(host)s:%(source)s %(destination)s' % {
        'user' : env.local_user,
        'host' : remote_host,
        'source' : os.path.join(remote_path, 'media/medialibrary'),
        'destination' : 'media/'
    })

def update_all():
    update_db()
    update_media()


def publish():
    local('git push')
    with cd(remote_path):
        run('git merge %s' % env.local_user)
        run('git submodule update --init')
        run('%s/manage.py collectstatic --noinput' % local_secrets.APP_MODULE)
        run('%s/manage.py syncdb' % local_secrets.APP_MODULE)
        if south_installed:
            run('%s/manage.py migrate' % local_secrets.APP_MODULE)
        run('touch runner.wsgi')

def push_db():
    dbname = local_secrets.DATABASES['default']['NAME']
    local('mysqldump -u root %s > /tmp/%s.sql' % (dbname, dbname))
    put('/tmp/%s.sql' % dbname, '/tmp/%s-fromdev.sql' % dbname)

    with cd(remote_path):
        run('%s/manage.py dbshell < /tmp/%s-fromdev.sql' % (local_secrets.APP_MODULE, dbname))

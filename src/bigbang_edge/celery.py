from __future__ import absolute_import

import os
import environ

from celery import Celery

# set the default Django settings module for the 'celery' program.
IS_PRODUCTION = environ.Env().bool('DJANGO_PRODUCTION', default=False)
if not IS_PRODUCTION:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigbang_edge.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigbang_edge.settings.production')

from django.conf import settings  # noqa

app = Celery('bigbang_edge')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


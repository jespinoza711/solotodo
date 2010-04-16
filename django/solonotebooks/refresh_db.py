#!/usr/bin/env python

print "Setting Up Environment",
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

from django.core.management import setup_environ, call_command
setup_environ(settings)
print "Done"

import sys

print "Deleting Tables",
import StringIO
from django.db.models import get_apps
app_labels = [app.__name__.split('.')[-2] for app in get_apps()]
sys.stdout = buffer = StringIO.StringIO()
call_command('sqlclear', *app_labels)
sys.stdout = sys.__stdout__

queries = buffer.getvalue().split(';')[1:-2]

from django.db import connection
cursor = connection.cursor()
for query in queries:
    cursor.execute(query.strip())
print "Done"

print "Synching Database"

call_command('syncdb')
print "Done"

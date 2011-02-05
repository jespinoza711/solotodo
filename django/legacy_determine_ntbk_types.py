import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

ntbks = Notebook.objects.all()

for ntbk in ntbks:
    print ntbk
    ntbk.determine_type()
    ntbk.save()

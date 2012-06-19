import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador import models
from subprocess import *
import simplejson
from datetime import *

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
    
json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.Product')
json = simplejson.loads(json.replace('cotizador.', 'backend.'))

for ptype in json:
    new_fields = {}
    f = ptype['fields']
    new_fields['name'] = f['display_name']
    new_fields['product_type'] = f['ptype']
    new_fields['creation_date'] = str(datetime.strptime(f['date_added'], '%Y-%m-%d %H:%M:%S').date())
    new_fields['creator'] = f['created_by'] or 507
    ptype['fields'] = new_fields
    
print simplejson.dumps(json, sort_keys=True, indent=4)

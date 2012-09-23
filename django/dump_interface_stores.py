import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.Store')
json = simplejson.loads(json.replace('cotizador.', 'backend_interface.'))

providers = []

for store in json:
    f = store['fields']
    new_fields = dict()
    new_fields['name'] = f['name']
    new_fields['is_active'] = True
    store['fields'] = new_fields

    p = dict()
    p['model'] = 'backend_interface.provider'
    p['pk'] = store['pk']
    p['fields'] = dict()
    p['fields']['class_name'] = 'Store'
    providers.append(p)

json.extend(providers)

print simplejson.dumps(json, sort_keys=True, indent=4)

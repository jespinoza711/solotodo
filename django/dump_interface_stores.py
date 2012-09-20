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

inherited_models = []
providers = []

for store in json:
    f = store['fields']
    new_fields = dict()
    new_fields['name'] = f['name']
    new_fields['is_active'] = True
    store['fields'] = new_fields

    im = dict()
    im['model'] = 'backend_interface.inheritedmodel'
    im['pk'] = store['pk']
    im['fields'] = dict()
    im['fields']['class_name'] = 'Store'
    inherited_models.append(im)

    p = dict()
    p['model'] = 'backend_interface.provider'
    p['pk'] = store['pk']
    p['fields'] = dict()
    providers.append(p)

json.extend(providers)
json.extend(inherited_models)

print simplejson.dumps(inherited_models, sort_keys=True, indent=4)

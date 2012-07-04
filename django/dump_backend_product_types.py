import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
    
json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.ProductType')
json = simplejson.loads(json.replace('cotizador.', 'backend.'))

conversion_dict = {
    'Screen': 'Monitor'
}

for ptype in json:
    new_fields = dict()
    new_fields['name'] = conversion_dict.get(ptype['fields']['classname'], ptype['fields']['classname'])
    new_fields['scrap_name'] = conversion_dict.get(ptype['fields']['classname'], ptype['fields']['classname'])
    ptype['fields'] = new_fields

json.append({
    'fields': {
        'name': 'Television',
        'scrap_name': 'Television'
    },
    'model': 'backend.producttype',
    'pk': 11
})
    
print simplejson.dumps(json, sort_keys=True, indent=4)

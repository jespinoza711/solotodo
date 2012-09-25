import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador import models
from subprocess import *
import simplejson

black_list = [
    'Cintegral',
    'Compumanque',
    'Eprod',
    'FullNotebook',
    'Impulso',
    'Racle',
    'rK-Notebooks',
    'Tecno.cl',
    'TecnoGroup',
]

scrap_conversion_dict = {
    'PCExpress': 'PcExpress',
    'PCFactory': 'PcFactory',
    'PCOfertas': 'PcOfertas',
    'TopPC': 'TopPc',
    'HPOnline': 'HpOnline',
    'Bym': 'TtChile'
}

name_conversion_dict = {
    'Bym': 'TtChile'
}

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.Store')
json = simplejson.loads(json.replace('cotizador.', 'backend.'))

providers = []

for store in json:
    f = store['fields']
    new_fields = dict()
    new_fields['name'] = name_conversion_dict.get(f['name'], f['name'])
    new_fields['scrapper_class_name'] = scrap_conversion_dict.get(f['classname'], f['classname'])
    new_fields['is_active'] = f['name'] not in black_list
    new_fields['logo'] = f['picture'].replace('store_logos', 'stores/logos')
    store['fields'] = new_fields

    p = dict()
    p['model'] = 'backend.provider'
    p['pk'] = store['pk']
    p['fields'] = dict()
    p['fields']['class_name'] = 'Store'
    providers.append(p)

json.extend(providers)

print simplejson.dumps(json, sort_keys=True, indent=4)

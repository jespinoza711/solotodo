import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador import models
from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

chosen_models = [
    'InterfaceBrand',
    'InterfaceVideoPort'
]

model_base_names = [
    'Screen'
]

reputable_brand_ids = [17, 29, 19, 9, 4, 12, 32, 2, 5, 3, 21]

for model_name in models.__all__:
    for name in model_base_names:
        if model_name.startswith(name) and model_name != name:
            chosen_models.append(model_name)
            break
    
final_result = simplejson.loads('[]')
for model_name in chosen_models:
    json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.%s --indent=4' % model_name)
    json = simplejson.loads(json.replace('cotizador.', 'electro.'))

    for j in json:
        j['model'] = j['model'].replace('screen', 'television')

        if model_name == 'ScreenBrand':
            j['fields']['is_reputable'] = j['pk'] in reputable_brand_ids

    final_result.extend(json)

print simplejson.dumps(final_result, sort_keys=True, indent=4)

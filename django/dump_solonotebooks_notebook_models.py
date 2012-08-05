import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador import models
from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

chosen_models = ['InterfaceBrand']
for model_name in models.__all__:
    if model_name.startswith('Notebook') and model_name != 'Notebook':
        chosen_models.append(model_name)
    
final_result = simplejson.loads('[]')
for model_name in chosen_models:
    json = run_cmd('python solonotebooks/manage.py dumpdata cotizador.%s --indent=4' % (model_name))
    json = simplejson.loads(json.replace('cotizador.', 'notebooks.'))

    if model_name == 'NotebookType':
        for idx, json_entry in enumerate(json):
            json_entry['fields'] = {
                'name': json_entry['fields']['name'],
                'description': '',
                'ordering': idx + 1
            }
    final_result.extend(json)

print simplejson.dumps(final_result, sort_keys=True, indent=4)

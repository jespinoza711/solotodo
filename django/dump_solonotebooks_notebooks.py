import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
    
products = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata cotizador.Product'))

products_dict = dict([(p['pk'], p['fields']) for p in products])

old_notebooks = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata cotizador.Notebook'))

result = []
for old_notebook in old_notebooks:
    product_fields = products_dict[old_notebook['pk']]
    
    # Create product
    creation_date = product_fields['date_added']
    
    product = {
        'pk': old_notebook['pk'],
        'model': 'backend_interface.product',
        'fields': {
            'display_name': product_fields['display_name'],
            'name': product_fields['name'],
            'class_name': 'Notebook'
        }
    }
    
    # Create notebook
    notebook = old_notebook
    
    notebook['fields']['picture'] = product_fields['picture'].replace('notebook_pics', 'notebooks')
    notebook['fields']['score_general'] = 0
    notebook['fields']['score_games'] = 0
    notebook['fields']['score_mobility'] = 0
    notebook['model'] = 'notebooks.Notebook'

    result.append(notebook)
    result.append(product)

print simplejson.dumps(result, sort_keys=True, indent=4)
    
    

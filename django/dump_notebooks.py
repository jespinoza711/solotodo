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
    
products = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata cotizador.Product'))

products_dict = dict([(p['pk'], p['fields']) for p in products])

old_notebooks = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata cotizador.Notebook'))

result = []
for old_notebook in old_notebooks:
    # Create inherited field
    inherited_field = {
        'pk': old_notebook['pk'],
        'model': 'backend_interface.inheritedmodel',
        'fields': {
            'class_name': 'Notebook'
        }
    }
    result.append(inherited_field)
    
    product_fields = products_dict[old_notebook['pk']]
    
    # Create product
    creation_date = product_fields['date_added']
    
    product = {
        'pk': old_notebook['pk'],
        'model': 'backend_interface.product',
        'fields': {
            'creation_date': str(datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S').date()),
            'display_name': product_fields['display_name'],
            'name': product_fields['name'],
            'creator': product_fields['created_by'] or 507
        }
    }
    result.append(product)
    
    # Create notebook
    notebook = old_notebook
    
    notebook['fields']['picture'] = product_fields['picture']
    notebook['model'] = 'notebooks.Notebook'
    result.append(notebook)
    
print simplejson.dumps(result, sort_keys=True, indent=4)
    
    
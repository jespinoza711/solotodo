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

model_base_names = [
    'VideoCard',
    'Processor',
    'Motherboard',
    'Ram',
    'StorageDrive',
    'PowerSupply',
    'ComputerCase',
    'Screen'
]

result = []

for name in model_base_names:
    old_products = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata cotizador.' + name))

    rname = name
    if rname == 'Screen':
        rname = 'Monitor'

    for old_product in old_products:
        product_fields = products_dict[old_product['pk']]

        if rname == 'Monitor' and old_product['fields']['stype'] == 1:
            continue

        # Create product
        creation_date = product_fields['date_added']

        product = {
            'pk': old_product['pk'],
            'model': 'backend_interface.product',
            'fields': {
                'display_name': product_fields['display_name'],
                'name': product_fields['name'],
                'class_name': rname
            }
        }

        # Create actual product
        new_product = old_product

        new_product['fields']['picture'] = product_fields['picture'].replace('notebook_pics', 'hardware')
        new_product['model'] = 'hardware.' + rname

        result.append(new_product)
        result.append(product)

print simplejson.dumps(result, sort_keys=True, indent=4)
    
    

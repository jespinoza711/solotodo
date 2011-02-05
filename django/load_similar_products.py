import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

for product in Product.objects.all():
    product = product.get_polymorphic_instance()
    print product
    similar_products = [str(prod.id) for prod in product.find_similar_products()]
    product.similar_products = ','.join(similar_products)

    product.save()
 

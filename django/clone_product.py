import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from solonotebooks.cotizador.models import *
from datetime import date

''' Utility method for cloning a product (useful when indexing and finding a 
model very similar - but not equal - to one already in the database) '''
def main():
    id_prod = sys.argv[1]
    prod = Product.objects.get(pk = id_prod).get_polymorphic_instance()
    
    clone_prod = prod.clone_product()

    print clone_prod.id

if __name__ == '__main__':
    main()

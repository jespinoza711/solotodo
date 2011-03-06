import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    old_brand_classes = [NotebookBrand, NotebookChipsetBrand, NotebookOperatingSystemBrand, NotebookProcessorBrand, NotebookVideoCardBrand, NotebookWifiCardBrand, ProcessorBrand, ScreenBrand, VideoCardBrand, VideoCardGpuBrand]
    for old_brand_class in old_brand_classes:
        old_brand_instances = old_brand_class.objects.all()
        for old_brand_instance in old_brand_instances:
            old_brand_instance.brand, created = InterfaceBrand.objects.get_or_create(name = old_brand_instance.name)
            old_brand_instance.save()
            print old_brand_instance.name + ' - ' + unicode(old_brand_instance.brand)
        
if __name__ == '__main__':
    print datetime.now()
    main()
    

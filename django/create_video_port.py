import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    old_port_classes = [VideoCardPort, ScreenVideoPort]
    for old_port_class in old_port_classes:
        old_port_instances = old_port_class.objects.all()
        for old_port_instance in old_port_instances:
            old_port_instance.port, created = InterfaceVideoPort.objects.get_or_create(name = old_port_instance.name)
            old_port_instance.save()
            print old_port_instance.name + ' - ' + unicode(old_port_instance.port)
        
if __name__ == '__main__':
    print datetime.now()
    main()
    

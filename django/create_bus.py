import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    old_bus_instances = VideoCardBus.objects.all()
    for old_bus_instance in old_bus_instances:
        old_bus_instance.bus, created = InterfaceCardBus.objects.get_or_create(name = old_bus_instance.name, lane = old_bus_instance.lane, version = old_bus_instance.version)
        old_bus_instance.bus.save()
        old_bus_instance.save()
        print unicode(old_bus_instance) + ' - ' + unicode(old_bus_instance.bus)
        
if __name__ == '__main__':
    print datetime.now()
    main()
    

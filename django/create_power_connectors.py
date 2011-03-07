import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    old_gpu_instances = VideoCardGpu.objects.all()
    for gpu in old_gpu_instances:
        pc = gpu.power_connectors
        if pc.id == 1:
            continue
        elif pc.id == 2:
            ipc, created = InterfacePowerConnector.objects.get_or_create(name = '6 pines')
            ipc.save()
            vcpc, created = VideoCardPowerConnector.objects.get_or_create(connector = ipc)
            vcpc.save()
            vchpc, created = VideoCardHasPowerConnector.objects.get_or_create(quantity = 1, connector = vcpc)
            vchpc.save()
            gpu.power_conns.add(vchpc)
            gpu.save()
        elif pc.id == 3:
            ipc, created = InterfacePowerConnector.objects.get_or_create(name = '6 pines')
            ipc.save()
            vcpc, created = VideoCardPowerConnector.objects.get_or_create(connector = ipc)
            vcpc.save()
            vchpc, created = VideoCardHasPowerConnector.objects.get_or_create(quantity = 2, connector = vcpc)
            vchpc.save()
            gpu.power_conns.add(vchpc)
            gpu.save()
        elif pc.id == 4:
            ipc, created = InterfacePowerConnector.objects.get_or_create(name = '6 pines')
            ipc.save()
            vcpc, created = VideoCardPowerConnector.objects.get_or_create(connector = ipc)
            vcpc.save()
            vchpc, created = VideoCardHasPowerConnector.objects.get_or_create(quantity = 1, connector = vcpc)
            vchpc.save()
            gpu.power_conns.add(vchpc)
            
            ipc, created = InterfacePowerConnector.objects.get_or_create(name = '8 pines')
            ipc.save()
            vcpc, created = VideoCardPowerConnector.objects.get_or_create(connector = ipc)
            vcpc.save()
            vchpc, created = VideoCardHasPowerConnector.objects.get_or_create(quantity = 1, connector = vcpc)
            vchpc.save()
            gpu.power_conns.add(vchpc)
            
            gpu.save()
            
        print unicode(gpu.power_connectors)
        for conn in gpu.power_conns.all():
            print '* ' + str(conn)
        
if __name__ == '__main__':
    print datetime.now()
    main()
    

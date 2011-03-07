import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from solonotebooks.fetch_scripts import *
from solonotebooks.cotizador.models import *
from common_fetch_methods import *

def main():
    old_socket_instances = ProcessorSocket.objects.all()
    for old_socket_instance in old_socket_instances:
        old_socket_instance.socket, created = InterfaceSocket.objects.get_or_create(name = old_socket_instance.name, num_pins = old_socket_instance.num_pins)
        old_socket_instance.socket.save()
        old_socket_instance.save()
        print unicode(old_socket_instance) + ' - ' + unicode(old_socket_instance.socket)
        
if __name__ == '__main__':
    print datetime.now()
    main()
    

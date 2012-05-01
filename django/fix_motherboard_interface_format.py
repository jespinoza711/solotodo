import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models.interface_motherboard_format import InterfaceMotherboardFormat
from solonotebooks.cotizador.models.motherboard_format import MotherboardFormat


for mf in MotherboardFormat.objects.all():
    imf = InterfaceMotherboardFormat.objects.get_or_create(
        name=mf.name,
        width=mf.width,
        height=mf.height
    )[0]
    mf.format = imf
    mf.save()
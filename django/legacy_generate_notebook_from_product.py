import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

products = Product.objects.all()

for product in products:
    notebook = product
    notebook.__class__ = Notebook
    
    notebook.name = product.name
    notebook.date_added = product.date_added

    notebook.is_ram_dual_channel_2 = product.is_ram_dual_channel
    notebook.has_bluetooth_2 = product.has_bluetooth
    notebook.has_esata_2 = product.has_esata
    notebook.has_fingerprint_reader_2 = product.has_fingerprint_reader
    notebook.has_firewire_2 = product.has_firewire

    notebook.battery_mah_2 = product.battery_mah
    notebook.battery_mwh_2 = product.battery_mwh
    notebook.battery_mv_2 = product.battery_mv
    notebook.battery_cells_2 = product.battery_cells
    notebook.weight_2 = product.weight
    notebook.width_2 = product.width
    notebook.height_2 = product.height
    notebook.thickness_2 = product.thickness
    notebook.usb_port_count_2 = product.usb_port_count
    notebook.webcam_mp_2 = product.webcam_mp

    notebook.ntype_2 = product.ntype
    notebook.line_2 = product.line
    notebook.processor_2 = product.processor
    notebook.lan_2 = product.lan
    notebook.screen_2 = product.screen
    notebook.operating_system_2 = product.operating_system
    notebook.ram_quantity_2 = product.ram_quantity
    notebook.ram_type_2 = product.ram_type
    notebook.ram_frequency_2 = product.ram_frequency
    notebook.chipset_2 = product.chipset
    notebook.optical_drive_2 = product.optical_drive
    notebook.wifi_card_2 = product.wifi_card
    notebook.power_adapter_2 = product.power_adapter
    notebook.card_reader_2 = product.card_reader
    
    print notebook.id
    print notebook
    notebook.save()

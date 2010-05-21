# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ProcessorBrand'
        db.create_table('cotizador_processorbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ProcessorBrand'])

        # Adding model 'ProcessorLineFamily'
        db.create_table('cotizador_processorlinefamily', (
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorBrand'])),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ProcessorLineFamily'])

        # Adding model 'ProcessorLine'
        db.create_table('cotizador_processorline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorLineFamily'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ProcessorLine'])

        # Adding model 'ProcessorFrequency'
        db.create_table('cotizador_processorfrequency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['ProcessorFrequency'])

        # Adding model 'ProcessorCache'
        db.create_table('cotizador_processorcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['ProcessorCache'])

        # Adding model 'ProcessorFSB'
        db.create_table('cotizador_processorfsb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['ProcessorFSB'])

        # Adding model 'ProcessorMultiplier'
        db.create_table('cotizador_processormultiplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
        ))
        db.send_create_signal('cotizador', ['ProcessorMultiplier'])

        # Adding model 'ProcessorSocket'
        db.create_table('cotizador_processorsocket', (
            ('pincount', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ProcessorSocket'])

        # Adding model 'ProcessorManufacturing'
        db.create_table('cotizador_processormanufacturing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['ProcessorManufacturing'])

        # Adding model 'ProcessorFamily'
        db.create_table('cotizador_processorfamily', (
            ('nm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorManufacturing'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ProcessorFamily'])

        # Adding model 'Processor'
        db.create_table('cotizador_processor', (
            ('min_voltage', self.gf('django.db.models.fields.IntegerField')()),
            ('max_voltage', self.gf('django.db.models.fields.IntegerField')()),
            ('cache', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorCache'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorFamily'])),
            ('has_turbo_mode', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorLine'])),
            ('fsb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorFSB'])),
            ('core_number', self.gf('django.db.models.fields.IntegerField')()),
            ('frequency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorFrequency'])),
            ('multiplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorMultiplier'])),
            ('has_smp', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('tdp', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('socket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ProcessorSocket'])),
        ))
        db.send_create_signal('cotizador', ['Processor'])

        # Adding model 'OpticalDrive'
        db.create_table('cotizador_opticaldrive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['OpticalDrive'])

        # Adding model 'NotebookBrand'
        db.create_table('cotizador_notebookbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['NotebookBrand'])

        # Adding model 'NotebookLine'
        db.create_table('cotizador_notebookline', (
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.NotebookBrand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['NotebookLine'])

        # Adding model 'Lan'
        db.create_table('cotizador_lan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['Lan'])

        # Adding model 'OperatingSystemBrand'
        db.create_table('cotizador_operatingsystembrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['OperatingSystemBrand'])

        # Adding model 'OperatingSystemFamily'
        db.create_table('cotizador_operatingsystemfamily', (
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.OperatingSystemBrand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['OperatingSystemFamily'])

        # Adding model 'OperatingSystemLanguage'
        db.create_table('cotizador_operatingsystemlanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['OperatingSystemLanguage'])

        # Adding model 'OperatingSystem'
        db.create_table('cotizador_operatingsystem', (
            ('is_64_bit', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.OperatingSystemLanguage'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.OperatingSystemFamily'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['OperatingSystem'])

        # Adding model 'VideoCardMemory'
        db.create_table('cotizador_videocardmemory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['VideoCardMemory'])

        # Adding model 'VideoCardType'
        db.create_table('cotizador_videocardtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['VideoCardType'])

        # Adding model 'VideoCardBrand'
        db.create_table('cotizador_videocardbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['VideoCardBrand'])

        # Adding model 'VideoCardLine'
        db.create_table('cotizador_videocardline', (
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.VideoCardBrand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['VideoCardLine'])

        # Adding model 'VideoCard'
        db.create_table('cotizador_videocard', (
            ('gpu_frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('card_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.VideoCardType'])),
            ('memory_frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('memory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.VideoCardMemory'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.VideoCardLine'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['VideoCard'])

        # Adding model 'WifiCardBrand'
        db.create_table('cotizador_wificardbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['WifiCardBrand'])

        # Adding model 'WifiCardNorm'
        db.create_table('cotizador_wificardnorm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['WifiCardNorm'])

        # Adding model 'WifiCard'
        db.create_table('cotizador_wificard', (
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.WifiCardBrand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('norm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.WifiCardNorm'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['WifiCard'])

        # Adding model 'VideoPort'
        db.create_table('cotizador_videoport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['VideoPort'])

        # Adding model 'ScreenResolution'
        db.create_table('cotizador_screenresolution', (
            ('horizontal', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vertical', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['ScreenResolution'])

        # Adding model 'ScreenSizeFamily'
        db.create_table('cotizador_screensizefamily', (
            ('base_size', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['ScreenSizeFamily'])

        # Adding model 'ScreenSize'
        db.create_table('cotizador_screensize', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ScreenSizeFamily'])),
            ('size', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
        ))
        db.send_create_signal('cotizador', ['ScreenSize'])

        # Adding model 'Screen'
        db.create_table('cotizador_screen', (
            ('is_led', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_rotating', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_glossy', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_touchscreen', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ScreenResolution'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ScreenSize'])),
        ))
        db.send_create_signal('cotizador', ['Screen'])

        # Adding model 'PowerAdapter'
        db.create_table('cotizador_poweradapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('power', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['PowerAdapter'])

        # Adding model 'StorageDriveType'
        db.create_table('cotizador_storagedrivetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['StorageDriveType'])

        # Adding model 'StorageDriveCapacity'
        db.create_table('cotizador_storagedrivecapacity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['StorageDriveCapacity'])

        # Adding model 'StorageDriveRpm'
        db.create_table('cotizador_storagedriverpm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['StorageDriveRpm'])

        # Adding model 'StorageDrive'
        db.create_table('cotizador_storagedrive', (
            ('capacity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.StorageDriveCapacity'])),
            ('write_speed', self.gf('django.db.models.fields.IntegerField')()),
            ('drive_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.StorageDriveType'])),
            ('rpm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.StorageDriveRpm'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('read_speed', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['StorageDrive'])

        # Adding model 'ChipsetBrand'
        db.create_table('cotizador_chipsetbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['ChipsetBrand'])

        # Adding model 'Chipset'
        db.create_table('cotizador_chipset', (
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.ChipsetBrand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['Chipset'])

        # Adding model 'RamQuantity'
        db.create_table('cotizador_ramquantity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
        ))
        db.send_create_signal('cotizador', ['RamQuantity'])

        # Adding model 'RamType'
        db.create_table('cotizador_ramtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['RamType'])

        # Adding model 'RamFrequency'
        db.create_table('cotizador_ramfrequency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['RamFrequency'])

        # Adding model 'NotebookCardReader'
        db.create_table('cotizador_notebookcardreader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['NotebookCardReader'])

        # Adding model 'Notebook'
        db.create_table('cotizador_notebook', (
            ('webcam_mp', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
            ('is_ram_dual_channel', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('has_fingerprint_reader', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('battery_mah', self.gf('django.db.models.fields.IntegerField')()),
            ('wifi_card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.WifiCard'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('has_bluetooth', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('ram_quantity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.RamQuantity'])),
            ('power_adapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.PowerAdapter'])),
            ('battery_mwh', self.gf('django.db.models.fields.IntegerField')()),
            ('thickness', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('min_price', self.gf('django.db.models.fields.IntegerField')()),
            ('optical_drive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.OpticalDrive'])),
            ('usb_port_count', self.gf('django.db.models.fields.IntegerField')()),
            ('battery_cells', self.gf('django.db.models.fields.IntegerField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('lan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Lan'])),
            ('screen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Screen'])),
            ('battery_mv', self.gf('django.db.models.fields.IntegerField')()),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('ram_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.RamType'])),
            ('has_firewire', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.NotebookLine'])),
            ('operating_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.OperatingSystem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('card_reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.NotebookCardReader'])),
            ('ram_frequency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.RamFrequency'])),
            ('chipset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Chipset'])),
            ('other', self.gf('django.db.models.fields.TextField')()),
            ('has_esata', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Processor'])),
        ))
        db.send_create_signal('cotizador', ['Notebook'])

        # Adding M2M table for field storage_drive on 'Notebook'
        db.create_table('cotizador_notebook_storage_drive', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notebook', models.ForeignKey(orm['cotizador.notebook'], null=False)),
            ('storagedrive', models.ForeignKey(orm['cotizador.storagedrive'], null=False))
        ))
        db.create_unique('cotizador_notebook_storage_drive', ['notebook_id', 'storagedrive_id'])

        # Adding M2M table for field video_card on 'Notebook'
        db.create_table('cotizador_notebook_video_card', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notebook', models.ForeignKey(orm['cotizador.notebook'], null=False)),
            ('videocard', models.ForeignKey(orm['cotizador.videocard'], null=False))
        ))
        db.create_unique('cotizador_notebook_video_card', ['notebook_id', 'videocard_id'])

        # Adding M2M table for field video_port on 'Notebook'
        db.create_table('cotizador_notebook_video_port', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notebook', models.ForeignKey(orm['cotizador.notebook'], null=False)),
            ('videoport', models.ForeignKey(orm['cotizador.videoport'], null=False))
        ))
        db.create_unique('cotizador_notebook_video_port', ['notebook_id', 'videoport_id'])

        # Adding model 'NotebookReview'
        db.create_table('cotizador_notebookreview', (
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('score_mobility', self.gf('django.db.models.fields.IntegerField')()),
            ('score_speed', self.gf('django.db.models.fields.IntegerField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('score_construction', self.gf('django.db.models.fields.IntegerField')()),
            ('notebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Notebook'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score_total', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['NotebookReview'])

        # Adding model 'NotebookComment'
        db.create_table('cotizador_notebookcomment', (
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('notebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Notebook'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['NotebookComment'])

        # Adding model 'NotebookPicture'
        db.create_table('cotizador_notebookpicture', (
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('notebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Notebook'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['NotebookPicture'])

        # Adding model 'NotebookPriceChange'
        db.create_table('cotizador_notebookpricechange', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('notebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Notebook'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['NotebookPriceChange'])

        # Adding model 'City'
        db.create_table('cotizador_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['City'])

        # Adding model 'Store'
        db.create_table('cotizador_store', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cotizador', ['Store'])

        # Adding model 'Sucursal'
        db.create_table('cotizador_sucursal', (
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.City'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('longitude', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('latitude', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Store'])),
        ))
        db.send_create_signal('cotizador', ['Sucursal'])

        # Adding model 'StoreHasNotebook'
        db.create_table('cotizador_storehasnotebook', (
            ('custom_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visitorCount', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('latest_price', self.gf('django.db.models.fields.IntegerField')()),
            ('notebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Notebook'], null=True, blank=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Store'])),
        ))
        db.send_create_signal('cotizador', ['StoreHasNotebook'])

        # Adding model 'StoreNotebookHistory'
        db.create_table('cotizador_storenotebookhistory', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.StoreHasNotebook'])),
        ))
        db.send_create_signal('cotizador', ['StoreNotebookHistory'])

        # Adding model 'LogEntry'
        db.create_table('cotizador_logentry', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cotizador', ['LogEntry'])

        # Adding model 'LogEntryMessage'
        db.create_table('cotizador_logentrymessage', (
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logEntry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.LogEntry'])),
        ))
        db.send_create_signal('cotizador', ['LogEntryMessage'])

        # Adding model 'ExternalVisit'
        db.create_table('cotizador_externalvisit', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shn', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.StoreHasNotebook'])),
        ))
        db.send_create_signal('cotizador', ['ExternalVisit'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'ProcessorBrand'
        db.delete_table('cotizador_processorbrand')

        # Deleting model 'ProcessorLineFamily'
        db.delete_table('cotizador_processorlinefamily')

        # Deleting model 'ProcessorLine'
        db.delete_table('cotizador_processorline')

        # Deleting model 'ProcessorFrequency'
        db.delete_table('cotizador_processorfrequency')

        # Deleting model 'ProcessorCache'
        db.delete_table('cotizador_processorcache')

        # Deleting model 'ProcessorFSB'
        db.delete_table('cotizador_processorfsb')

        # Deleting model 'ProcessorMultiplier'
        db.delete_table('cotizador_processormultiplier')

        # Deleting model 'ProcessorSocket'
        db.delete_table('cotizador_processorsocket')

        # Deleting model 'ProcessorManufacturing'
        db.delete_table('cotizador_processormanufacturing')

        # Deleting model 'ProcessorFamily'
        db.delete_table('cotizador_processorfamily')

        # Deleting model 'Processor'
        db.delete_table('cotizador_processor')

        # Deleting model 'OpticalDrive'
        db.delete_table('cotizador_opticaldrive')

        # Deleting model 'NotebookBrand'
        db.delete_table('cotizador_notebookbrand')

        # Deleting model 'NotebookLine'
        db.delete_table('cotizador_notebookline')

        # Deleting model 'Lan'
        db.delete_table('cotizador_lan')

        # Deleting model 'OperatingSystemBrand'
        db.delete_table('cotizador_operatingsystembrand')

        # Deleting model 'OperatingSystemFamily'
        db.delete_table('cotizador_operatingsystemfamily')

        # Deleting model 'OperatingSystemLanguage'
        db.delete_table('cotizador_operatingsystemlanguage')

        # Deleting model 'OperatingSystem'
        db.delete_table('cotizador_operatingsystem')

        # Deleting model 'VideoCardMemory'
        db.delete_table('cotizador_videocardmemory')

        # Deleting model 'VideoCardType'
        db.delete_table('cotizador_videocardtype')

        # Deleting model 'VideoCardBrand'
        db.delete_table('cotizador_videocardbrand')

        # Deleting model 'VideoCardLine'
        db.delete_table('cotizador_videocardline')

        # Deleting model 'VideoCard'
        db.delete_table('cotizador_videocard')

        # Deleting model 'WifiCardBrand'
        db.delete_table('cotizador_wificardbrand')

        # Deleting model 'WifiCardNorm'
        db.delete_table('cotizador_wificardnorm')

        # Deleting model 'WifiCard'
        db.delete_table('cotizador_wificard')

        # Deleting model 'VideoPort'
        db.delete_table('cotizador_videoport')

        # Deleting model 'ScreenResolution'
        db.delete_table('cotizador_screenresolution')

        # Deleting model 'ScreenSizeFamily'
        db.delete_table('cotizador_screensizefamily')

        # Deleting model 'ScreenSize'
        db.delete_table('cotizador_screensize')

        # Deleting model 'Screen'
        db.delete_table('cotizador_screen')

        # Deleting model 'PowerAdapter'
        db.delete_table('cotizador_poweradapter')

        # Deleting model 'StorageDriveType'
        db.delete_table('cotizador_storagedrivetype')

        # Deleting model 'StorageDriveCapacity'
        db.delete_table('cotizador_storagedrivecapacity')

        # Deleting model 'StorageDriveRpm'
        db.delete_table('cotizador_storagedriverpm')

        # Deleting model 'StorageDrive'
        db.delete_table('cotizador_storagedrive')

        # Deleting model 'ChipsetBrand'
        db.delete_table('cotizador_chipsetbrand')

        # Deleting model 'Chipset'
        db.delete_table('cotizador_chipset')

        # Deleting model 'RamQuantity'
        db.delete_table('cotizador_ramquantity')

        # Deleting model 'RamType'
        db.delete_table('cotizador_ramtype')

        # Deleting model 'RamFrequency'
        db.delete_table('cotizador_ramfrequency')

        # Deleting model 'NotebookCardReader'
        db.delete_table('cotizador_notebookcardreader')

        # Deleting model 'Notebook'
        db.delete_table('cotizador_notebook')

        # Removing M2M table for field storage_drive on 'Notebook'
        db.delete_table('cotizador_notebook_storage_drive')

        # Removing M2M table for field video_card on 'Notebook'
        db.delete_table('cotizador_notebook_video_card')

        # Removing M2M table for field video_port on 'Notebook'
        db.delete_table('cotizador_notebook_video_port')

        # Deleting model 'NotebookReview'
        db.delete_table('cotizador_notebookreview')

        # Deleting model 'NotebookComment'
        db.delete_table('cotizador_notebookcomment')

        # Deleting model 'NotebookPicture'
        db.delete_table('cotizador_notebookpicture')

        # Deleting model 'NotebookPriceChange'
        db.delete_table('cotizador_notebookpricechange')

        # Deleting model 'City'
        db.delete_table('cotizador_city')

        # Deleting model 'Store'
        db.delete_table('cotizador_store')

        # Deleting model 'Sucursal'
        db.delete_table('cotizador_sucursal')

        # Deleting model 'StoreHasNotebook'
        db.delete_table('cotizador_storehasnotebook')

        # Deleting model 'StoreNotebookHistory'
        db.delete_table('cotizador_storenotebookhistory')

        # Deleting model 'LogEntry'
        db.delete_table('cotizador_logentry')

        # Deleting model 'LogEntryMessage'
        db.delete_table('cotizador_logentrymessage')

        # Deleting model 'ExternalVisit'
        db.delete_table('cotizador_externalvisit')
    
    
    models = {
        'cotizador.chipset': {
            'Meta': {'object_name': 'Chipset'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ChipsetBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.chipsetbrand': {
            'Meta': {'object_name': 'ChipsetBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.externalvisit': {
            'Meta': {'object_name': 'ExternalVisit'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasNotebook']"})
        },
        'cotizador.lan': {
            'Meta': {'object_name': 'Lan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.logentrymessage': {
            'Meta': {'object_name': 'LogEntryMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logEntry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.notebook': {
            'Meta': {'object_name': 'Notebook'},
            'battery_cells': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mah': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mv': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mwh': ('django.db.models.fields.IntegerField', [], {}),
            'card_reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookCardReader']"}),
            'chipset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Chipset']"}),
            'has_bluetooth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_esata': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_fingerprint_reader': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_firewire': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_ram_dual_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'lan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Lan']"}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookLine']"}),
            'min_price': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OperatingSystem']"}),
            'optical_drive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OpticalDrive']"}),
            'other': ('django.db.models.fields.TextField', [], {}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'power_adapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerAdapter']"}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Processor']"}),
            'ram_frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamFrequency']"}),
            'ram_quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamQuantity']"}),
            'ram_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamType']"}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Screen']"}),
            'storage_drive': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.StorageDrive']"}),
            'thickness': ('django.db.models.fields.IntegerField', [], {}),
            'usb_port_count': ('django.db.models.fields.IntegerField', [], {}),
            'video_card': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.VideoCard']"}),
            'video_port': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.VideoPort']"}),
            'webcam_mp': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'weight': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {}),
            'wifi_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.WifiCard']"})
        },
        'cotizador.notebookbrand': {
            'Meta': {'object_name': 'NotebookBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookcardreader': {
            'Meta': {'object_name': 'NotebookCardReader'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookcomment': {
            'Meta': {'object_name': 'NotebookComment'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Notebook']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.notebookline': {
            'Meta': {'object_name': 'NotebookLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookpicture': {
            'Meta': {'object_name': 'NotebookPicture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Notebook']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'cotizador.notebookpricechange': {
            'Meta': {'object_name': 'NotebookPriceChange'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Notebook']"}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookreview': {
            'Meta': {'object_name': 'NotebookReview'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Notebook']"}),
            'score_construction': ('django.db.models.fields.IntegerField', [], {}),
            'score_mobility': ('django.db.models.fields.IntegerField', [], {}),
            'score_speed': ('django.db.models.fields.IntegerField', [], {}),
            'score_total': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.operatingsystem': {
            'Meta': {'object_name': 'OperatingSystem'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OperatingSystemFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_64_bit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OperatingSystemLanguage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.operatingsystembrand': {
            'Meta': {'object_name': 'OperatingSystemBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.operatingsystemfamily': {
            'Meta': {'object_name': 'OperatingSystemFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OperatingSystemBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.operatingsystemlanguage': {
            'Meta': {'object_name': 'OperatingSystemLanguage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.opticaldrive': {
            'Meta': {'object_name': 'OpticalDrive'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.poweradapter': {
            'Meta': {'object_name': 'PowerAdapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processor': {
            'Meta': {'object_name': 'Processor'},
            'cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorCache']"}),
            'core_number': ('django.db.models.fields.IntegerField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorFamily']"}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorFrequency']"}),
            'fsb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorFSB']"}),
            'has_smp': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_turbo_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorLine']"}),
            'max_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'min_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'multiplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorMultiplier']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorSocket']"}),
            'tdp': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        },
        'cotizador.processorbrand': {
            'Meta': {'object_name': 'ProcessorBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processorcache': {
            'Meta': {'object_name': 'ProcessorCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorfamily': {
            'Meta': {'object_name': 'ProcessorFamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorManufacturing']"})
        },
        'cotizador.processorfrequency': {
            'Meta': {'object_name': 'ProcessorFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorfsb': {
            'Meta': {'object_name': 'ProcessorFSB'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorline': {
            'Meta': {'object_name': 'ProcessorLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorLineFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processorlinefamily': {
            'Meta': {'object_name': 'ProcessorLineFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.processormanufacturing': {
            'Meta': {'object_name': 'ProcessorManufacturing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processormultiplier': {
            'Meta': {'object_name': 'ProcessorMultiplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.processorsocket': {
            'Meta': {'object_name': 'ProcessorSocket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincount': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramfrequency': {
            'Meta': {'object_name': 'RamFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramquantity': {
            'Meta': {'object_name': 'RamQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.ramtype': {
            'Meta': {'object_name': 'RamType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.screen': {
            'Meta': {'object_name': 'Screen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_glossy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_led': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_rotating': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_touchscreen': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenResolution']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenSize']"})
        },
        'cotizador.screenresolution': {
            'Meta': {'object_name': 'ScreenResolution'},
            'horizontal': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vertical': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screensize': {
            'Meta': {'object_name': 'ScreenSize'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenSizeFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.screensizefamily': {
            'Meta': {'object_name': 'ScreenSizeFamily'},
            'base_size': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.storagedrive': {
            'Meta': {'object_name': 'StorageDrive'},
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveCapacity']"}),
            'drive_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_speed': ('django.db.models.fields.IntegerField', [], {}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveRpm']"}),
            'write_speed': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedrivecapacity': {
            'Meta': {'object_name': 'StorageDriveCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedriverpm': {
            'Meta': {'object_name': 'StorageDriveRpm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedrivetype': {
            'Meta': {'object_name': 'StorageDriveType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.store': {
            'Meta': {'object_name': 'Store'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cotizador.storehasnotebook': {
            'Meta': {'object_name': 'StoreHasNotebook'},
            'custom_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'latest_price': ('django.db.models.fields.IntegerField', [], {}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Notebook']", 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'visitorCount': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storenotebookhistory': {
            'Meta': {'object_name': 'StoreNotebookHistory'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'registry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasNotebook']"})
        },
        'cotizador.sucursal': {
            'Meta': {'object_name': 'Sucursal'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.IntegerField', [], {}),
            'longitude': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"})
        },
        'cotizador.videocard': {
            'Meta': {'object_name': 'VideoCard'},
            'card_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardType']"}),
            'gpu_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardLine']"}),
            'memory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardMemory']"}),
            'memory_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardbrand': {
            'Meta': {'object_name': 'VideoCardBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardline': {
            'Meta': {'object_name': 'VideoCardLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardmemory': {
            'Meta': {'object_name': 'VideoCardMemory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardtype': {
            'Meta': {'object_name': 'VideoCardType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videoport': {
            'Meta': {'object_name': 'VideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.wificard': {
            'Meta': {'object_name': 'WifiCard'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.WifiCardBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'norm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.WifiCardNorm']"})
        },
        'cotizador.wificardbrand': {
            'Meta': {'object_name': 'WifiCardBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.wificardnorm': {
            'Meta': {'object_name': 'WifiCardNorm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['cotizador']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Notebook.power_adapter_2'
        db.rename_column('cotizador_notebook', 'power_adapter_2_id', 'power_adapter_id')

        # Deleting field 'Notebook.ram_quantity_2'
        db.rename_column('cotizador_notebook', 'ram_quantity_2_id', 'ram_quantity_id')

        # Deleting field 'Notebook.has_bluetooth_2'
        db.rename_column('cotizador_notebook', 'has_bluetooth_2', 'has_bluetooth')

        # Deleting field 'Notebook.chipset_2'
        db.rename_column('cotizador_notebook', 'chipset_2_id', 'chipset_id')

        # Deleting field 'Notebook.has_firewire_2'
        db.rename_column('cotizador_notebook', 'has_firewire_2', 'has_firewire')

        # Deleting field 'Notebook.optical_drive_2'
        db.rename_column('cotizador_notebook', 'optical_drive_2_id', 'optical_drive_id')

        # Deleting field 'Notebook.lan_2'
        db.rename_column('cotizador_notebook', 'lan_2_id', 'lan_id')

        # Deleting field 'Notebook.card_reader_2'
        db.rename_column('cotizador_notebook', 'card_reader_2_id', 'card_reader_id')

        # Deleting field 'Notebook.usb_port_count_2'
        db.rename_column('cotizador_notebook', 'usb_port_count_2', 'usb_port_count')

        # Deleting field 'Notebook.battery_mwh_2'
        db.rename_column('cotizador_notebook', 'battery_mwh_2', 'battery_mwh')

        # Deleting field 'Notebook.operating_system_2'
        db.rename_column('cotizador_notebook', 'operating_system_2_id', 'operating_system_id')

        # Deleting field 'Notebook.webcam_mp_2'
        db.rename_column('cotizador_notebook', 'webcam_mp_2', 'webcam_mp')

        # Deleting field 'Notebook.height_2'
        db.rename_column('cotizador_notebook', 'height_2', 'height')

        # Deleting field 'Notebook.battery_mah_2'
        db.rename_column('cotizador_notebook', 'battery_mah_2', 'battery_mah')

        # Deleting field 'Notebook.line_2'
        db.rename_column('cotizador_notebook', 'line_2_id', 'line_id')

        # Deleting field 'Notebook.width_2'
        db.rename_column('cotizador_notebook', 'width_2', 'width')

        # Deleting field 'Notebook.ram_type_2'
        db.rename_column('cotizador_notebook', 'ram_type_2_id', 'ram_type_id')

        # Deleting field 'Notebook.screen_2'
        db.rename_column('cotizador_notebook', 'screen_2_id', 'screen_id')

        # Deleting field 'Notebook.battery_cells_2'
        db.rename_column('cotizador_notebook', 'battery_cells_2', 'battery_cells')

        # Deleting field 'Notebook.wifi_card_2'
        db.rename_column('cotizador_notebook', 'wifi_card_2_id', 'wifi_card_id')

        # Deleting field 'Notebook.is_ram_dual_channel_2'
        db.rename_column('cotizador_notebook', 'is_ram_dual_channel_2', 'is_ram_dual_channel')

        # Deleting field 'Notebook.battery_mv_2'
        db.rename_column('cotizador_notebook', 'battery_mv_2', 'battery_mv')

        # Deleting field 'Notebook.weight_2'
        db.rename_column('cotizador_notebook', 'weight_2', 'weight')

        # Deleting field 'Notebook.ntype_2'
        db.rename_column('cotizador_notebook', 'ntype_2_id', 'ntype_id')

        # Deleting field 'Notebook.processor_2'
        db.rename_column('cotizador_notebook', 'processor_2_id', 'processor_id')

        # Deleting field 'Notebook.has_fingerprint_reader_2'
        db.rename_column('cotizador_notebook', 'has_fingerprint_reader_2', 'has_fingerprint_reader')

        # Deleting field 'Notebook.ram_frequency_2'
        db.rename_column('cotizador_notebook', 'ram_frequency_2_id', 'ram_frequency_id')

        # Deleting field 'Notebook.has_esata_2'
        db.rename_column('cotizador_notebook', 'has_esata_2', 'has_esata')

        # Deleting field 'Notebook.thickness_2'
        db.rename_column('cotizador_notebook', 'thickness_2', 'thickness')
    
    
    def backwards(self, orm):
        
        # Deleting field 'Notebook.power_adapter'
        db.rename_column('cotizador_notebook', 'power_adapter_id', 'power_adapter_2_id')

        # Deleting field 'Notebook.ram_quantity'
        db.rename_column('cotizador_notebook', 'ram_quantity_id', 'ram_quantity_2_id')

        # Deleting field 'Notebook.has_bluetooth'
        db.rename_column('cotizador_notebook', 'has_bluetooth', 'has_bluetooth_2')

        # Deleting field 'Notebook.chipset'
        db.rename_column('cotizador_notebook', 'chipset_id', 'chipset_2_id')

        # Deleting field 'Notebook.has_firewire'
        db.rename_column('cotizador_notebook', 'has_firewire', 'has_firewire_2')

        # Deleting field 'Notebook.optical_drive'
        db.rename_column('cotizador_notebook', 'optical_drive_id', 'optical_drive_2_id')

        # Deleting field 'Notebook.lan'
        db.rename_column('cotizador_notebook', 'lan_id', 'lan_2_id')

        # Deleting field 'Notebook.card_reader'
        db.rename_column('cotizador_notebook', 'card_reader_id', 'card_reader_2_id')

        # Deleting field 'Notebook.usb_port_count'
        db.rename_column('cotizador_notebook', 'usb_port_count', 'usb_port_count_2')

        # Deleting field 'Notebook.battery_mwh'
        db.rename_column('cotizador_notebook', 'battery_mwh', 'battery_mwh_2')

        # Deleting field 'Notebook.operating_system'
        db.rename_column('cotizador_notebook', 'operating_system_id', 'operating_system_2_id')

        # Deleting field 'Notebook.webcam_mp'
        db.rename_column('cotizador_notebook', 'webcam_mp', 'webcam_mp_2')

        # Deleting field 'Notebook.height'
        db.rename_column('cotizador_notebook', 'height', 'height_2')

        # Deleting field 'Notebook.battery_mah'
        db.rename_column('cotizador_notebook', 'battery_mah', 'battery_mah_2')

        # Deleting field 'Notebook.line'
        db.rename_column('cotizador_notebook', 'line_id', 'line_2_id')

        # Deleting field 'Notebook.width'
        db.rename_column('cotizador_notebook', 'width', 'width_2')

        # Deleting field 'Notebook.ram_type'
        db.rename_column('cotizador_notebook', 'ram_type_id', 'ram_type_2_id')

        # Deleting field 'Notebook.screen'
        db.rename_column('cotizador_notebook', 'screen_id', 'screen_2_id')

        # Deleting field 'Notebook.battery_cells'
        db.rename_column('cotizador_notebook', 'battery_cells', 'battery_cells_2')

        # Deleting field 'Notebook.wifi_card'
        db.rename_column('cotizador_notebook', 'wifi_card_id', 'wifi_card_2_id')

        # Deleting field 'Notebook.is_ram_dual_channel'
        db.rename_column('cotizador_notebook', 'is_ram_dual_channel', 'is_ram_dual_channel_2')

        # Deleting field 'Notebook.battery_mv'
        db.rename_column('cotizador_notebook', 'battery_mv', 'battery_mv_2')

        # Deleting field 'Notebook.weight'
        db.rename_column('cotizador_notebook', 'weight', 'weight_2')

        # Deleting field 'Notebook.ntype'
        db.rename_column('cotizador_notebook', 'ntype_id', 'ntype_2_id')

        # Deleting field 'Notebook.processor'
        db.rename_column('cotizador_notebook', 'processor_id', 'processor_2_id')

        # Deleting field 'Notebook.has_fingerprint_reader'
        db.rename_column('cotizador_notebook', 'has_fingerprint_reader', 'has_fingerprint_reader_2')

        # Deleting field 'Notebook.ram_frequency'
        db.rename_column('cotizador_notebook', 'ram_frequency_id', 'ram_frequency_2_id')

        # Deleting field 'Notebook.has_esata'
        db.rename_column('cotizador_notebook', 'has_esata', 'has_esata_2')

        # Deleting field 'Notebook.thickness'
        db.rename_column('cotizador_notebook', 'thickness', 'thickness_2')
    
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cotizador.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'embedding_html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.IntegerField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.AdvertisementPosition']"}),
            'target_url': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.advertisementposition': {
            'Meta': {'object_name': 'AdvertisementPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.advertisementvisit': {
            'Meta': {'object_name': 'AdvertisementVisit'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Advertisement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referer_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.lan': {
            'Meta': {'object_name': 'Lan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.logchangemodelprice': {
            'Meta': {'object_name': 'LogChangeModelPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'new_price': ('django.db.models.fields.IntegerField', [], {}),
            'old_price': ('django.db.models.fields.IntegerField', [], {}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logchangenotebookprice': {
            'Meta': {'object_name': 'LogChangeNotebookPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'new_price': ('django.db.models.fields.IntegerField', [], {}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'old_price': ('django.db.models.fields.IntegerField', [], {})
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
        'cotizador.loglostmodel': {
            'Meta': {'object_name': 'LogLostModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.loglostnotebook': {
            'Meta': {'object_name': 'LogLostNotebook'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.lognewmodel': {
            'Meta': {'object_name': 'LogNewModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logrevivemodel': {
            'Meta': {'object_name': 'LogReviveModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logrevivenotebook': {
            'Meta': {'object_name': 'LogReviveNotebook'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.mailchangenotebookprice': {
            'Meta': {'object_name': 'MailChangeNotebookPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogChangeNotebookPrice']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.maillostnotebook': {
            'Meta': {'object_name': 'MailLostNotebook'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogLostNotebook']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.mailrevivenotebook': {
            'Meta': {'object_name': 'MailReviveNotebook'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogReviveNotebook']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.notebook': {
            'Meta': {'object_name': 'Notebook', '_ormbases': ['cotizador.Product']},
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
            'is_ram_dual_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'lan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Lan']"}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookLine']"}),
            'ntype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookType']"}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OperatingSystem']"}),
            'optical_drive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.OpticalDrive']"}),
            'power_adapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerAdapter']"}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Processor']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'ram_frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamFrequency']"}),
            'ram_quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamQuantity']"}),
            'ram_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamType']"}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Screen']"}),
            'storage_drive': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.StorageDrive']", 'symmetrical': 'False'}),
            'thickness': ('django.db.models.fields.IntegerField', [], {}),
            'usb_port_count': ('django.db.models.fields.IntegerField', [], {}),
            'video_card': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.VideoCard']", 'symmetrical': 'False'}),
            'video_port': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.VideoPort']", 'symmetrical': 'False'}),
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
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.notebookcomparisonlist': {
            'Meta': {'object_name': 'NotebookComparisonList'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebooks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.Product']", 'symmetrical': 'False'})
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
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'cotizador.notebookpricechange': {
            'Meta': {'object_name': 'NotebookPriceChange'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookreview': {
            'Meta': {'object_name': 'NotebookReview'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'score_construction': ('django.db.models.fields.IntegerField', [], {}),
            'score_mobility': ('django.db.models.fields.IntegerField', [], {}),
            'score_speed': ('django.db.models.fields.IntegerField', [], {}),
            'score_total': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebooksubscription': {
            'Meta': {'object_name': 'NotebookSubscription'},
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cotizador.notebooktype': {
            'Meta': {'object_name': 'NotebookType'},
            'css_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'processor_consumption': ('django.db.models.fields.IntegerField', [], {}),
            'processor_speed': ('django.db.models.fields.IntegerField', [], {}),
            'ram_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'screen_size': ('django.db.models.fields.IntegerField', [], {}),
            'storage_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'video_card_speed': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookvisit': {
            'Meta': {'object_name': 'NotebookVisit'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
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
            'consumption': ('django.db.models.fields.IntegerField', [], {}),
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
            'speed_score': ('django.db.models.fields.IntegerField', [], {}),
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
        'cotizador.product': {
            'Meta': {'object_name': 'Product'},
            'date_added': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'min_price': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other': ('django.db.models.fields.TextField', [], {}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'publicized_offer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ntbk'", 'null': 'True', 'to': "orm['cotizador.StoreHasProductEntity']"}),
            'similar_notebooks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'}),
            'week_discount': ('django.db.models.fields.IntegerField', [], {}),
            'week_visitor_count': ('django.db.models.fields.IntegerField', [], {})
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
        'cotizador.searchregistry': {
            'Meta': {'object_name': 'SearchRegistry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {})
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
        'cotizador.storehasproduct': {
            'Meta': {'object_name': 'StoreHasProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']", 'null': 'True', 'blank': 'True'}),
            'prevent_availability_change': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'shne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']", 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"})
        },
        'cotizador.storehasproductentity': {
            'Meta': {'object_name': 'StoreHasProductEntity'},
            'comparison_field': ('django.db.models.fields.TextField', [], {}),
            'custom_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'latest_price': ('django.db.models.fields.IntegerField', [], {}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProduct']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.storenotebookhistory': {
            'Meta': {'object_name': 'StoreNotebookHistory'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'registry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
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
        'cotizador.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'assigned_store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']", 'null': 'True', 'blank': 'True'}),
            'change_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'confirmation_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'cotizador.videocard': {
            'Meta': {'object_name': 'VideoCard'},
            'card_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardType']"}),
            'gpu_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardLine']"}),
            'memory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardMemory']"}),
            'memory_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'speed_score': ('django.db.models.fields.IntegerField', [], {})
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

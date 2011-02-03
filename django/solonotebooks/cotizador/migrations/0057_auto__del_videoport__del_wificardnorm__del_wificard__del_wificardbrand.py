# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'VideoPort'
        db.rename_table('cotizador_videoport', 'cotizador_notebookvideoport')

        # Deleting model 'WifiCardNorm'
        db.rename_table('cotizador_wificardnorm', 'cotizador_notebookwificardnorm')

        # Deleting model 'WifiCard'
        db.rename_table('cotizador_wificard', 'cotizador_notebookwificard')

        # Deleting model 'WifiCardBrand'
        db.rename_table('cotizador_wificardbrand', 'cotizador_notebookwificardbrand')
        
        db.rename_column('cotizador_notebook_video_port', 'videoport_id', 'notebookvideoport_id')
        
        # Changing field 'Notebook.wifi_card'
        db.alter_column('cotizador_notebook', 'wifi_card_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.NotebookWifiCard']))
    
    
    def backwards(self, orm):
        
        # Deleting model 'VideoPort'
        db.rename_table('cotizador_notebookvideoport', 'cotizador_videoport')

        # Deleting model 'WifiCardNorm'
        db.rename_table('cotizador_notebookwificardnorm', 'cotizador_wificardnorm')

        # Deleting model 'WifiCard'
        db.rename_table('cotizador_notebookwificard', 'cotizador_wificard')

        # Deleting model 'WifiCardBrand'
        db.rename_table('cotizador_notebookwificardbrand', 'cotizador_wificardbrand')
        
        db.rename_column('cotizador_notebook_video_port', 'notebookvideoport_id', 'videoport_id')

        # Changing field 'Notebook.wifi_card'
        db.alter_column('cotizador_notebook', 'wifi_card_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.WifiCard']))
    
    
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
        'cotizador.externalvisit': {
            'Meta': {'object_name': 'ExternalVisit'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logchangeentityprice': {
            'Meta': {'object_name': 'LogChangeEntityPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'new_price': ('django.db.models.fields.IntegerField', [], {}),
            'old_price': ('django.db.models.fields.IntegerField', [], {}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logchangeproductprice': {
            'Meta': {'object_name': 'LogChangeProductPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'new_price': ('django.db.models.fields.IntegerField', [], {}),
            'old_price': ('django.db.models.fields.IntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
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
        'cotizador.loglostentity': {
            'Meta': {'object_name': 'LogLostEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.loglostproduct': {
            'Meta': {'object_name': 'LogLostProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.lognewentity': {
            'Meta': {'object_name': 'LogNewEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logreviveentity': {
            'Meta': {'object_name': 'LogReviveEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.logreviveproduct': {
            'Meta': {'object_name': 'LogReviveProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.mailchangeproductprice': {
            'Meta': {'object_name': 'MailChangeProductPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogChangeProductPrice']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.maillostproduct': {
            'Meta': {'object_name': 'MailLostProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogLostProduct']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.mailreviveproduct': {
            'Meta': {'object_name': 'MailReviveProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogReviveProduct']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.notebook': {
            'Meta': {'object_name': 'Notebook', '_ormbases': ['cotizador.Product']},
            'battery_cells': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mah': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mv': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mwh': ('django.db.models.fields.IntegerField', [], {}),
            'card_reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookCardReader']"}),
            'chipset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookChipset']"}),
            'has_bluetooth': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_esata': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_fingerprint_reader': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_firewire': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'is_ram_dual_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'lan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookLan']"}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookLine']"}),
            'ntype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookType']"}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystem']"}),
            'optical_drive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOpticalDrive']"}),
            'power_adapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookPowerAdapter']"}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessor']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'ram_frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookRamFrequency']"}),
            'ram_quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookRamQuantity']"}),
            'ram_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookRamType']"}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreen']"}),
            'storage_drive': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.NotebookStorageDrive']", 'symmetrical': 'False'}),
            'thickness': ('django.db.models.fields.IntegerField', [], {}),
            'usb_port_count': ('django.db.models.fields.IntegerField', [], {}),
            'video_card': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.NotebookVideoCard']", 'symmetrical': 'False'}),
            'video_port': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.NotebookVideoPort']", 'symmetrical': 'False'}),
            'webcam_mp': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'weight': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {}),
            'wifi_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookWifiCard']"})
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
        'cotizador.notebookchipset': {
            'Meta': {'object_name': 'NotebookChipset'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookChipsetBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookchipsetbrand': {
            'Meta': {'object_name': 'NotebookChipsetBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebooklan': {
            'Meta': {'object_name': 'NotebookLan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookline': {
            'Meta': {'object_name': 'NotebookLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystem': {
            'Meta': {'object_name': 'NotebookOperatingSystem'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystemFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_64_bit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystemLanguage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystembrand': {
            'Meta': {'object_name': 'NotebookOperatingSystemBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystemfamily': {
            'Meta': {'object_name': 'NotebookOperatingSystemFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystemBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystemlanguage': {
            'Meta': {'object_name': 'NotebookOperatingSystemLanguage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookopticaldrive': {
            'Meta': {'object_name': 'NotebookOpticalDrive'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookpoweradapter': {
            'Meta': {'object_name': 'NotebookPowerAdapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessor': {
            'Meta': {'object_name': 'NotebookProcessor'},
            'cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorCache']"}),
            'consumption': ('django.db.models.fields.IntegerField', [], {}),
            'core_number': ('django.db.models.fields.IntegerField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFamily']"}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFrequency']"}),
            'fsb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFSB']"}),
            'has_smp': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_turbo_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorLine']"}),
            'max_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'min_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'multiplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorMultiplier']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorSocket']"}),
            'speed_score': ('django.db.models.fields.IntegerField', [], {}),
            'tdp': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        },
        'cotizador.notebookprocessorbrand': {
            'Meta': {'object_name': 'NotebookProcessorBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookprocessorcache': {
            'Meta': {'object_name': 'NotebookProcessorCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorfamily': {
            'Meta': {'object_name': 'NotebookProcessorFamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorManufacturing']"})
        },
        'cotizador.notebookprocessorfrequency': {
            'Meta': {'object_name': 'NotebookProcessorFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorfsb': {
            'Meta': {'object_name': 'NotebookProcessorFSB'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorline': {
            'Meta': {'object_name': 'NotebookProcessorLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorLineFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookprocessorlinefamily': {
            'Meta': {'object_name': 'NotebookProcessorLineFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.notebookprocessormanufacturing': {
            'Meta': {'object_name': 'NotebookProcessorManufacturing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessormultiplier': {
            'Meta': {'object_name': 'NotebookProcessorMultiplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookprocessorsocket': {
            'Meta': {'object_name': 'NotebookProcessorSocket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincount': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookramfrequency': {
            'Meta': {'object_name': 'NotebookRamFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookramquantity': {
            'Meta': {'object_name': 'NotebookRamQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookramtype': {
            'Meta': {'object_name': 'NotebookRamType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookscreen': {
            'Meta': {'object_name': 'NotebookScreen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_glossy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_led': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_rotating': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_touchscreen': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenResolution']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenSize']"})
        },
        'cotizador.notebookscreenresolution': {
            'Meta': {'object_name': 'NotebookScreenResolution'},
            'horizontal': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vertical': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookscreensize': {
            'Meta': {'object_name': 'NotebookScreenSize'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenSizeFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookscreensizefamily': {
            'Meta': {'object_name': 'NotebookScreenSizeFamily'},
            'base_size': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookstoragedrive': {
            'Meta': {'object_name': 'NotebookStorageDrive'},
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveCapacity']"}),
            'drive_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_speed': ('django.db.models.fields.IntegerField', [], {}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveRpm']"}),
            'write_speed': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedrivecapacity': {
            'Meta': {'object_name': 'NotebookStorageDriveCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedriverpm': {
            'Meta': {'object_name': 'NotebookStorageDriveRpm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedrivetype': {
            'Meta': {'object_name': 'NotebookStorageDriveType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        'cotizador.notebookvideocard': {
            'Meta': {'object_name': 'NotebookVideoCard'},
            'card_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookVideoCardType']"}),
            'gpu_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookVideoCardLine']"}),
            'memory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookVideoCardMemory']"}),
            'memory_frequency': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'speed_score': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookvideocardbrand': {
            'Meta': {'object_name': 'NotebookVideoCardBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookvideocardline': {
            'Meta': {'object_name': 'NotebookVideoCardLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookVideoCardBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookvideocardmemory': {
            'Meta': {'object_name': 'NotebookVideoCardMemory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookvideocardtype': {
            'Meta': {'object_name': 'NotebookVideoCardType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookvideoport': {
            'Meta': {'object_name': 'NotebookVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookwificard': {
            'Meta': {'object_name': 'NotebookWifiCard'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookWifiCardBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'norm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookWifiCardNorm']"})
        },
        'cotizador.notebookwificardbrand': {
            'Meta': {'object_name': 'NotebookWifiCardBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookwificardnorm': {
            'Meta': {'object_name': 'NotebookWifiCardNorm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.product': {
            'Meta': {'object_name': 'Product'},
            'date_added': ('django.db.models.fields.DateField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        'cotizador.productcomment': {
            'Meta': {'object_name': 'ProductComment'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'cotizador.productcomparisonlist': {
            'Meta': {'object_name': 'ProductComparisonList'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.Product']", 'symmetrical': 'False'})
        },
        'cotizador.productpicture': {
            'Meta': {'object_name': 'ProductPicture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'cotizador.productpricechange': {
            'Meta': {'object_name': 'ProductPriceChange'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.productsubscription': {
            'Meta': {'object_name': 'ProductSubscription'},
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cotizador.productvisit': {
            'Meta': {'object_name': 'ProductVisit'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.searchregistry': {
            'Meta': {'object_name': 'SearchRegistry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {})
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
            'prevent_availability_change': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']", 'null': 'True', 'blank': 'True'}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']", 'null': 'True', 'blank': 'True'}),
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
            'shp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProduct']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.storeproducthistory': {
            'Meta': {'object_name': 'StoreProductHistory'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'registry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'assigned_store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']", 'null': 'True', 'blank': 'True'}),
            'change_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'confirmation_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['cotizador']

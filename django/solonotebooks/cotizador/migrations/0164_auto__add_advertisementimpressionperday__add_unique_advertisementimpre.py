# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AdvertisementImpressionPerDay'
        db.create_table('cotizador_advertisementimpressionperday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('advertisement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cotizador.Advertisement'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cotizador', ['AdvertisementImpressionPerDay'])

        # Adding unique constraint on 'AdvertisementImpressionPerDay', fields ['advertisement', 'date']
        db.create_unique('cotizador_advertisementimpressionperday', ['advertisement_id', 'date'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AdvertisementImpressionPerDay', fields ['advertisement', 'date']
        db.delete_unique('cotizador_advertisementimpressionperday', ['advertisement_id', 'date'])

        # Deleting model 'AdvertisementImpressionPerDay'
        db.delete_table('cotizador_advertisementimpressionperday')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.AdvertisementPosition']"}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']", 'null': 'True'}),
            'target_url': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.advertisementimpression': {
            'Meta': {'ordering': "['-date']", 'object_name': 'AdvertisementImpression'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Advertisement']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.advertisementimpressionperday': {
            'Meta': {'ordering': "['-date']", 'unique_together': "(('advertisement', 'date'),)", 'object_name': 'AdvertisementImpressionPerDay'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Advertisement']"}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.advertisementposition': {
            'Meta': {'object_name': 'AdvertisementPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.advertisementvisit': {
            'Meta': {'object_name': 'AdvertisementVisit'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Advertisement']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referer_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cell': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Cell', '_ormbases': ['cotizador.Product']},
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Cellphone']"}),
            'pricing': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.CellPricing']", 'unique': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        'cotizador.cellcompany': {
            'Meta': {'ordering': "['store']", 'object_name': 'CellCompany'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"})
        },
        'cotizador.cellphone': {
            'Meta': {'ordering': "['manufacturer', 'name']", 'object_name': 'Cellphone'},
            'battery': ('django.db.models.fields.IntegerField', [], {}),
            'camera': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneCamera']"}),
            'card_reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneCardReader']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneCategory']"}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'form_factor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneFormFactor']"}),
            'graphics': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneGraphics']", 'null': 'True', 'blank': 'True'}),
            'has_3g': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_bluetooth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_gps': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_headphones_output': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_wifi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_memory': ('django.db.models.fields.IntegerField', [], {}),
            'keyboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneKeyboard']"}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneManufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneOperatingSystem']"}),
            'plays_mp3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneProcessor']", 'null': 'True', 'blank': 'True'}),
            'ram': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneRam']"}),
            'records_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneScreen']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.cellphonecamera': {
            'Meta': {'ordering': "['mp']", 'object_name': 'CellphoneCamera'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.cellphonecardreader': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneCardReader'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphonecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphoneformfactor': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneFormFactor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphonegraphics': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneGraphics'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphonekeyboard': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneKeyboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphonemanufacturer': {
            'Meta': {'ordering': "['brand']", 'object_name': 'CellphoneManufacturer'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.cellphoneoperatingsystem': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneOperatingSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphoneprocessor': {
            'Meta': {'ordering': "['name']", 'object_name': 'CellphoneProcessor'},
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellphoneram': {
            'Meta': {'ordering': "['value']", 'object_name': 'CellphoneRam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.cellphonescreen': {
            'Meta': {'ordering': "['size', 'resolution']", 'object_name': 'CellphoneScreen'},
            'colors': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneScreenColors']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_touch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneScreenResolution']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellphoneScreenSize']"})
        },
        'cotizador.cellphonescreencolors': {
            'Meta': {'ordering': "['quantity']", 'object_name': 'CellphoneScreenColors'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.cellphonescreenresolution': {
            'Meta': {'ordering': "['total_pixels']", 'object_name': 'CellphoneScreenResolution'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_pixels': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.cellphonescreensize': {
            'Meta': {'ordering': "['value']", 'object_name': 'CellphoneScreenSize'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'})
        },
        'cotizador.cellpricing': {
            'Meta': {'ordering': "['company', 'name']", 'object_name': 'CellPricing'},
            'best_tier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellPricingTier']", 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellCompany']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.cellpricingplan': {
            'Meta': {'ordering': "['ordering', 'id']", 'object_name': 'CellPricingPlan'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellCompany']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'includes_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.cellpricingtier': {
            'Meta': {'ordering': "['pricing', 'plan']", 'object_name': 'CellPricingTier'},
            'cellphone_price': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_quota': ('django.db.models.fields.IntegerField', [], {}),
            'ordering_cellphone_price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'ordering_six_month_price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'ordering_three_month_price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'ordering_twelve_month_price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellPricingPlan']"}),
            'pricing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.CellPricing']"}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']", 'null': 'True', 'blank': 'True'}),
            'six_month_pricing': ('django.db.models.fields.IntegerField', [], {}),
            'three_month_pricing': ('django.db.models.fields.IntegerField', [], {}),
            'twelve_month_pricing': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.computercase': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'ComputerCase', '_ormbases': ['cotizador.Product']},
            'bottom_fan_slots': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bfs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ComputerCaseBrand']"}),
            'external_3_1_2_bays': ('django.db.models.fields.IntegerField', [], {}),
            'external_5_1_4_bays': ('django.db.models.fields.IntegerField', [], {}),
            'front_usb_ports': ('django.db.models.fields.IntegerField', [], {}),
            'frontal_fan_slots': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ffs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'has_front_audio_ports': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_front_esata_port': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_front_firewire_port': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_motherboard_tray': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'included_fans': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'if'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'internal_2_1_2_bays': ('django.db.models.fields.IntegerField', [], {}),
            'internal_3_1_2_bays': ('django.db.models.fields.IntegerField', [], {}),
            'largest_motherboard_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ComputerCaseMotherboardFormat']"}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'power_supply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ComputerCasePowerSupply']"}),
            'power_supply_position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ComputerCasePowerSupplyPosition']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'rear_expansion_slots': ('django.db.models.fields.IntegerField', [], {}),
            'rear_fan_slots': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rfs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'side_fan_slots': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sfs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'top_fan_slots': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tfs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cotizador.ComputerCaseFanDistribution']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.computercasebrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'ComputerCaseBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.computercasefan': {
            'Meta': {'ordering': "['mm']", 'object_name': 'ComputerCaseFan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mm': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.computercasefandistribution': {
            'Meta': {'ordering': "['fan', 'quantity']", 'object_name': 'ComputerCaseFanDistribution'},
            'fan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ComputerCaseFan']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.computercasemotherboardformat': {
            'Meta': {'object_name': 'ComputerCaseMotherboardFormat'},
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMotherboardFormat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.computercasepowersupply': {
            'Meta': {'ordering': "['power']", 'object_name': 'ComputerCasePowerSupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.computercasepowersupplyposition': {
            'Meta': {'ordering': "['name']", 'object_name': 'ComputerCasePowerSupplyPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.externalvisit': {
            'Meta': {'object_name': 'ExternalVisit'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.interfacebrand': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacebus': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceBus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacecardbus': {
            'Meta': {'ordering': "['name', 'version', 'lane']", 'object_name': 'InterfaceCardBus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceCardBusLane']"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceCardBusName']"}),
            'version': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'})
        },
        'cotizador.interfacecardbuslane': {
            'Meta': {'ordering': "['value']", 'object_name': 'InterfaceCardBusLane'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.interfacecardbusname': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceCardBusName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'show_version_and_lanes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cotizador.interfacememorybus': {
            'Meta': {'ordering': "['format', 'type']", 'object_name': 'InterfaceMemoryBus'},
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMemoryFormat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pincount': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMemoryType']"})
        },
        'cotizador.interfacememoryformat': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceMemoryFormat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacememorytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceMemoryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacemotherboardformat': {
            'Meta': {'object_name': 'InterfaceMotherboardFormat'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.interfaceport': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfacePort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacepowerconnector': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfacePowerConnector'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.interfacesocket': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'InterfaceSocket'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceSocketBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_pins': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.interfacesocketbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'InterfaceSocketBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.interfacevideoport': {
            'Meta': {'ordering': "['name']", 'object_name': 'InterfaceVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.logchangeentityname': {
            'Meta': {'object_name': 'LogChangeEntityName'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        'cotizador.logfetchstoreerror': {
            'Meta': {'object_name': 'LogFetchStoreError'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogEntry']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"})
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
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cotizador.maillostproduct': {
            'Meta': {'object_name': 'MailLostProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogLostProduct']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cotizador.mailreviveproduct': {
            'Meta': {'object_name': 'MailReviveProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.LogReviveProduct']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductSubscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cotizador.motherboard': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Motherboard', '_ormbases': ['cotizador.Product']},
            'allows_cf': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allows_raid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allows_sli': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'audio_channels': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardAudioChannels']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardBrand']"}),
            'buses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.MotherboardHasBus']", 'symmetrical': 'False'}),
            'card_buses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.MotherboardHasCardBus']", 'symmetrical': 'False'}),
            'chipset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardChipset']"}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardFormat']"}),
            'memory_channels': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardMemoryChannel']"}),
            'memory_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.MotherboardHasMemoryType']", 'symmetrical': 'False'}),
            'ports': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.MotherboardHasPort']", 'symmetrical': 'False'}),
            'power_connectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.MotherboardHasPowerConnector']", 'symmetrical': 'False'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'video_ports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cotizador.MotherboardHasVideoPort']", 'null': 'True', 'blank': 'True'})
        },
        'cotizador.motherboardaudiochannels': {
            'Meta': {'ordering': "['name']", 'object_name': 'MotherboardAudioChannels'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.motherboardbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'MotherboardBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardbus': {
            'Meta': {'ordering': "['bus']", 'object_name': 'MotherboardBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardcardbus': {
            'Meta': {'ordering': "['bus']", 'object_name': 'MotherboardCardBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceCardBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardchipset': {
            'Meta': {'ordering': "['northbridge']", 'object_name': 'MotherboardChipset'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'northbridge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardNorthbridge']"}),
            'southbridge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardSouthbridge']"})
        },
        'cotizador.motherboardchipsetbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'MotherboardChipsetBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardformat': {
            'Meta': {'object_name': 'MotherboardFormat'},
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMotherboardFormat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardgraphics': {
            'Meta': {'ordering': "['name']", 'object_name': 'MotherboardGraphics'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.motherboardhasbus': {
            'Meta': {'ordering': "['bus', 'quantity']", 'object_name': 'MotherboardHasBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardhascardbus': {
            'Meta': {'ordering': "['bus', 'quantity']", 'object_name': 'MotherboardHasCardBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardCardBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardhasmemorytype': {
            'Meta': {'ordering': "['mtype']", 'object_name': 'MotherboardHasMemoryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardMemoryType']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardhasport': {
            'Meta': {'ordering': "['port', 'quantity']", 'object_name': 'MotherboardHasPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardPort']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardhaspowerconnector': {
            'Meta': {'ordering': "['connector', 'quantity']", 'object_name': 'MotherboardHasPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardPowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardhasvideoport': {
            'Meta': {'ordering': "['port', 'quantity']", 'object_name': 'MotherboardHasVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardVideoPort']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardmemorychannel': {
            'Meta': {'ordering': "['value']", 'object_name': 'MotherboardMemoryChannel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.motherboardmemorytype': {
            'Meta': {'ordering': "['itype']", 'object_name': 'MotherboardMemoryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMemoryBus']", 'null': 'True', 'blank': 'True'})
        },
        'cotizador.motherboardnorthbridge': {
            'Meta': {'ordering': "['family']", 'object_name': 'MotherboardNorthbridge'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardNorthbridgeFamily']"}),
            'graphics': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardGraphics']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.motherboardnorthbridgefamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'MotherboardNorthbridgeFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardChipsetBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.MotherboardSocket']"})
        },
        'cotizador.motherboardport': {
            'Meta': {'ordering': "['port']", 'object_name': 'MotherboardPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfacePort']"})
        },
        'cotizador.motherboardpowerconnector': {
            'Meta': {'ordering': "['connector']", 'object_name': 'MotherboardPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfacePowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.motherboardsocket': {
            'Meta': {'ordering': "['socket']", 'object_name': 'MotherboardSocket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceSocket']"})
        },
        'cotizador.motherboardsouthbridge': {
            'Meta': {'object_name': 'MotherboardSouthbridge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.motherboardvideoport': {
            'Meta': {'ordering': "['port']", 'object_name': 'MotherboardVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceVideoPort']"})
        },
        'cotizador.notebook': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Notebook', '_ormbases': ['cotizador.Product']},
            'battery_cells': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mah': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mv': ('django.db.models.fields.IntegerField', [], {}),
            'battery_mwh': ('django.db.models.fields.IntegerField', [], {}),
            'card_reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookCardReader']"}),
            'chipset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookChipset']"}),
            'has_bluetooth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_esata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_fingerprint_reader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_firewire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'is_ram_dual_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookcardreader': {
            'Meta': {'ordering': "['name']", 'object_name': 'NotebookCardReader'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookchipset': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'NotebookChipset'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookChipsetBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookchipsetbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookChipsetBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebooklan': {
            'Meta': {'object_name': 'NotebookLan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookline': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'NotebookLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystem': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'NotebookOperatingSystem'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystemFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_64_bit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookOperatingSystemLanguage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookoperatingsystembrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookOperatingSystemBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookoperatingsystemfamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'NotebookOperatingSystemFamily'},
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
            'Meta': {'ordering': "['power']", 'object_name': 'NotebookPowerAdapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessor': {
            'Meta': {'ordering': "('line', 'name')", 'object_name': 'NotebookProcessor'},
            'cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorCache']"}),
            'consumption': ('django.db.models.fields.IntegerField', [], {}),
            'core_number': ('django.db.models.fields.IntegerField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFamily']"}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFrequency']"}),
            'fsb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorFSB']"}),
            'has_smp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_turbo_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookProcessorBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookprocessorcache': {
            'Meta': {'ordering': "('value',)", 'object_name': 'NotebookProcessorCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorfamily': {
            'Meta': {'ordering': "['name']", 'object_name': 'NotebookProcessorFamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorManufacturing']"})
        },
        'cotizador.notebookprocessorfrequency': {
            'Meta': {'ordering': "('value',)", 'object_name': 'NotebookProcessorFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorfsb': {
            'Meta': {'ordering': "('value',)", 'object_name': 'NotebookProcessorFSB'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessorline': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'NotebookProcessorLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorLineFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookprocessorlinefamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'NotebookProcessorLineFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookProcessorBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.notebookprocessormanufacturing': {
            'Meta': {'ordering': "['value']", 'object_name': 'NotebookProcessorManufacturing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookprocessormultiplier': {
            'Meta': {'ordering': "['value']", 'object_name': 'NotebookProcessorMultiplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookprocessorsocket': {
            'Meta': {'ordering': "['name']", 'object_name': 'NotebookProcessorSocket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pincount': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookramfrequency': {
            'Meta': {'ordering': "('value',)", 'object_name': 'NotebookRamFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookramquantity': {
            'Meta': {'ordering': "['value']", 'object_name': 'NotebookRamQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookramtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'NotebookRamType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookscreen': {
            'Meta': {'ordering': "['size', 'resolution']", 'object_name': 'NotebookScreen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_glossy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_led': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rotating': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_touchscreen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenResolution']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenSize']"})
        },
        'cotizador.notebookscreenresolution': {
            'Meta': {'ordering': "('horizontal', 'vertical')", 'object_name': 'NotebookScreenResolution'},
            'horizontal': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vertical': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookscreensize': {
            'Meta': {'ordering': "('size',)", 'object_name': 'NotebookScreenSize'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookScreenSizeFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.notebookscreensizefamily': {
            'Meta': {'ordering': "('base_size',)", 'object_name': 'NotebookScreenSizeFamily'},
            'base_size': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookstoragedrive': {
            'Meta': {'ordering': "['drive_type', 'capacity', 'rpm']", 'object_name': 'NotebookStorageDrive'},
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveCapacity']"}),
            'drive_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_speed': ('django.db.models.fields.IntegerField', [], {}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookStorageDriveRpm']"}),
            'write_speed': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedrivecapacity': {
            'Meta': {'ordering': "['value']", 'object_name': 'NotebookStorageDriveCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedriverpm': {
            'Meta': {'ordering': "['value']", 'object_name': 'NotebookStorageDriveRpm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.notebookstoragedrivetype': {
            'Meta': {'object_name': 'NotebookStorageDriveType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebooktype': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NotebookType'},
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
            'Meta': {'ordering': "['line', 'name']", 'object_name': 'NotebookVideoCard'},
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
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookVideoCardBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookvideocardline': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'NotebookVideoCardLine'},
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
            'Meta': {'ordering': "['name']", 'object_name': 'NotebookVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.notebookwificard': {
            'Meta': {'ordering': "['brand', 'name', 'norm']", 'object_name': 'NotebookWifiCard'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookWifiCardBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'norm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.NotebookWifiCardNorm']"})
        },
        'cotizador.notebookwificardbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'NotebookWifiCardBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.notebookwificardnorm': {
            'Meta': {'object_name': 'NotebookWifiCardNorm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.powersupply': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'PowerSupply', '_ormbases': ['cotizador.Product']},
            'certification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplyCertification']"}),
            'currents_on_12V_rails': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'currents_on_33V_rails': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'currents_on_5V_rails': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'has_active_pfc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_modular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplyLine']"}),
            'power': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplyPower']"}),
            'power_connectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.PowerSupplyHasPowerConnector']", 'symmetrical': 'False'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplySize']"})
        },
        'cotizador.powersupplybrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'PowerSupplyBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.powersupplycertification': {
            'Meta': {'ordering': "['value']", 'object_name': 'PowerSupplyCertification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.powersupplyhaspowerconnector': {
            'Meta': {'ordering': "['connector', 'quantity']", 'object_name': 'PowerSupplyHasPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplyPowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.powersupplyline': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'PowerSupplyLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.PowerSupplyBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.powersupplypower': {
            'Meta': {'ordering': "['value']", 'object_name': 'PowerSupplyPower'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.powersupplypowerconnector': {
            'Meta': {'ordering': "['connector']", 'object_name': 'PowerSupplyPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfacePowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.powersupplysize': {
            'Meta': {'ordering': "['name']", 'object_name': 'PowerSupplySize'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processor': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Processor', '_ormbases': ['cotizador.Product']},
            'core': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorCore']"}),
            'core_count': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorCoreCount']"}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            'fsb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorFsb']"}),
            'graphics': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorGraphics']"}),
            'has_smp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_unlocked_multiplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_vt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_64_bit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'l2_cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorL2Cache']"}),
            'l3_cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorL3Cache']"}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorLine']"}),
            'max_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'min_voltage': ('django.db.models.fields.IntegerField', [], {}),
            'multiplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorMultiplier']"}),
            'passmark_score': ('django.db.models.fields.IntegerField', [], {}),
            'pcmark_05_score': ('django.db.models.fields.IntegerField', [], {}),
            'pcmark_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pcmark_vantage_score': ('django.db.models.fields.IntegerField', [], {}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorSocket']"}),
            'tdp': ('django.db.models.fields.IntegerField', [], {}),
            'turbo_modes': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'})
        },
        'cotizador.processorarchitecture': {
            'Meta': {'ordering': "['brand']", 'object_name': 'ProcessorArchitecture'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'turbo_step': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'ProcessorBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.processorcore': {
            'Meta': {'ordering': "['architecture', 'name']", 'object_name': 'ProcessorCore'},
            'architecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorArchitecture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturing_process': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorManufacturingProcess']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processorcorecount': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorCoreCount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorfamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'ProcessorFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'separator': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processorfsb': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorFsb'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorgraphics': {
            'Meta': {'object_name': 'ProcessorGraphics'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processorl2cache': {
            'Meta': {'ordering': "['quantity', 'multiplier']", 'object_name': 'ProcessorL2Cache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {}),
            'quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorL2CacheQuantity']"})
        },
        'cotizador.processorl2cachequantity': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorL2CacheQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorl3cache': {
            'Meta': {'ordering': "['quantity', 'multiplier']", 'object_name': 'ProcessorL3Cache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {}),
            'quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorL3CacheQuantity']"})
        },
        'cotizador.processorl3cachequantity': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorL3CacheQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processorline': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'ProcessorLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProcessorFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.processormanufacturingprocess': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorManufacturingProcess'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.processormultiplier': {
            'Meta': {'ordering': "['value']", 'object_name': 'ProcessorMultiplier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.processorsocket': {
            'Meta': {'ordering': "['socket']", 'object_name': 'ProcessorSocket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceSocket']"})
        },
        'cotizador.product': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Product'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'default': "' '"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductType']", 'null': 'True', 'blank': 'True'}),
            'review_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chosen_by'", 'null': 'True', 'to': "orm['cotizador.StoreHasProduct']"}),
            'similar_products': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "'0'", 'max_length': '30'}),
            'sponsored_shp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sponsored_product'", 'null': 'True', 'to': "orm['cotizador.StoreHasProduct']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'week_discount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week_external_visits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week_visitor_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cotizador.productcomment': {
            'Meta': {'object_name': 'ProductComment'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cotizador.producttype': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'ProductType'},
            'adminurlname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {}),
            'urlname': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.productvisit': {
            'Meta': {'object_name': 'ProductVisit'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']"})
        },
        'cotizador.ram': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Ram', '_ormbases': ['cotizador.Product']},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamBus']"}),
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamCapacity']"}),
            'is_ecc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fully_buffered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latency_cl': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamLatencyCl']", 'null': 'True', 'blank': 'True'}),
            'latency_tras': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamLatencyTras']", 'null': 'True', 'blank': 'True'}),
            'latency_trcd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamLatencyTrcd']", 'null': 'True', 'blank': 'True'}),
            'latency_trp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamLatencyTrp']", 'null': 'True', 'blank': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamLine']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'voltage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamVoltage']"})
        },
        'cotizador.rambrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'RamBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.rambus': {
            'Meta': {'ordering': "['bus', 'frequency']", 'object_name': 'RamBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamMemoryBus']"}),
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamFrequency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.ramcapacity': {
            'Meta': {'ordering': "['dimm_quantity', 'dimm_capacity']", 'object_name': 'RamCapacity'},
            'dimm_capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamDimmCapacity']"}),
            'dimm_quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamDimmQuantity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamTotalCapacity']"})
        },
        'cotizador.ramdimmcapacity': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamDimmCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramdimmquantity': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamDimmQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramfrequency': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramlatencycl': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamLatencyCl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramlatencytras': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamLatencyTras'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramlatencytrcd': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamLatencyTrcd'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramlatencytrp': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamLatencyTrp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramline': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'RamLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.RamBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.rammemorybus': {
            'Meta': {'ordering': "['bus']", 'object_name': 'RamMemoryBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceMemoryBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.ramtotalcapacity': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamTotalCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.ramvoltage': {
            'Meta': {'ordering': "['value']", 'object_name': 'RamVoltage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        },
        'cotizador.screen': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'Screen', '_ormbases': ['cotizador.Product']},
            'brightness': ('django.db.models.fields.IntegerField', [], {}),
            'consumption': ('django.db.models.fields.IntegerField', [], {}),
            'contrast': ('django.db.models.fields.IntegerField', [], {}),
            'digital_tuner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenDigitalTuner']"}),
            'display': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenDisplay']"}),
            'has_analog_tuner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_3d': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenLine']"}),
            'panel_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenPanelType']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'refresh_rate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenRefreshRate']"}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenResolution']"}),
            'response_time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenResponseTime']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenSize']"}),
            'speakers': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenSpeakers']"}),
            'stype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenType']"}),
            'usb_ports': ('django.db.models.fields.IntegerField', [], {}),
            'video_ports': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.ScreenHasVideoPort']", 'symmetrical': 'False'})
        },
        'cotizador.screenaspectratio': {
            'Meta': {'object_name': 'ScreenAspectRatio'},
            'h_value': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'v_value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screenbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'ScreenBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.screendigitaltuner': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'ScreenDigitalTuner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screendisplay': {
            'Meta': {'ordering': "['dtype']", 'object_name': 'ScreenDisplay'},
            'backlight': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenDisplayType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.screendisplaytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScreenDisplayType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.screenhasvideoport': {
            'Meta': {'ordering': "['port', 'quantity']", 'object_name': 'ScreenHasVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenVideoPort']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screenline': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'ScreenLine'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.screenpaneltype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScreenPanelType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.screenrefreshrate': {
            'Meta': {'ordering': "['value']", 'object_name': 'ScreenRefreshRate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screenresolution': {
            'Meta': {'ordering': "['-commercial_name', 'total_pixels']", 'object_name': 'ScreenResolution'},
            'aspect_ratio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenAspectRatio']"}),
            'commercial_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'h_value': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_pixels': ('django.db.models.fields.IntegerField', [], {}),
            'v_value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screenresponsetime': {
            'Meta': {'ordering': "['value']", 'object_name': 'ScreenResponseTime'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screensize': {
            'Meta': {'ordering': "['value']", 'object_name': 'ScreenSize'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ScreenSizeFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        },
        'cotizador.screensizefamily': {
            'Meta': {'ordering': "['value']", 'object_name': 'ScreenSizeFamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screenspeakers': {
            'Meta': {'ordering': "['value']", 'object_name': 'ScreenSpeakers'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.screentype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScreenType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.screenvideoport': {
            'Meta': {'ordering': "['port']", 'object_name': 'ScreenVideoPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceVideoPort']"})
        },
        'cotizador.searchregistry': {
            'Meta': {'object_name': 'SearchRegistry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.sponsoredvisit': {
            'Meta': {'ordering': "['-date']", 'object_name': 'SponsoredVisit'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProduct']"})
        },
        'cotizador.storagedrive': {
            'Meta': {'ordering': "['display_name']", 'object_name': 'StorageDrive', '_ormbases': ['cotizador.Product']},
            'buffer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveBuffer']"}),
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveBus']"}),
            'capacity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveCapacity']"}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveLine']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'random_read_speed': ('django.db.models.fields.IntegerField', [], {}),
            'random_write_speed': ('django.db.models.fields.IntegerField', [], {}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveRpm']"}),
            'sequential_read_speed': ('django.db.models.fields.IntegerField', [], {}),
            'sequential_write_speed': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveSize']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveType']"})
        },
        'cotizador.storagedrivebrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'StorageDriveBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.storagedrivebuffer': {
            'Meta': {'ordering': "['value']", 'object_name': 'StorageDriveBuffer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedrivebus': {
            'Meta': {'ordering': "['bus']", 'object_name': 'StorageDriveBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.storagedrivecapacity': {
            'Meta': {'ordering': "['value']", 'object_name': 'StorageDriveCapacity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedrivefamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'StorageDriveFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.storagedriveline': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'StorageDriveLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StorageDriveFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.storagedriverpm': {
            'Meta': {'ordering': "['value']", 'object_name': 'StorageDriveRpm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.storagedrivesize': {
            'Meta': {'ordering': "['value']", 'object_name': 'StorageDriveSize'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.storagedrivetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'StorageDriveType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.store': {
            'Meta': {'ordering': "['name']", 'object_name': 'Store'},
            'affiliate_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'sponsor_cap': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cotizador.storecustomupdateregistry': {
            'Meta': {'ordering': "['-start_datetime', 'store']", 'object_name': 'StoreCustomUpdateRegistry'},
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"})
        },
        'cotizador.storehasproduct': {
            'Meta': {'ordering': "['product']", 'object_name': 'StoreHasProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Product']", 'null': 'True', 'blank': 'True'}),
            'shpe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']", 'null': 'True', 'blank': 'True'})
        },
        'cotizador.storehasproductentity': {
            'Meta': {'object_name': 'StoreHasProductEntity'},
            'comparison_field': ('django.db.models.fields.TextField', [], {}),
            'custom_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_resolved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_price': ('django.db.models.fields.IntegerField', [], {}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'prevent_availability_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.ProductType']", 'null': 'True', 'blank': 'True'}),
            'resolved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'shp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProduct']", 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']"}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'cotizador.storeproducthistory': {
            'Meta': {'object_name': 'StoreProductHistory'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'registry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.StoreHasProductEntity']"})
        },
        'cotizador.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'assigned_store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.Store']", 'null': 'True', 'blank': 'True'}),
            'can_access_competitivity_report': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_use_extra_ordering_options': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'change_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'confirmation_mails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managed_product_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.ProductType']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'cotizador.videocard': {
            'Meta': {'ordering': "['brand', 'gpu__name', 'name']", 'object_name': 'VideoCard', '_ormbases': ['cotizador.Product']},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardBrand']"}),
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardBus']"}),
            'core_clock': ('django.db.models.fields.IntegerField', [], {}),
            'gpu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpu']"}),
            'memory_bus_width': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardMemoryBusWidth']"}),
            'memory_clock': ('django.db.models.fields.IntegerField', [], {}),
            'memory_quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardMemoryQuantity']"}),
            'memory_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardMemoryType']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cotizador.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardProfile']"}),
            'refrigeration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardRefrigeration']"}),
            'shader_clock': ('django.db.models.fields.IntegerField', [], {}),
            'slot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardSlotType']"}),
            'video_ports': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cotizador.VideoCardHasPort']", 'symmetrical': 'False'})
        },
        'cotizador.videocardbrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'VideoCardBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.videocardbus': {
            'Meta': {'ordering': "['bus']", 'object_name': 'VideoCardBus'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceCardBus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.videocardgpu': {
            'Meta': {'ordering': "['line__family', 'name']", 'object_name': 'VideoCardGpu'},
            'core': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuCore']"}),
            'core_count': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuCoreCount']"}),
            'default_core_clock': ('django.db.models.fields.IntegerField', [], {}),
            'default_memory_clock': ('django.db.models.fields.IntegerField', [], {}),
            'default_shader_clock': ('django.db.models.fields.IntegerField', [], {}),
            'dx_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuDirectxVersion']"}),
            'has_multi_gpu_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuLine']"}),
            'manufacturing_process': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuManufacturingProcess']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ogl_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuOpenglVersion']"}),
            'power_conns': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cotizador.VideoCardHasPowerConnector']", 'null': 'True', 'blank': 'True'}),
            'rops': ('django.db.models.fields.IntegerField', [], {}),
            'stream_processors': ('django.db.models.fields.IntegerField', [], {}),
            'tdmark_06_score': ('django.db.models.fields.IntegerField', [], {}),
            'tdmark_11_score': ('django.db.models.fields.IntegerField', [], {}),
            'tdmark_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tdmark_vantage_score': ('django.db.models.fields.IntegerField', [], {}),
            'tdp': ('django.db.models.fields.IntegerField', [], {}),
            'texture_units': ('django.db.models.fields.IntegerField', [], {}),
            'transistor_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardgpuarchitecture': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'VideoCardGpuArchitecture'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardgpubrand': {
            'Meta': {'ordering': "['brand']", 'object_name': 'VideoCardGpuBrand'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.videocardgpucore': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'VideoCardGpuCore'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuCoreFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardgpucorecount': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardGpuCoreCount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardgpucorefamily': {
            'Meta': {'ordering': "['architecture', 'name']", 'object_name': 'VideoCardGpuCoreFamily'},
            'architecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuArchitecture']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardgpudirectxversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardGpuDirectxVersion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'})
        },
        'cotizador.videocardgpufamily': {
            'Meta': {'ordering': "['brand', 'name']", 'object_name': 'VideoCardGpuFamily'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuBrand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardgpuline': {
            'Meta': {'ordering': "['family', 'name']", 'object_name': 'VideoCardGpuLine'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardGpuFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardgpumanufacturingprocess': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardGpuManufacturingProcess'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardgpuopenglversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardGpuOpenglVersion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'})
        },
        'cotizador.videocardhasport': {
            'Meta': {'ordering': "['port', 'quantity']", 'object_name': 'VideoCardHasPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardPort']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardhaspowerconnector': {
            'Meta': {'ordering': "['connector', 'quantity']", 'object_name': 'VideoCardHasPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.VideoCardPowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardmemorybuswidth': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardMemoryBusWidth'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardmemoryquantity': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardMemoryQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'cotizador.videocardmemorytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'VideoCardMemoryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardport': {
            'Meta': {'ordering': "['port']", 'object_name': 'VideoCardPort'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfaceVideoPort']"})
        },
        'cotizador.videocardpowerconnector': {
            'Meta': {'ordering': "['connector']", 'object_name': 'VideoCardPowerConnector'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cotizador.InterfacePowerConnector']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cotizador.videocardprofile': {
            'Meta': {'ordering': "['name']", 'object_name': 'VideoCardProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardrefrigeration': {
            'Meta': {'ordering': "['name']", 'object_name': 'VideoCardRefrigeration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cotizador.videocardslottype': {
            'Meta': {'ordering': "['value']", 'object_name': 'VideoCardSlotType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['cotizador']

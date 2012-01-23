from django.db import models
from solonotebooks.cotizador.models.storage_drive_buffer import StorageDriveBuffer
from solonotebooks.cotizador.models.storage_drive_bus import StorageDriveBus
from solonotebooks.cotizador.models.storage_drive_capacity import StorageDriveCapacity
from solonotebooks.cotizador.models.storage_drive_line import StorageDriveLine
from solonotebooks.cotizador.models.storage_drive_rpm import StorageDriveRpm
from solonotebooks.cotizador.models.storage_drive_size import StorageDriveSize
from solonotebooks.cotizador.models.storage_drive_type import StorageDriveType
from solonotebooks.cotizador.models.product import Product

class StorageDrive(Product):
    type = models.ForeignKey(StorageDriveType)
    line = models.ForeignKey(StorageDriveLine)
    capacity = models.ForeignKey(StorageDriveCapacity)
    rpm = models.ForeignKey(StorageDriveRpm)
    size = models.ForeignKey(StorageDriveSize)
    bus = models.ForeignKey(StorageDriveBus)
    buffer = models.ForeignKey(StorageDriveBuffer)

    sequential_read_speed = models.IntegerField()
    sequential_write_speed = models.IntegerField()
    random_read_speed = models.IntegerField()
    random_write_speed = models.IntegerField()
    
    def get_display_name(self):
        result = '%s %s' % (unicode(self.line), unicode(self.capacity))
        if self.name != ' ':
            result += ' (%s)' % self.name
        else:
            result += ' (%s, %s, %s)' % (unicode(self.size), unicode(self.rpm), unicode(self.bus))
        return result
        
    def raw_text(self):
        return super(StorageDrive, self).base_raw_text()
        
    def load_similar_products(self):
        self.similar_products = ''

    class Meta:
        ordering = ['display_name']
        app_label = 'cotizador'
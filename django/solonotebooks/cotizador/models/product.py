import operator
from datetime import date, timedelta
from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import *
from utils import prettyPrice

class Product(models.Model):
    name = models.CharField(max_length = 255)
    display_name = models.CharField(max_length = 255)
    date_added = models.DateField()
    is_available = models.BooleanField()
    
    publicized_offer = models.ForeignKey('StoreHasProductEntity', null = True, blank = True, related_name = 'ntbk')
    min_price = models.IntegerField()
    week_visitor_count = models.IntegerField()
    week_discount = models.IntegerField()    
    
    other = models.TextField()
    long_description = models.TextField()

    similar_notebooks = models.CommaSeparatedIntegerField(max_length = 30)
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (88, 88), },
        extra_thumbnails = {
            'large': {'size': (300, 300)},
            'gallery_thumb': {'size': (90, 90)},
        },                                          
        upload_to = 'notebook_pics',
        generate_on_save = True,)
        
    def __unicode__(self):
        return self.display_name
        
    def pretty_min_price(self):
        return prettyPrice(self.min_price)

    def normalize(self):
        new_price = self.storehasproduct_set.all().filter(is_available = True).filter(is_hidden = False).aggregate(Min('latest_price'))['latest_price__min']
        
        if new_price:
            print 'El notebook tiene registros de disponibilidad'
            
            log_price_change = True
            if not self.is_available:
                LogReviveNotebook.new(notebook).send_notification_mails()
                log_price_change = False
            
            if new_price != self.min_price:
                if log_price_change:
                    LogChangeNotebookPrice.new(notebook, self.min_price, new_price).send_notification_mails()
                npc = NotebookPriceChange()
                npc.notebook = notebook
                npc.price = new_price
                npc.date = date.today()
                npc.save()
                self.min_price = new_price

            self.is_available = True
        else:
            print 'El notebook no tiene registros de disponibilidad'

            if self.is_available:
                LogLostNotebook.new(notebook).send_notification_mails()
                self.is_available = False
            
        npcs = self.notebookpricechange_set.all()
        if len(npcs) == 0:
            npc = NotebookPriceChange()
            npc.notebook = notebook
            npc.price = self.min_price
            npc.date = date.today()
            npc.save()
            
        try:     
            self.publicized_offer = self.storehasproduct_set.filter(is_publicized = True, is_available = True).order_by('latest_price')[0]
        except IndexError:
            self.publicized_offer = None
            
        self.long_description = self.rawText()
        self.save()
        
        
        #similar_notebooks = [str(ntbk.id) for ntbk in self.findSimilarNotebooks()]
        #self.similar_notebooks = ','.join(similar_notebooks)
        
    def create_miniature(self):
        return { 
            'name': str(self),
            'min_price': self.min_price,
            'url': '/notebooks/' + str(self.id)
        }
        
    def price_at(self, date):
        from . import NotebookPriceChange
    
        npc = NotebookPriceChange.objects.filter(notebook = self).filter(date__lte = date).order_by('-date')
        if npc:
            return npc[0].price
        else:
            return self.min_price
        
    def update_week_discount(self):
        t = date.today()
        d = timedelta(days = 7)
        old_price = self.price_at(t - d)
        try:
            self.week_discount = int(100 * (old_price - self.min_price) / old_price)
        except:
            self.week_discount = 0;
            
    def update_week_visits(self):
        t = date.today()
        d = timedelta(days = 7)
        self.week_visitor_count = len(self.notebookvisit_set.filter(date__gte = t - d))
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product'
        ordering = ['name']       
        

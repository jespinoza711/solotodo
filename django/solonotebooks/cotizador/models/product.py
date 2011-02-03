#-*- coding: UTF-8 -*-
import operator
from datetime import date, timedelta
from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import *
from utils import prettyPrice
from solonotebooks import settings

class Product(models.Model):
    name = models.CharField(max_length = 255)
    date_added = models.DateField()
    is_available = models.BooleanField()
    
    publicized_offer = models.ForeignKey('StoreHasProductEntity', null = True, blank = True, related_name = 'ntbk')
    ptype = models.ForeignKey(ProductType)
    
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
    
    def get_polymorphic_instance(self):
        from solonotebooks.cotizador.models import *
        c = eval(self.ptype.classname)
        return c.objects.get(pk = self.id) 
        
    def __unicode__(self):
        entity = self.get_polymorphic_instance()
        return self.ptype.classname + ' - ' + unicode(entity)
        
    def raw_text(self):
        entity = self.get_polymorphic_instance()
        return entity.raw_text()
        
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
        from . import ProductPriceChange
    
        ppc = ProductPriceChange.objects.filter(notebook = self).filter(date__lte = date).order_by('-date')
        if ppc:
            return ppc[0].price
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
        self.week_visitor_count = len(self.productvisit_set.filter(date__gte = t - d))
        
    def generate_chart(self):
        import cairo
        import pycha.line
        from copy import deepcopy
        from . import ProductPriceChange

        ppcs = ProductPriceChange.objects.filter(notebook = self).order_by('date')
        min_price = ppcs.aggregate(Min('price'))['price__min']
        max_price = ppcs.aggregate(Max('price'))['price__max'] 
        indexed_ppcs = [[i, ppcs[i]] for i in range(len(ppcs))]
        
        last_ppc = indexed_ppcs[len(indexed_ppcs) - 1][1]
        new_ppc = deepcopy(last_ppc)
        new_ppc.date = date.today()
        indexed_ppcs += [[len(indexed_ppcs), new_ppc]]

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 300)
        lines = [[ippc[0], ippc[1].price] for ippc in indexed_ppcs]
            
        dataSet = (
            ('lines', [(k, v) for k, v in lines]),
            )

        options = {
            'axis': {
                'x': {
                    #'ticks': ['' for inpc in indexed_npcs],
                },
                'y': {
                    'tickCount': 4,
                    'range': (min_price / 1.3, max_price * 1.2)
                }
            },
            'background': {
                'color': '#eeeeff',
                'lineColor': '#444444',
                'baseColor': '#FFFFFF',
            },
            'colorScheme': {
                'name': 'gradient',
                'args': {
                    'initialColor': 'blue',
                },
            },
            'legend': {
                'hide': True,
            },
            'padding': {
                'left': 60,
                'bottom': 20,
                'right': 10,
            },
            'title': 'Cambios de precio a la fecha'
        }
        chart = pycha.line.LineChart(surface, options)

        chart.addDataset(dataSet)
        chart.render()

        surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + str(self.id) + '.png')
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product'
        ordering = ['name']       
        

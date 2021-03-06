#-*- coding: UTF-8 -*-
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.db import models
from django.db.models import Min, Max
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import *
from copy import deepcopy
from utils import prettyPrice
from solonotebooks import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def count_decimals(value):
    """
    Returns the number of decimals in a Decimal value
    e.g.; count_decimals(Decimal("1234.56")) = 2
    """
    return abs(value.as_tuple().exponent)

def format_currency(value, curr='$', sep='.', dp=',',
                    pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    curr: optional currency symbol before the sign (may be blank)
    sep: optional grouping separator (comma, period, space, or blank)
    dp: decimal point indicator (comma or period)
    only specify as blank when places is zero
    pos: optional sign for positive numbers: '+', space or blank
    neg: optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator: '-', ')', space or blank

    """

    places = count_decimals(value)

    if not places:
        dp = ''

    q = Decimal(10) ** -places  # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)

    return unicode(''.join(reversed(result)))

class Product(models.Model):
    name = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)
    part_number = models.CharField(blank=True, null=True, max_length=20)
    date_added = models.DateTimeField(auto_now_add = True)
    ptype = models.ForeignKey(ProductType, blank = True, null = True)
    
    shp = models.ForeignKey('StoreHasProduct', null = True, blank = True, related_name = 'chosen_by')
    sponsored_shp = models.ForeignKey('StoreHasProduct', null = True, blank = True, related_name = 'sponsored_product')
    week_visitor_count = models.IntegerField(default = 0)
    week_discount = models.IntegerField(default = 0)
    week_external_visits = models.IntegerField(default = 0)
    long_description = models.TextField(default = ' ')
    display_name = models.CharField(max_length = 255, default = '')
    review_url = models.CharField(max_length = 255, blank=True, null=True)

    similar_products = models.CommaSeparatedIntegerField(max_length = 30, default = '0')
    created_by = models.ForeignKey(User, blank=True, null=True)
    
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (100, 100), },
        extra_thumbnails = {
            'large': {'size': (300, 300)},
            'medium': {'size': (200, 200)},
            'gallery_thumb': {'size': (90, 90)},
        },                                          
        upload_to = 'notebook_pics',
        generate_on_save = True,)
        
    def extra_data(self, request):
        return {}
        
    def pretty_display(self):
        return unicode(self)
        
    def determine_url(self):
        if hasattr(self, 'is_sponsored'):
            return reverse('solonotebooks.cotizador.views.sponsored_product_redirect', args = [self.sponsored_shp.id])
        else:
            args = ''
            if hasattr(self, 'url_args'):
                vals = ['%s=%s' % (k, v) for k, v in self.url_args.items()]
                args = '?' + '&'.join(vals)
                
            return reverse('solonotebooks.cotizador.views.product_details', args = [self.url]) + args
        
    def base_raw_text(self):
        result = self.name
        for field in self._meta.fields:
            if field.__class__.__name__ == 'ForeignKey':
                name = field.get_attname().replace('_id', '')
                if name in ['shp', 'sponsored_shp', 'created_by']:
                    continue
                try:
                    result += ' ' + getattr(self, name).raw_text()
                except AttributeError:
                    pass
            elif field.__class__.__name__ == 'CharField':
                part_result = getattr(self, field.get_attname())
                if part_result:
                    result += ' ' + part_result
            
        for m2mfield in self._meta.get_m2m_with_model():
            m2mfieldname = m2mfield[0].name
            many_related_manager = getattr(self, m2mfieldname)
            for entry in many_related_manager.all():
                result += ' ' + unicode(entry.raw_text())
                
        return result
                
    def dprint(self):
        message = str(self.id) + ' ' + unicode(self) + '\n'
        if self.shp:
            message += 'Disponible'
        else:
            message += 'No disponible'
        return message + '\n'
        
    def disqus_id(self):
        return str(self.id)
        
    @classmethod
    def custom_update(cls):
        pass

    @classmethod
    def get_valid(cls):
        return cls.objects.filter(shp__isnull = False)
        
    @staticmethod
    def get_all_ordered():
        from solonotebooks.cotizador.models import *
        pts = ProductType.get_valid()
        result = []
        for pt in pts:
            c = eval(pt.classname)
            result.extend(c.objects.all())
        return result
        
    @classmethod
    def get_available(self):
        return self.objects.filter(shp__isnull = False)
        
    def clean(self):
        self.ptype = ProductType.objects.get(classname = self.__class__.__name__)
        if not self.similar_products:
            self.similar_products == '0'
    
    def save(self):
        super(Product, self).save()
        if self.similar_products == '0':
            self.load_similar_products()
        self.update_display_name()
        super(Product, self).save()

    def update_display_name(self):
        from solonotebooks.cotizador.utils import urlify
        pself = self.get_polymorphic_instance()
        self.display_name = pself.get_display_name()
        self.url = str(self.id) + '-' + urlify(self.display_name)
        
    def update_part_number(self):
        from . import StoreHasProductEntity
        if not self.part_number:
            shpes = StoreHasProductEntity.objects.filter(shp__product=self, part_number__isnull=False)
            if shpes:
                self.part_number = shpes[0].part_number
            
    def latest_price(self):
        if hasattr(self, 'is_sponsored'):
            return self.sponsored_shp.shpe.latest_price
        elif self.shp and self.shp.shpe:
            return self.shp.shpe.latest_price
        else:
            return 0
            
    def update(self, send_mails=True, product_visits=None):
        from . import LogReviveProduct, LogChangeProductPrice, LogLostProduct, ProductPriceChange, LogReviveProduct
        print self

        print '1'
        shps = self.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price')
        print '2'
        
        if shps:
            shp = shps[0]
            print 'El producto tiene registros de disponibilidad'
            
            log_price_change = True
            if not self.shp:
                LogReviveProduct.new(self).send_notification_mails(send_mails)
                log_price_change = False
            
            if self.shp and self.shp.shpe and shp.shpe.latest_price != self.shp.shpe.latest_price:
                if log_price_change:
                    LogChangeProductPrice.new(self, self.shp.shpe.latest_price, shp.shpe.latest_price).send_notification_mails(send_mails)
                ppc = ProductPriceChange()
                ppc.product = self
                ppc.price = shp.shpe.latest_price
                ppc.date = date.today()
                ppc.save()

            self.shp = shp
        else:
            print 'El producto no tiene registros de disponibilidad'

            if self.shp:
                 LogLostProduct.new(self).send_notification_mails(send_mails)

            self.shp = None

        print '3'
        ppcs = self.productpricechange_set.all()
        print '4'
        if len(ppcs) == 0:
            ppc = ProductPriceChange()
            ppc.product = self
            if self.shp and self.shp.shpe:
                ppc.price = self.shp.shpe.latest_price
            else:
                ppc.price = 0
            ppc.date = date.today()
            ppc.save()
        
        if self.sponsored_shp and not self.sponsored_shp.shpe:
            self.sponsored_shp = None

        print '5'
        self.long_description = self.raw_text()
        print '6'
        self.update_week_discount()
        print '7'
        if not product_visits:
            self.update_week_visits()
        else:
            try:
                self.week_visitor_count = product_visits[self.id]
            except KeyError:
                print 'Error: ' + str(self.id);
                self.week_visitor_count = 0
        print '8'
        self.update_week_external_visits()
        print '9'
        self.update_display_name()
        print '10'
        self.update_part_number()
        print '11'
        
        self.save()
        print '12'
        self.generate_chart()
        print '13'

        print '14'
        pol_prod = self.get_polymorphic_instance()
        print '15'
        pol_prod.custom_local_update()
        print '16'
        pol_prod.save()
        print '17'
        
    def custom_local_update(self):
        pass
        
    
    def get_polymorphic_instance(self):
        from solonotebooks.cotizador.models import *
        c = eval(self.ptype.classname)
        return c.objects.get(pk = self.id) 
        
    def __unicode__(self):
        return self.display_name
        
    def raw_text(self):
        entity = self.get_polymorphic_instance()
        return entity.raw_text()
        
    def pretty_min_price(self):
        if self.shp:
            return prettyPrice(self.latest_price())
        else:
            return 'No disponible'
        
    def price_at(self, date):
        from . import StoreProductHistory
        
        sphs = StoreProductHistory.objects.filter(registry__shp__product = self, date = date).order_by('price')
        
        if sphs:
            return sphs[0].price
        else:
            return 0
    
    def update_week_discount(self):
        t = date.today()
        d = timedelta(days = 3)
        old_price = self.price_at(t - d)
        try:
            self.week_discount = int(100 * (old_price - self.shp.shpe.latest_price) / old_price)
        except Exception:
            self.week_discount = 0
            
    def update_week_external_visits(self):
        from . import ExternalVisit
        t = date.today()
        d = timedelta(days = 3)
        counter = ExternalVisit.objects.filter(shn__shp__product = self, date__gte=t - d, date__lte=t).count()
        self.week_external_visits = counter
            
    def update_week_visits(self):
        t = date.today()
        d = timedelta(days = 1)
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
        
    def render_div(self):
        entity = self
        if entity.__class__.__name__ == 'Product':
            entity = entity.get_polymorphic_instance()
        
        template_file = 'templatetags/div_' + self.ptype.adminurlname + '.html'
        return render_to_string(template_file, { 'product': entity })
        
    def render_similar(self):
        entity = self
        if entity.__class__.__name__ == 'Product':
            entity = entity.get_polymorphic_instance()
        
        template_file = 'templatetags/similar_' + self.ptype.adminurlname + '.html'
        return render_to_string(template_file, { self.ptype.adminurlname: entity })
        
    def render_details(self):
        entity = self
        if entity.__class__.__name__ == 'Product':
            entity = entity.get_polymorphic_instance()
        
        template_file = 'templatetags/sub_details_' + self.ptype.adminurlname + '.html'
        
        return render_to_string(template_file, { self.ptype.adminurlname: entity })
        
    def load_similar_products(self):
        entity = self
        if entity.__class__.__name__ == 'Product':
            entity = entity.get_polymorphic_instance()
        entity.load_similar_products()
        
    def clone_product(self, staff):
        clone_prod = deepcopy(self)
        clone_prod.id = None
        clone_prod.product_ptr.id = None
        clone_prod.product_ptr_id = None
        clone_prod.date_added = datetime.now()
        clone_prod.shp = None
        clone_prod.name += ' (clone)'
        clone_prod.week_visitor_count = 0
        clone_prod.week_discount = 0
        clone_prod.week_visitor_count = 0
        clone_prod.week_external_visits = 0
        clone_prod.part_number = ''
        clone_prod.created_by = staff
        
        clone_prod.save()
        
        for m2mfield in self._meta.get_m2m_with_model():
            m2mfieldname = m2mfield[0].name
            orig_many_related_manager = getattr(self, m2mfieldname)
            clone_many_related_manager = getattr(clone_prod, m2mfieldname)
            for entry in orig_many_related_manager.all():
                clone_many_related_manager.add(entry)

        clone_prod.save()
        return clone_prod

    def determine_site(self):
        if self.ptype.id == 4:
            o = self.get_polymorphic_instance()
            if o.stype.name == 'Monitores':
                return settings.MONITOR_SITE
            else:
                return settings.TELEVISION_SITE

        return settings.D[self.ptype.id]

    def formatted_price(self):
        return format_currency(Decimal(self.price))
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Product'
        ordering = ['display_name']       
        

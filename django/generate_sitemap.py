#-*- coding: UTF-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from xml.dom import minidom
from django.forms import ChoiceField
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.forms import *
from solonotebooks.cotizador.fields import *
from solonotebooks import settings

# Script that generates the sitemap of the catalog, including notebooks,
# processor lines and video card lines
def main():
    siteUrl = settings.SERVER_NAME

    xml = minidom.Document()
    
    rootElem = xml.createElement('urlset');
    rootElem.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    specificSites = [siteUrl + '/', siteUrl + '/blog/']
    
    for specificSite in specificSites:
        siteElem = xml.createElement('url')
        
        locText = xml.createTextNode(specificSite)
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        siteElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        siteElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        siteElem.appendChild(priorityElem)        
        
        rootElem.appendChild(siteElem)
        
    product_types = ProductType.objects.all()
    for product_type in product_types:
        prodElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/' + product_type.urlname + '/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        prodElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        prodElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        prodElem.appendChild(priorityElem)        
        
        rootElem.appendChild(prodElem)
        
        prodElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/' + product_type.urlname + '/catalog/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        prodElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        prodElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        prodElem.appendChild(priorityElem)        
        
        rootElem.appendChild(prodElem)
    
    prods = Product.objects.order_by('id')
    for prod in prods:
        prodElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/products/' + str(prod.url) + '/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        prodElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        prodElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        prodElem.appendChild(priorityElem)        
        
        rootElem.appendChild(prodElem)
        
    ptypes = ProductType.objects.all()
    for ptype in ptypes:
        sf = eval(ptype.classname + 'SearchForm({}, False)')
        for field in sf.fields:
            field_value = sf.fields[field]
            if field_value.__class__.__name__ == 'ClassChoiceField':
                queryset = field_value.queryset
                ids = [elem.id for elem in queryset]
            elif field_value.__class__.__name__ == 'CustomChoiceField':
                queryset = field_value.choices
                ids = [elem[0] for elem in queryset]
            else:
                continue
            for i in ids:
                procElem = xml.createElement('url')
            
                locText = xml.createTextNode(siteUrl + '/' + ptype.urlname + '/catalog/?advanced_controls=1&' + field + '=' + str(i))
                locElem = xml.createElement('loc')
                locElem.appendChild(locText)
                procElem.appendChild(locElem)
                
                changeFreqText = xml.createTextNode('daily')
                changeFreqElem = xml.createElement('changefreq')
                changeFreqElem.appendChild(changeFreqText)
                procElem.appendChild(changeFreqElem)
                
                priorityText = xml.createTextNode('1.00')
                priorityElem = xml.createElement('priority')
                priorityElem.appendChild(priorityText)
                procElem.appendChild(priorityElem)        
                
                rootElem.appendChild(procElem)
        
    video_card_lines = NotebookVideoCardLine.objects.order_by('id')
    for video_card_line in video_card_lines:
        vclElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/notebooks/video_card_lines/' + str(video_card_line.id) + '/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        vclElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        vclElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        vclElem.appendChild(priorityElem)        
        
        rootElem.appendChild(vclElem)
        
    processor_line_families = NotebookProcessorLineFamily.objects.order_by('id')
    for processor_line_family in processor_line_families:
        procElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/notebooks/processor_lines/' + str(processor_line_family.id) + '/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        procElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        procElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        procElem.appendChild(priorityElem)        
        
        rootElem.appendChild(procElem)
        
    gpus = VideoCardGpu.objects.all()
    for gpu in gpus:
        procElem = xml.createElement('url')
        
        locText = xml.createTextNode(siteUrl + '/video_cards/gpu_details/' + str(gpu.id) + '/')
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        procElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        procElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        procElem.appendChild(priorityElem)        
        
        rootElem.appendChild(procElem)
        
    xml.appendChild(rootElem)
    
    print xml.toprettyxml(indent='\t', encoding='UTF-8')
                
if __name__ == '__main__':
    main()
    

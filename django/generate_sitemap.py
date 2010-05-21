import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from xml.dom import minidom
from solonotebooks.cotizador.models import *

def main():
    xml = minidom.Document()
    
    rootElem = xml.createElement('urlset');
    rootElem.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    specificSites = ['http://www.solonotebooks.net/', 'http://www.solonotebooks.net/blog']
    
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
    
    ntbks = Notebook.objects.all().order_by('id')
    for ntbk in ntbks:
        ntbkElem = xml.createElement('url')
        
        locText = xml.createTextNode('http://www.solonotebooks.net/notebooks/' + str(ntbk.id))
        locElem = xml.createElement('loc')
        locElem.appendChild(locText)
        ntbkElem.appendChild(locElem)
        
        changeFreqText = xml.createTextNode('daily')
        changeFreqElem = xml.createElement('changefreq')
        changeFreqElem.appendChild(changeFreqText)
        ntbkElem.appendChild(changeFreqElem)
        
        priorityText = xml.createTextNode('1.00')
        priorityElem = xml.createElement('priority')
        priorityElem.appendChild(priorityText)
        ntbkElem.appendChild(priorityElem)        
        
        rootElem.appendChild(ntbkElem)
    
    xml.appendChild(rootElem)
    
    print xml.toprettyxml(indent='\t', encoding='UTF-8')
                
if __name__ == '__main__':
    main()
    

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from xml.dom import minidom
from solonotebooks.cotizador.models import *

# Script that generates the sitemap of the catalog, including notebooks,
# processor lines and video card lines
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
    
    ntbks = Notebook.objects.order_by('id')
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
        
    video_card_lines = VideoCardLine.objects.order_by('id')
    for video_card_line in video_card_lines:
        vclElem = xml.createElement('url')
        
        locText = xml.createTextNode('http://www.solonotebooks.net/video_card_line/' + str(video_card_line.id))
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
        
    processor_line_families = ProcessorLineFamily.objects.order_by('id')
    for processor_line_family in processor_line_families:
        procElem = xml.createElement('url')
        
        locText = xml.createTextNode('http://www.solonotebooks.net/processor_line_families/' + str(processor_line_family.id))
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
    

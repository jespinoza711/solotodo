#-*- coding: UTF-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from xml.dom import minidom
from django.forms import ChoiceField
from solonotebooks.cotizador.models import *
from solonotebooks.cotizador.forms import *
from solonotebooks.cotizador.fields import *
from solonotebooks import settings
from xml.sax.saxutils import unescape

# Script that generates the sitemap of the catalog, including notebooks,
# processor lines and video card lines
def main():
    siteUrl = 'http://www.solotodo.net'

    xml = minidom.Document()
    
    rootElem = xml.createElement('rss');
    rootElem.setAttribute('version', '2.0')
    rootElem.setAttribute('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rootElem.setAttribute('xmlns:dsq', 'http://www.disqus.com/')
    rootElem.setAttribute('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rootElem.setAttribute('xmlns:wp', 'http://wordpress.org/export/1.0/')
    
    subRootElem = xml.createElement('channel');
    
    for product in Product.objects.all():
        productElem = xml.createElement('item')
        
        titleText = xml.createTextNode(unicode(product))
        titleElem = xml.createElement('title')
        titleElem.appendChild(titleText)
        productElem.appendChild(titleElem)
        
        linkText = xml.createTextNode(siteUrl + '/products/' + str(product.id))
        linkElem = xml.createElement('link')
        linkElem.appendChild(linkText)        
        productElem.appendChild(linkElem)
        
        text = xml.createTextNode('')
        elem = xml.createElement('content:encoded')
        elem.appendChild(text)        
        productElem.appendChild(elem)
        
        text = xml.createTextNode(str(product.id))
        elem = xml.createElement('dsq:thread_identifier')
        elem.appendChild(text)        
        productElem.appendChild(elem)
        
        text = xml.createTextNode(str(product.date_added) + ' 00:00:00')
        elem = xml.createElement('wp:post_date_gmt')
        elem.appendChild(text)        
        productElem.appendChild(elem)
        
        text = xml.createTextNode('open')
        elem = xml.createElement('wp:comment_status')
        elem.appendChild(text)        
        productElem.appendChild(elem)
        
        for comment in product.productcomment_set.filter(validated = True):
            comment_elem = xml.createElement('wp:comment')
            
            text = xml.createTextNode(str(comment.id))
            elem = xml.createElement('wp:comment_id')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            if comment.user:
                user = comment.user.username
            elif comment.nickname:
                user = comment.nickname
            else:
                user = 'Anonimo'
                
            text = xml.createTextNode(user)
            elem = xml.createElement('wp:comment_author')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            if comment.user:
                text = xml.createTextNode(comment.user.email)
            else:
                text = xml.createTextNode(user + '@example.com')
            elem = xml.createElement('wp:comment_author_email')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode('http://www.solotodo.net/')
            elem = xml.createElement('wp:comment_author_url')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode('93.48.67.119')
            elem = xml.createElement('wp:comment_author_IP')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode(str(comment.date) + ' 00:00:00')
            elem = xml.createElement('wp:comment_date_gmt')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode('<![CDATA[' + comment.comments + ']]>')
            elem = xml.createElement('wp:comment_content')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode('1')
            elem = xml.createElement('wp:comment_approved')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            text = xml.createTextNode('0')
            elem = xml.createElement('wp:comment_parent')
            elem.appendChild(text)        
            comment_elem.appendChild(elem)
            
            productElem.appendChild(comment_elem)
        
        subRootElem.appendChild(productElem)
    
    rootElem.appendChild(subRootElem)    
    xml.appendChild(rootElem)
    
    print unescape(xml.toprettyxml(indent='\t', encoding='UTF-8'))
                
if __name__ == '__main__':
    main()
    

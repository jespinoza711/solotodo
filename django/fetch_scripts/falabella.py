#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from fetch_scripts import ProductData

class Falabella:
    name = 'Falabella'

    # Main method
    def getNotebooks(self):
        print 'Getting Falabella notebooks'
        # Basic data of the target webpage and the specific catalog
        
        # Browser initialization
        browser = mechanize.Browser()
        
        # Array containing the data for each product
        productsData = []
        
        urls = [    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=0&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=1&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=2&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                    'http://www.falabella.com/webapp/commerce/command/ExecMacro/falabella/macros/list_prod.d2w/report?cgmenbr=1891&cgrfnbr=2458576&cgpadre=2458457&cghijo=&cgnieto=2458576&division=3&orden=&ConFoto=1&pcomp1=&pcomp2=&pcomp3=&pcomp4=&pcomp5=&pcomp6=&pcomp7=&pcomp8=&pcomp9=&pcomp10=&cghijo1=2460493&nivel=1',
                    ]
                            
        for url in urls:

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(url).get_data()
            baseSoup = BeautifulSoup(baseData)

            # Obtain the links to the other pages of the catalog (2, 3, ...)
            mosaicDivs = baseSoup.findAll("div", { "id" : "mosaico" })
            
            for mosaicDiv in mosaicDivs:    
                productData = ProductData()
                    
                divPrecioNormal = mosaicDiv.find("div", { "id" : "precioNormal" })
                contents = divPrecioNormal.string.replace('&nbsp;', '').replace('Oferta:', '').replace('Normal:', '').replace('&#36;', '').replace('.', '').strip()
                
                if len(contents) > 0:
                    contents = contents.replace('&nbsp;', '').replace('Oferta:', '').replace('Normal:', '').replace('&#36;', '').replace('.', '').strip()
                    precio = int(contents)
                else:
                    divPrecio = mosaicDiv.find("div", { "id" : "precioPrincipal" })
                    contentsi = divPrecio.string
                    contentsi = contentsi.replace('&nbsp;', '').replace('Oferta:', '').replace('Normal:', '').replace('&#36;', '').replace('.', '').strip()
                    precio = int(contentsi)
                    
                productData.price = precio
                
                divDesc = mosaicDiv.find("div", { "id" : "descripcion" })
                name_1 = divDesc.find("h1").find("a")
                name_1b = name_1.find("b")
                if (name_1b):
                    name_1 = name_1b.string
                else:
                    name_1 = name_1.string
                name_1 = name_1.encode('ascii','ignore').strip()
                name_2 = divDesc.find("h1").find("a").contents
                if (len(name_2) > 2):
                    name_2 = name_2[2].strip()
                else:
                    name_2 = ''
                name_2 = name_2.encode('ascii','ignore').strip()
                
                productData.custom_name = name_1 + ' ' + name_2

                url = 'http://www.falabella.com' + mosaicDiv.find('a')['href']
                productData.url = url
                productData.comparison_field = url
                
                print productData
                
                productsData.append(productData)

        return productsData


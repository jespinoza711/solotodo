#!/usr/bin/env python

import mechanize
import json
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore
from django.db.models import Q
from solonotebooks.cotizador.models import CellPricingTier, CellCompany, CellPricingPlan
from solonotebooks.cotizador.utils import latin1_to_ascii
import re

class Entel(FetchStore):
    name = 'Entel'
    use_existing_links = False

    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except mechanize.HTTPError:
            return None
            
        product_soup = BeautifulSoup(product_data)
        
        product_title = product_soup.find('h1').contents[0].strip().encode('ascii', 'ignore')
        product_price = 0
                
        product_data = ProductData()
        product_data.custom_name = product_title
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        url = 'http://personas.entelpcs.cl/PortalPersonas/com/entelpcs/catalogoEquipos/publico/controllers/listadoEquipos/ListadoEquiposController.jpf'
        
        # Browser initialization
        browser = mechanize.Browser()
        product_links = []              

        # Obtain and parse HTML information of the base webpage
        baseData = browser.open(url).get_data()
        json_data = json.loads(baseData)
        
        json_products = json_data['equipos']
        for json_product in json_products:
            product_id = json_product['codProducto']
            product_links.append(['http://personas.entel.cl/PortalPersonas/appmanager/entelpcs/personas?_nfpb=true&_pageLabel=P12800364521294253893661&codProducto=' + product_id, 'Cell'])
                
        return product_links
        
    def get_plans(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://personas.entel.cl/PortalPersonas/appmanager/entelpcs/personas?_nfpb=true&_pageLabel='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        extensions = [
                    ['P7200113701283291467481', True],
                    ['P15600386721300459240749', True],
                    ['P800933501267454369229', False],
                    ['P800233501267216196630', False],
                    ['P800333501267216211110', False],
                    ]
                    
        plans = []
                    
        for extension, includes_data in extensions:
            url = urlBase + extension
            data = browser.open(url).get_data()
            soup = BeautifulSoup(data)

            tables = soup.findAll('table', { 'class': 'tablaLiquida' })
                
            for table in tables:
                rows = table.findAll('tr')[1:]
                for row in rows:
                    cells = row.findAll('td')
                    name_container = cells[0].find('p')
                    if not name_container:
                        name_container = cells[0].contents[0]
                    if not name_container.string:
                        continue
                    name = latin1_to_ascii(name_container.string.strip())
                    
                    price_container = cells[1].find('p')
                    if not price_container:
                        price_container = cells[1].contents[0]
                    price = price_container.string.strip()
                    price = int(price.replace('$', '').replace('.', ''))
                    plan = [name, price, includes_data]
                    plans.append(plan)
                    
        return plans
        
    def calculate_tiers(self, shpe, cell_plans, pricing):
        print shpe.dprint()
        
        browser = mechanize.Browser()
        data = browser.open(shpe.url).get_data()
        soup = BeautifulSoup(data)
        
        blackberry_plans = cell_plans.filter(includes_data = True).filter(Q(name__icontains = 'blackberry') | Q(name__icontains = 'bb'))
        data_plans = cell_plans.filter(includes_data = True)
        voice_plans = cell_plans.filter(includes_data = False)
        
        # Multimedia check
        multimedia_link = soup.find('a', { 'class': 'btnAzul centrarBtn lbPlanesMulti' })
        if multimedia_link:
            
            p = re.compile('codMaterial = "\d+"')
            for match in p.finditer(data):
                first_index = match.span()[0]
                last_index = match.span()[1]
                cod_material = data[first_index + 15:last_index - 1]
                break
            
            link = 'http://personas.entel.cl/PortalPersonas/com/entelpcs/catalogoEquipos/publico/controllers/detalleEquipo/planesMultimedia.do?marcaModelo=&query1=idContenido%3D%27pltelssmulti%27%20%26%26%20(cm_nodeName%20like%20%273*oculta*%27)&query2=idContenido%20%3D%20%27pltelssmulti%27%20%26%26%20(%20cm_nodeName%20like%20%2702*%27%20%7C%7C%20cm_nodeName%20like%20%2703*%27%20%7C%7C%20cm_nodeName%20like%20%2705*%27%20%7C%7C%20cm_nodeName%20like%20%2706*%27)&query3=idContenido%20%3D%20%27pltelssmulti%27%20%26%26%20(%20cm_nodeName%20like%20%2707%20*%27%20%7C%7C%20cm_nodeName%20like%20%2709*%27%20%7C%7C%20cm_nodeName%20like%20%2710%20*%27%20)&codMaterial=' + cod_material

            data = browser.open(link).get_data()
            sub_soup = BeautifulSoup(data)
            
            table = sub_soup.find('table', {'class': 'tablaLiquida tablaPlanesMultimedia-equipo'})
            if table:
                rows = table.findAll('tr')
                
                plan_titles = []
                sum_cols = 0
                for price_header in rows[0].findAll('th')[1:]:
                    title = price_header.find('p').string
                    title = title.replace('Planes ', '').replace(' Todo Destino', '')
                    colspan = int(price_header['colspan'])
                    sum_cols += colspan
                    price_title_data = [title, sum_cols]
                    plan_titles.append(price_title_data)
                    
                plan_names = []
                for idx, price_header in enumerate(rows[1].findAll('th')):
                    name = price_header.find('p').string.strip()
                    for title, cols in plan_titles:
                        if cols >= (idx + 1):
                            plan_name = title + ' ' + name
                            plan_names.append(plan_name)
                            break
                    
                plan_tiers = []
                for idx, price_cell in enumerate(rows[2].findAll('td')[1:]):
                    price = int(price_cell.find('p').string.replace('$', '').replace('.', ''))
                    plan_data = [plan_names[idx], price]
                    plan_tiers.append(plan_data)
                    
                
                for plan_name, cellphone_price in plan_tiers:
                    plan = data_plans.get(name = plan_name)
                    tier = CellPricingTier()
                    tier.pricing = pricing
                    tier.plan = plan
                    tier.shpe = shpe
                    tier.cellphone_price = cellphone_price
                    tier.update_prices()
                    tier.save()
                    print tier.pretty_print()
                    
        # Blackberry check
        if 'blackberry' in shpe.custom_name.lower():
            headers = soup.findAll('h3')
            bb_headers = []
            for header in headers:
                text = header.string
                if text and 'Arriendo' in text:
                    bb_headers.append(header)
                    
            bb_headers.reverse()
                    
            for bb_header in bb_headers:
                price_spans = bb_header.parent.findAll('span', {'class': 'valorPrecio'})
                if price_spans and 'No disponible' not in price_spans[0].string:
                    cellphone_price = int(price_spans[0].string.replace('$', '').replace(',', ''))
                    monthly_quota = int(price_spans[1].string.replace('$', '').replace(',', ''))
                    
                    for plan in blackberry_plans:
                        tier = CellPricingTier()
                        tier.pricing = pricing
                        tier.plan = plan
                        tier.shpe = shpe
                        tier.cellphone_price = cellphone_price
                        tier.monthly_quota = monthly_quota
                        tier.update_prices()
                        tier.save()
                        print tier.pretty_print()
                        
                    break
                
        # Voice check
        headers = soup.findAll('h3')
        voice_headers = []
        for header in headers:
            text = header.string
            if text and 'Arriendo' in text:
                voice_headers.append(header)
                
        voice_headers.reverse()
                
        for voice_header in voice_headers:
            price_spans = voice_header.parent.findAll('span', {'class': 'valorPrecio'})
            if price_spans and 'No disponible' not in price_spans[0].string:
                cellphone_price = int(price_spans[0].string.replace('$', '').replace(',', ''))
                monthly_quota = int(price_spans[1].string.replace('$', '').replace(',', ''))
                
                for plan in voice_plans:
                    tier = CellPricingTier()
                    tier.pricing = pricing
                    tier.plan = plan
                    tier.shpe = shpe
                    tier.cellphone_price = cellphone_price
                    tier.monthly_quota = monthly_quota
                    tier.update_prices()
                    tier.save()
                    print tier.pretty_print()
                    
                break
            
        # Prepago check
        prepago_header = None
        for header in headers:
            text = header.string
            if text and 'Prepago' in text:
                prepago_header = header
                
        if prepago_header:
            price_span = prepago_header.parent.find('span', {'class': 'valorPrecio'})
            if price_span:
                cellphone_price = int(price_span.string.replace('$', '').replace(',', ''))
                
                company = CellCompany.objects.get(store__classname = self.__class__.__name__)
                
                try:
                    plan = CellPricingPlan.objects.get(name = 'Prepago', company = company)
                except CellPricingPlan.DoesNotExist:
                    plan = CellPricingPlan()
                    plan.price = 0
                    plan.name = 'Prepago'
                    plan.ordering = 1
                    plan.includes_data = False
                    plan.company = company
                    plan.save()
                
                tier = CellPricingTier()
                tier.pricing = pricing
                tier.plan = plan
                tier.shpe = shpe
                tier.cellphone_price = cellphone_price
                tier.update_prices()
                tier.save()
                print tier.pretty_print()

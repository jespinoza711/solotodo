#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore
from django.db.models import Q
from solonotebooks.cotizador.models import CellPricingTier, CellCompany, CellPricingPlan
import pdb
import re

class Movistar(FetchStore):
    name = 'Movistar'
    use_existing_links = False

    def retrieve_product_data(self, product_link):
        browser = mechanize.Browser()
        try:
            product_data = browser.open(product_link).get_data()
        except mechanize.HTTPError:
            return None
        product_soup = BeautifulSoup(product_data)
        
        product_title = product_soup.find('h2').string
        product_price = 0
                
        product_data = ProductData()
        product_data.custom_name = product_title
        product_data.price = product_price
        product_data.url = product_link
        product_data.comparison_field = product_link
        
        return product_data

    def retrieve_product_links(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://hogar.movistar.cl'
        urlBuscarProductos = '/equipos/index.php/catalogo/pagina/'
        
        # Browser initialization
        browser = mechanize.Browser()

        product_links = []
        page_number = 1                    
        while True:
            urlWebpage = urlBase + urlBuscarProductos + str(page_number)

            # Obtain and parse HTML information of the base webpage
            baseData = browser.open(urlWebpage).get_data()
            baseSoup = BeautifulSoup(baseData)

            prod_list = baseSoup.findAll('div', {'class': 'producto'})
            
            if not prod_list:
                break
        
            for prod in prod_list:
                link = prod.find('a')['href']
                product_links.append([link, 'Cell'])
                    
            page_number += 1
                
        return product_links
        
    def get_plans(self):
        # Basic data of the target webpage and the specific catalog
        urlBase = 'http://www.movistar.cl/PortalMovistarWeb/appmanager/PortalMovistar/portal?_nfpb=true&_pageLabel='
        
        # Browser initialization
        browser = mechanize.Browser()
        
        extensions = [
                    # Multimedia Libre
                    ['P13000377301307396916365', True, -1],
                    # Planes Libre
                    ['P9600488711290017299371', False, -1],
                    # Planes Club
                    ['P9600588711290017393713', False, -1],
                    # Planes Control Destino
                    ['P9600688711290017495969', False, -1],
                    # Planes Control Tarifa Plana
                    ['P9600788711290017587840', False, -1],
                    # Planes BlackBerry Libres
                    ['P9601088711290017897034', True, 0],
                    ]
                    
        plans = []
                    
        for extension, includes_data, last_index in extensions:
            url = urlBase + extension
            data = browser.open(url).get_data()
            soup = BeautifulSoup(data)    

            tables = soup.findAll('table', { 'class': 'TablaPlanesIndividiales' })
            if last_index != 0:
                tables = tables[:last_index]
                
            for table in tables:
                rows = table.findAll('tr')
                for row in rows:
                    cells = row.findAll('td')
                    name = ' '.join(str(c).strip() for c in cells[0].find('div').contents if str(c) != '<br />')
                    name = name.replace('<br />', '')
                    name = name.replace('Smartphone ', '')
                    price = cells[2].find('div', { 'class': 'PrecioPlan' }).string
                    price = int(price.replace('$', '').replace('.', '').replace('(**)', ''))
                    plan = [name, price, includes_data]
                    plans.append(plan)
                    
        # LANPASS plans
        lanpass_url = urlBase + 'P1201419831272321333859'
        data = browser.open(lanpass_url).get_data()
        soup = BeautifulSoup(data)    

        tables = soup.findAll('table', { 'class': 'TablaPlanesLANPASS' })
        for table in tables:
            rows = table.findAll('tr')
            for row in rows:
                cells = row.findAll('td')
                name = cells[1].find('div').string
                name = name.replace('Smartphones', 'Multimedia')
                name = ' '.join([s for s in name.split(' ') if s])
                name = name.replace('Multimedia BB', 'Blackberry')
                price = cells[1].find('div', { 'class': 'PrecioPlan' }).string
                price = int(price.replace('$', '').replace('.', '').replace('(**)', ''))
                plan = [name, price, True]
                plans.append(plan)
                
        # Súper Smartphone plans
        super_smartphone_url = urlBase + 'P14400695741312847094968'
        data = browser.open(super_smartphone_url).get_data()
        soup = BeautifulSoup(data)    

        
        table = soup.find('div', { 'class': 'contenedorPlanesConecta' }).find('table')
        rows = table.findAll('tr')[1:]
        for row in rows:
            cells = row.findAll('td')
            name = cells[0].find('div', 'equipos').string
            name = name.replace('/', ' - ')
            price = cells[4].find('span', { 'class': 'renta' }).string
            price = int(price.replace('$', '').replace('.', '').replace('(**)', ''))
            plan = [name, price, True]
            plans.append(plan)
                    
        return plans
        
    def calculate_tiers(self, shpe, cell_plans, pricing):
        print shpe.id
        print pricing.id
        print shpe.dprint()
        
        browser = mechanize.Browser()
        try:
            data = browser.open(shpe.url).get_data()
        except Exception, e:
            return
        soup = BeautifulSoup(data)
        
        contrato_tab = soup.find('a', { 'id': 'contrato_test' })
        if contrato_tab:
            plan_divs = soup.findAll('div', 'seleccionPlan')
            plan_count = len(plan_divs) / 2
            plan_divs = plan_divs[:plan_count]
            
            for plan_div in plan_divs:
                phone_price = plan_div.find('span', 'precioCabecera').string
                phone_price = int(phone_price.replace('$', '').replace('.', ''))
                
                plan_labels = plan_div.findAll('label')
                for plan_label in plan_labels:
                    plan_name = plan_label.string
                    
                    m = re.search(r'(\d+)G', plan_name)
                    if m:
                        plan_name = plan_name.replace(m.group(), m.group() + 'B')
                        
                    m = re.match(r'Libre', plan_name)
                    if m:
                        plan_name = 'Plan ' + plan_name
                        
                    plan_name = plan_name.replace(' + Num Ilimitado', '')
                    plan_name = plan_name.replace(u' + Servicio Reparación', '')
                        
                    try:
                        plan = cell_plans.get(name=plan_name)
                        
                        tier = CellPricingTier()
                        tier.pricing = pricing
                        tier.plan = plan
                        tier.shpe = shpe
                        tier.cellphone_price = phone_price
                        tier.monthly_quota = plan.price
                        tier.update_prices()
                        tier.save()
                        print tier.pretty_print()
                    except:
                        print 'Plan no encontrado %s' % plan_name

        prepago_tab = soup.find('a', { 'id': 'prepago_test' })
        
        if prepago_tab:
            prepago_container = soup.find('div', { 'id': 'prepago' })
            
            try:
                prepaid_price = int(prepago_container.find('p', {'class': 'precio'}).string.replace('$', '').replace('.', ''))
            except:
                prepaid_price = int(prepago_container.find('strong').string.replace('$', '').replace('.', ''))
            
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
            tier.cellphone_price = prepaid_price
            tier.monthly_quota = plan.price
            tier.update_prices()
            tier.save()
            print tier.pretty_print()

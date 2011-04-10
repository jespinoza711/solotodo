#!/usr/bin/env python

import mechanize
from BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
from . import ProductData, FetchStore
from django.db.models import Q
from solonotebooks.cotizador.models import CellPricingTier, CellCompany, CellPricingPlan

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
                    ['P9601988711290175314777', True, -1],
                    ['P9600488711290017299371', False, -1],
                    ['P9600588711290017393713', False, -1],
                    ['P9600688711290017495969', False, -1],
                    ['P9600788711290017587840', False, -1],
                    ['P9600988711290017787150', False, 0],
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
                    price = cells[2].find('div', { 'class': 'PrecioPlan' }).string
                    price = int(price.replace('$', '').replace('.', '').replace('(**)', ''))
                    plan = [name, price, includes_data]
                    plans.append(plan)
                    
        return plans
        
    def calculate_tiers(self, shpe, cell_plans, pricing):
        print shpe.dprint()
        
        browser = mechanize.Browser()
        data = browser.open(shpe.url).get_data()
        soup = BeautifulSoup(data)
        
        multimedia_plans = list(cell_plans.filter(includes_data = True).filter(~Q(name__icontains = 'blackberry')))
        voice_plans = list(cell_plans.filter(includes_data = False).all())
        blackberry_plans = list(cell_plans.filter(includes_data = True, name__icontains = 'blackberry').all())
        
        contrato_tab = soup.find('a', { 'id': 'contrato_test' })
        if contrato_tab:
            contrato_container = soup.find('div', { 'id': 'contrato' })
            plan_divs = contrato_container.findAll('div', { 'class': 'equipoPlan clearfix' })
            for plan_div in plan_divs:
                text = plan_div.find('h3').string.lower()
                if 'blackberry' in text:
                    plans = blackberry_plans
                elif 'multimedia' in text:
                    plans = multimedia_plans
                elif 'voz' in text:
                    plans = voice_plans
                else:
                    continue
                    
                cellphone_price = int(plan_div.find('li', { 'class': 'valor' }).string.replace('$', '').replace('.', ''))
                try:
                    min_plan_price = int(text.split('$')[1].replace('.', ''))
                except:
                    min_plan_price = 0
                   
                i = 0
                while i < len(plans):
                    plan = plans[i]
                    if plan.price >= min_plan_price:
                        tier = CellPricingTier()
                        tier.pricing = pricing
                        tier.plan = plan
                        tier.shpe = shpe
                        tier.cellphone_price = cellphone_price
                        tier.monthly_quota = plan.price
                        tier.update_prices()
                        tier.save()
                        print tier.pretty_print()
                        plans.remove(plan)
                    else:
                        i += 1

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

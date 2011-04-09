#-*- coding: UTF-8 -*-
from models import *
from views import append_metadata_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q

def append_cellphone_metadata_to_response(request, template, args):
    ptype = ProductType.objects.get(classname = 'Cell')
    args['ptype'] = ptype
    return append_metadata_to_response(request, template, args)
    
         
def plan_details(request, plan_id):
    plan = get_object_or_404(CellPricingPlan, pk = plan_id)
    
    if 'price_ordering' in request.GET and request.GET['price_ordering'] == 'monthly_price':
        tiers = plan.cellpricingtier_set.filter(pricing__cell__isnull = False)
        tiers = sorted(tiers, key=lambda tier: tier.plan_price())
    else:
        tiers = plan.cellpricingtier_set.filter(pricing__cell__isnull = False).order_by('cellphone_price')
    
    return append_cellphone_metadata_to_response(request, 'cotizador/cell_plan_details.html', {
            'plan': plan,
            'tiers': tiers,
        })

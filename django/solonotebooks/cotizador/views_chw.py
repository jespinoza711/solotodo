#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from solonotebooks.cotizador.models.product import Product

def inline_forum_post(request, product_id):
    product = Product.objects.get(pk=product_id).get_polymorphic_instance()

    stores_with_product_available = product.storehasproduct_set.filter(shpe__isnull = False).order_by('shpe__latest_price')[:3]

    template_file = 'chw/details_' + product.ptype.adminurlname + '.html'
    return render_to_response(
        template_file,
        {
            'product': product,
            'product_prices': stores_with_product_available,
        },
        context_instance=RequestContext(request)
    )

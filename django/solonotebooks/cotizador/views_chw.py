#-*- coding: UTF-8 -*-
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from solonotebooks.cotizador.models.product import Product

def inline_forum_post(request, product_id):
    try:
        product = Product.objects.get(pk=product_id).get_polymorphic_instance()
    except Product.DoesNotExist:
        return HttpResponsePermanentRedirect('/')

    try:
        url = product.determine_site() + '/products/' + str(product_id) + '/mini/'
    except KeyError:
        return HttpResponsePermanentRedirect('/')

    return HttpResponsePermanentRedirect(url)

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

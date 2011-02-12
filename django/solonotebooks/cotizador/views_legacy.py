#-*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from utils import concat_dictionary
from django.http import HttpResponseRedirect
         
def notebook_details(request, notebook_id):
    url = reverse('solonotebooks.cotizador.views.product_details', kwargs = {'product_id': notebook_id})
    return HttpResponseRedirect(url)
    
def processor_line_family_details(request, processor_line_family_id):
    url = reverse('solonotebooks.cotizador.views_notebooks.processor_line_details', args = [processor_line_family_id])
    url += concat_dictionary(request.GET)
    return HttpResponseRedirect(url)
    
def all_processor_line_families(request):
    url = reverse('solonotebooks.cotizador.views_notebooks.processor_line')
    return HttpResponseRedirect(url)
    
def video_card_line_details(request, video_card_line_id):
    url = reverse('solonotebooks.cotizador.views_notebooks.video_card_line_details', args = [video_card_line_id])
    url += concat_dictionary(request.GET)
    return HttpResponseRedirect(url)
    
def video_card_line(request):
    url = reverse('solonotebooks.cotizador.views_notebooks.video_card_line')
    return HttpResponseRedirect(url)

#-*- coding: UTF-8 -*-
from models import *
from views import append_metadata_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q

def append_videocard_ptype_to_response(request, template, args):
    ptype = ProductType.objects.get(classname = 'VideoCard')
    args['ptype'] = ptype
    return append_metadata_to_response(request, template, args)
    
         
def gpu_details(request, gpu_id):
    gpu = get_object_or_404(VideoCardGpu, pk = gpu_id)
    video_cards = gpu.videocard_set.filter(shp__isnull = False).order_by('?')[:4]
    
    return append_videocard_ptype_to_response(request, 'cotizador/videocard_gpu_details.html', {
            'gpu': gpu,
            'video_cards': video_cards,
        })

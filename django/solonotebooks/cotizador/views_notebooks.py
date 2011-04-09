#-*- coding: UTF-8 -*-
from models import *
from views import append_metadata_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q

def append_notebook_ptype_to_response(request, template, args):
    ptype = ProductType.objects.get(classname = 'Notebook')
    args['ptype'] = ptype
    return append_metadata_to_response(request, template, args)
    
         
def processor_line_details(request, processor_line_id):
    processor_line_family = get_object_or_404(NotebookProcessorLineFamily, pk = processor_line_id)
    other_processor_line_families = NotebookProcessorLineFamily.objects.filter(~Q(id = processor_line_family.id))
    
    processor_id = 0
    if 'processor' in request.GET:
        try:
            processor_id = int(request.GET['processor'])
        except:
            processor_id = 0
            
        try:
            processor = NotebookProcessor.objects.filter(line__family = processor_line_family).get(pk = processor_id)
            ntbks = Notebook.get_valid().filter(processor = processor).order_by('?')[0:5]
        except:
            processor = None
            ntbks = Notebook.get_valid().filter(processor__line__family = processor_line_family).order_by('?')[0:5]
    else:
        processor = None
        ntbks = Notebook.get_valid().filter(processor__line__family = processor_line_family).order_by('?')[0:5]
        
    processors = NotebookProcessor.objects.filter(line__family = processor_line_family).order_by('-speed_score')
    return append_notebook_ptype_to_response(request, 'cotizador/notebook_processor_line_details.html', {
                'processor_line_family': processor_line_family,
                'processors': processors,
                'notebooks': ntbks,
                'processor_id': processor_id,
                'processor': processor,
                'other_processor_line_families': other_processor_line_families,
            })
            
def video_card_line_details(request, video_card_line_id):
    video_card_line = get_object_or_404(NotebookVideoCardLine, pk = video_card_line_id)
    other_video_card_lines = NotebookVideoCardLine.objects.filter(~Q(id = video_card_line.id))
    video_card_id = 0
    if 'video_card' in request.GET:
        try:
            video_card_id = int(request.GET['video_card'])
        except: 
            video_card_id = 0
            
        try:
            video_card = NotebookVideoCard.objects.filter(line = video_card_line).get(pk = video_card_id)
            ntbks = Notebook.get_valid().filter(video_card = video_card).order_by('?').distinct()[0:5]
        except:
            video_card = None
            ntbks = Notebook.get_valid().filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    else:
        video_card = None    
        ntbks = Notebook.get_valid().filter(video_card__line = video_card_line).order_by('?').distinct()[0:5]
    
    video_cards = NotebookVideoCard.objects.filter(line = video_card_line).order_by('-speed_score')
    return append_notebook_ptype_to_response(request, 'cotizador/notebook_video_card_line_details.html', {
                'video_card_line': video_card_line,
                'video_cards': video_cards,
                'notebooks': ntbks,
                'video_card_id': video_card_id,
                'video_card': video_card,
                'other_video_card_lines': other_video_card_lines,
            })            
            
def processor_line(request):
    processor_line_families = NotebookProcessorLineFamily.objects.all()
    processors = NotebookProcessor.objects.order_by('-speed_score')
    return append_notebook_ptype_to_response(request, 'cotizador/notebook_all_processor_lines.html', {
        'processor_line_families': processor_line_families,
        'processors': processors
    })            
            
def video_card_line(request):
    video_card_lines = NotebookVideoCardLine.objects.all()
    video_cards = NotebookVideoCard.objects.order_by('-speed_score')
    return append_notebook_ptype_to_response(request, 'cotizador/notebook_all_video_card_lines.html', {
                'video_card_lines': video_card_lines,
                'video_cards': video_cards
    })

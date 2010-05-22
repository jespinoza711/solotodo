#-*- coding: UTF-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import sys
from datetime import date
from solonotebooks.cotizador.models import *

ntbks = Notebook.objects.all()
for ntbk in ntbks:
    npcs = NotebookPriceChange.objects.filter(notebook = ntbk)
    if len(npcs) == 0:
        print ntbk
        npc = NotebookPriceChange()
        npc.notebook = ntbk
        npc.price = ntbk.min_price
        npc.date = date.today()
        npc.save()

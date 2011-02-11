import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

notebooks = dict([[ntbk.id, ntbk] for ntbk in Notebook.objects.all()])

for notebook in Notebook.objects.all():
    print notebook
    try:
        ntbks = [notebooks[int(nid)] for nid in notebook.similar_notebooks.split(',')]
    except:
        print '*'
        similar_notebooks = [str(ntbk.id) for ntbk in notebook.findSimilarNotebooks()]
        notebook.similar_notebooks = ','.join(similar_notebooks)

        notebook.save()
 

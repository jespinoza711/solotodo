import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador.models import *

for notebook in Notebook.objects.all():
    print notebook
    similar_notebooks = [str(ntbk.id) for ntbk in notebook.findSimilarNotebooks()]
    notebook.similar_notebooks = ','.join(similar_notebooks)

    notebook.save()
 

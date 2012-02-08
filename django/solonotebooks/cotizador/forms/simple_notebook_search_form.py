from django.forms import forms
from django.forms.fields import DecimalField
from django.forms.models import ModelChoiceField
from solonotebooks.cotizador.models import NotebookType

class SimpleNotebookSearchForm(forms.Form):
    notebook_type = ModelChoiceField(queryset=NotebookType.objects.all(), initial=NotebookType.objects.get(name='Juegos'))
    max_price = DecimalField(decimal_places=0)
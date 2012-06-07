# coding=utf-8
from django.forms import forms
from django.forms.models import ModelChoiceField
from solonotebooks.cotizador.models.notebook import Notebook
from solonotebooks.cotizador.models.notebook_brand import NotebookBrand
from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity

class RipleyNotebookSearchForm(forms.Form):
    brand = ModelChoiceField(queryset=NotebookBrand.objects.all(),
        required=False, label='Marca')

    def __init__(self, *args, **kwargs):
        super(RipleyNotebookSearchForm, self).__init__(*args, **kwargs)
        self.is_valid()

    def notebook_list(self):
        available_entities = StoreHasProductEntity.objects.filter(
            is_available=True,
            store__name='Ripley',
            shp__isnull=False
        )

        notebook_entity_dict = dict([[e.shp.product.id, e] for e in available_entities])
        notebooks = Notebook.objects.filter(pk__in=notebook_entity_dict.keys())

        brand = self.cleaned_data['brand']
        if brand:
            notebooks = notebooks.filter(line__brand=brand)

        for notebook in notebooks:
            notebook.price = notebook_entity_dict[notebook.id].latest_price

        notebooks = sorted(notebooks, key=lambda n: n.price)

        return notebooks



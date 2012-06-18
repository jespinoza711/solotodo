# coding=utf-8
from decimal import Decimal
from django.forms import forms
from django.forms.models import ModelChoiceField
from solonotebooks.cotizador.models.notebook import Notebook
from solonotebooks.cotizador.models.notebook_brand import NotebookBrand
from solonotebooks.cotizador.models.product import format_currency
from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity
from solonotebooks.cotizador.models.store import Store


class RipleyNotebookSearchForm(forms.Form):
    brand = ModelChoiceField(queryset=NotebookBrand.objects.all(),
        required=False, label='Marca')

    def __init__(self, *args, **kwargs):
        super(RipleyNotebookSearchForm, self).__init__(*args, **kwargs)
        self.is_valid()

    def notebook_list(self):
        from solonotebooks.cotizador.views_ripley import considered_store_ids

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
            notebook.other_prices = dict()

        dicts = {}
        for store_id in considered_store_ids:
            if store_id == 18:
                continue
            store = Store.objects.get(pk=store_id)
            entities = StoreHasProductEntity.objects.filter(
                is_available=True,
                store=store,
                shp__isnull=False,
                shp__product__in=notebooks
            )
            entity_dict = dict([[e.shp.product.id, format_currency(Decimal(e.latest_price))] for e in entities])
            dicts[store.name] = entity_dict

        for key, value in dicts.items():
            for notebook in notebooks:
                notebook.other_prices[key] = value.get(notebook.id, 0)

        notebooks = sorted(notebooks, key=lambda n: n.price)


        return notebooks



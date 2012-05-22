# coding=utf-8
from django.forms import forms
from django.forms.fields import DecimalField, ChoiceField
from django.forms.widgets import HiddenInput
from solonotebooks.cotizador.models.notebook import Notebook
from solonotebooks.cotizador.models.store import Store
from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity

class HponlineSearchForm(forms.Form):
    notebook_type = ChoiceField(choices=[
        (1, u'Hogar y Oficina - Revisar correos y Facebook, usar Office, ver videos de Youtube, y correr juegos ligeros.'),
        (2, u'Juegos - Correr aplicaciones y juegos 3D pesados (PES, Call of Duty, Battlefield, Starcraft, etc.)'),
        (3, u'Netbooks - Pequeños y baratos, para tareas muy básicas de Internet y Office.'),
        (4, u'Ultraportátiles - Equipos ligeros de alta autonomía para tareas de hogar y oficina.'),
    ], initial=2)
    max_price = DecimalField(decimal_places=0, widget=HiddenInput, initial=400000)

    def find_best_notebook(self):
        max_price = self.cleaned_data['max_price']
        store = Store.objects.get(name='HP Online')
        available_entities = StoreHasProductEntity.objects.filter(
            store=store,
            is_available=True,
            shp__isnull=False,
            latest_price__lte=max_price
        )
        notebook_entity_dict = dict([[e.shp.product.id, e] for e in available_entities])
        notebooks = Notebook.objects.filter(pk__in=notebook_entity_dict.keys())

        notebook_type = int(self.cleaned_data['notebook_type'])

        if notebook_type == 1:
            # Hogar y oficina
            notebooks = notebooks.filter(
                processor__speed_score__gte=1000,
                ram_quantity__value__gte=2,
                storage_drive__capacity__value__gte=250,
                screen__size__family__base_size__gte=13
            ).order_by('-processor__speed_score')
        elif notebook_type == 2:
            # Juegos
            notebooks = notebooks.filter(
                processor__speed_score__gte=2000,
                ram_quantity__value__gte=3,
                storage_drive__capacity__value__gte=320,
                screen__size__family__base_size__gte=14,
                video_card__speed_score__gte=4000
            ).order_by('-video_card__speed_score')
        elif notebook_type == 3:
            # Netbooks
            notebooks = notebooks.filter(
                screen__size__family__base_size=10,
            ).order_by('-processor__speed_score')
        elif notebook_type == 4:
            # Ultraportátiles
            notebooks = notebooks.filter(
                processor__consumption=2,
                screen__size__family__base_size__gte=11,
                screen__size__family__base_size__lte=13,
            ).order_by('-processor__speed_score')

        if notebooks:
            return notebooks[0], notebook_entity_dict[notebooks[0].id]
        else:
            return None, None


from datetime import date
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity

shpes = StoreHasProductEntity.objects.filter(
    shp__isnull=False
).select_related('resolved_by', 'shp')

result = []

for shpe in shpes:
    try:
        resolve_date = str(shpe.date_resolved.date())
    except AttributeError:
        resolve_date = None

    result.append(
        [
            shpe.url,
            shpe.shp.product_id,
            shpe.resolved_by_id,
            resolve_date
        ]
    )

print simplejson.dumps(result, indent=4)

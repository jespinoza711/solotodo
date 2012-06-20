import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity

shpes = StoreHasProductEntity.objects.filter(
    shp__isnull=False
)

result = []

for shpe in shpes:
    try:
        resolver_id = shpe.resolved_by.id
    except AttributeError:
        resolver_id = None

    result.append(
        [
            shpe.url,
            shpe.shp.product.id,
            resolver_id
        ]
    )

print simplejson.dumps(result, indent=4)

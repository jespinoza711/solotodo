import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'
import simplejson

from solonotebooks.cotizador.models.store_has_product_entity import StoreHasProductEntity

shpes = StoreHasProductEntity.objects.filter(
    shp__isnull=False
).select_related('shp')

total_shpes = shpes.count()

result = []

for idx, shpe in enumerate(shpes):
    print >> sys.stderr, '{0} de {1}'.format(idx+1, total_shpes)

    try:
        resolve_date = str(shpe.date_resolved.date())
    except AttributeError:
        resolve_date = None

    try:
        str_date = str(shpe.date_resolved.date())
    except AttributeError:
        str_date = None

    result.append(
        [
            shpe.url,
            shpe.shp.product_id,
            shpe.resolved_by_id,
            str_date
        ]
    )

print simplejson.dumps(result, indent=4)

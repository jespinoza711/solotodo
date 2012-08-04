from boto.s3.key import Key
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

import sys
from boto.s3.connection import S3Connection
from django.conf import settings
from django.db.models import get_model

def main():
    Model = get_model('cotizador', sys.argv[1])

    if not Model:
        print 'Model not found'
        return

    bucket_name = sys.argv[2]
    dir_name = sys.argv[3]

    if len(sys.argv) >= 5:
        min_id = int(sys.argv[4])
    else:
        min_id = 0

    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)


    print 'min_id: ' + str(min_id)

    base_path = settings.MEDIA_ROOT

    models = Model.objects.filter(pk__gt=min_id).order_by('id')

    c = models.count()

    for idx, n in enumerate(models):
        print '{0} de {1}: {2}'.format(idx + 1, c, n.id)
        k = Key(bucket)
        k.key = dir_name + '/' + n.picture.name.split('/')[1]
        full_path = base_path + '/' + n.picture.name

        print k.key
        print full_path

        k.set_contents_from_filename(full_path)

if __name__ == '__main__':
    main()

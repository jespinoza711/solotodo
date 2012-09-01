import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from solonotebooks.cotizador import models
from subprocess import *
import simplejson

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
    
user_list_json = simplejson.loads(run_cmd('python solonotebooks/manage.py dumpdata auth.User'))
staff_user_list = []
staff_user_ids = []

for user_json in user_list_json:
    f = user_json['fields']
    if f['is_staff']:
        user_json['fields']['groups'] = []
        staff_user_list.append(user_json)
        staff_user_ids.append(user_json['pk'])
    
print simplejson.dumps(staff_user_list, sort_keys=True, indent=4)

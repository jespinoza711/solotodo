import sys
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

for user_json in user_list_json:
    user_json['fields']['groups'] = []

old_user_profile_list_json_string = run_cmd('python solonotebooks/manage.py dumpdata cotizador.UserProfile')
user_profile_list_json = simplejson.loads(old_user_profile_list_json_string.replace('cotizador.', 'backend.'))

for user_profile_json in user_profile_list_json:
    new_fields = {}
    f = user_profile_json['fields']
    new_fields['user'] = f['user']
    new_fields['assigned_product_types'] = f['managed_product_types']
    new_fields['is_api_client'] = False
    user_profile_json['fields'] = new_fields

user_list_json.extend(user_profile_list_json)
    
print simplejson.dumps(user_list_json, sort_keys=True, indent=4)

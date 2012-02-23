import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.conf import settings
import urllib2
import re
import simplejson

def test_new_user_can_login_without_existing_facebook_session():
    facebook_user_name = 'Dexter Morgan'
    email, password = create_facebook_test_user(facebook_user_name)

    driver = webdriver.Chrome()

    driver.get(settings.SERVER_NAME)

    login_button = driver.find_element_by_class_name('fb_button_text')
    login_button.click()

    WebDriverWait(driver, 10).until(lambda d : len(d.window_handles) > 1)

    main_window_handler = driver.window_handles[0]
    facebook_popup_handler = driver.window_handles[-1]

    driver.switch_to_window(facebook_popup_handler)

    email_field = driver.find_element_by_name('email')
    email_field.send_keys(email)

    password_field = driver.find_element_by_name('pass')
    password_field.send_keys(password)

    password_field.submit()

    grant_button = driver.find_element_by_name('grant_clicked')
    time.sleep(2)
    grant_button.click()

    driver.switch_to_window(main_window_handler)
    time.sleep(10)

    full_name_container = driver.find_element_by_class_name('full_name')
    print full_name_container.text == facebook_user_name
    driver.close()

def create_facebook_test_user(full_name):
    access_token = get_facebook_app_access_token()
    encoded_full_name = urllib2.quote(full_name)
    url = 'https://graph.facebook.com/%s/accounts/test-users?installed=true&name=%s&permissions=read_stream&method=post&access_token=%s' % (settings.FACEBOOK_ID, encoded_full_name, access_token,)
    result = urllib2.urlopen(url)
    user_data = simplejson.load(result)
    email = user_data['email']
    password = user_data['password']
    return email, password

def get_facebook_app_access_token():
    url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials' % (settings.FACEBOOK_ID, settings.FACEBOOK_SECRET,)
    result = urllib2.urlopen(url).read()

    r = re.match(r'access_token=((\w|\|)+)', result)
    if not r:
        raise ValueError
    access_token = r.groups()[0]
    return access_token

# Script to test the fetch script for a store
def main():
    test_new_user_can_login_without_existing_facebook_session()

if __name__ == '__main__':
    main()


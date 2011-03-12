#-*- coding: UTF-8 -*-
from django import forms
import datetime

class AdvertisementSlotDetailsForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today() - datetime.timedelta(days = 30))
    end_date = forms.DateField(initial = datetime.date.today())

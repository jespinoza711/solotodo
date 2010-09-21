#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length = 255, widget = forms.PasswordInput)
    new_password = forms.CharField(max_length = 255, widget = forms.PasswordInput)
    repeat_new_password = forms.CharField(max_length = 255, widget = forms.PasswordInput)
    
    def validate_password_and_form(self, user):
        if not self.is_valid():
            return False
        else:
            flag = True
            if not user.check_password(self.cleaned_data['old_password']):
                errors = self._errors.setdefault('old_password', ErrorList())
                errors.append(u'La contraseña original no es valida')
                flag = False
            if self.cleaned_data['new_password'] != self.cleaned_data['repeat_new_password']:
                errors = self._errors.setdefault('repeat_new_password', ErrorList())
                errors.append(u'Las nuevas contraseñas no concuerdan')
                flag = False
            return flag

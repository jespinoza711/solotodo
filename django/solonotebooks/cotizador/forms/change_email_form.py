#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList

class ChangeEmailForm(forms.Form):
    password = forms.CharField(max_length = 255, widget = forms.PasswordInput)
    new_email = forms.EmailField()
    
    def validate_password_and_form(self, user):
        if not self.is_valid():
            return False
        else:
            if not user.check_password(self.cleaned_data['password']):
                errors = self._errors.setdefault('password', ErrorList())
                errors.append(u'La contraseña no es valida')
                return False
            else:
                return True

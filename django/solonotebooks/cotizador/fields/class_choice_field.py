from django import forms

class ClassChoiceField(forms.ModelChoiceField):
    def __init__(self, class_name):
        self.class_name = class_name
        super(ClassChoiceField, self).__init__(class_name.objects.all(), 'Cualquiera')
        

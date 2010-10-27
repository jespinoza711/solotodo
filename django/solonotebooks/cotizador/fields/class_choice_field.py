from django import forms

class ClassChoiceField(forms.ModelChoiceField):
    def __init__(self, class_name, name, default_name = 'Cualquiera'):
        self.class_name = class_name
        self.name = name
        super(ClassChoiceField, self).__init__(class_name.objects.all(), default_name)
        
    def get_object_name(self, pk):
        return str(self.class_name.objects.get(pk = pk))

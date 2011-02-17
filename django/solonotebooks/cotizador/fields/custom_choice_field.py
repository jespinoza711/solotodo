from django.forms import ChoiceField

class CustomChoiceField(ChoiceField):
    def get_object_name(self, pk):
        return str(dict(self.choices)[pk])
        
    def set_name(self, name):
        self.name = name
        return self
        
    def does_require_advanced_controls(self):
        self.requires_advanced_controls = True
        return self

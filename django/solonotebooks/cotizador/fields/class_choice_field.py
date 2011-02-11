from django import forms

class ClassChoiceField(forms.ModelChoiceField):
    def __init__(self, class_name, name, default_name = 'Cualquiera', in_quick_search = False, requires_advanced_controls = False, widget = forms.Select):
        self.class_name = class_name
        self.name = name
        self.in_quick_search = in_quick_search
        self.requires_advanced_controls = requires_advanced_controls
        super(ClassChoiceField, self).__init__(class_name.objects.all(), default_name, widget = widget)
        
    def get_object_name(self, pk):
        return str(self.class_name.objects.get(pk = pk))

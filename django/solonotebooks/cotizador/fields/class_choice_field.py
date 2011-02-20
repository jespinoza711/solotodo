from django import forms

class ClassChoiceField(forms.ModelChoiceField):
    def __init__(self, class_name, name, default_name = 'Cualquiera', in_quick_search = False, requires_advanced_controls = False, widget = forms.Select, quick_search_name = ''):
        self.class_name = class_name
        self.name = name
        self.in_quick_search = in_quick_search
        self.quick_search_name = quick_search_name
        self.requires_advanced_controls = requires_advanced_controls
        super(ClassChoiceField, self).__init__(class_name.objects.all(), default_name, widget = widget)
        
    def get_object_name(self, pk):
        return str(self.class_name.objects.get(pk = pk))
        
    def set_widget(self, widget):
        self.widget = widget
        self.is_slider = True
        return self
        
    @staticmethod
    def generate_slider(classname):
        first = ClassChoiceField(classname, '', default_name = None)
        first.widget = forms.Select(attrs = {'class': 'custom_range_select'})
        second = ClassChoiceField(classname, '', default_name = None)
        second.widget = forms.Select(attrs = {'class': 'custom_range_select'})
        try:
            first.default_slider_value = classname.objects.all()[0].id
            second.default_slider_value = classname.objects.reverse()[0].id
        except:
            first.default_slider_value = 0
            second.default_slider_value = 0
        second.has_css_slider = True
        return [first, second]

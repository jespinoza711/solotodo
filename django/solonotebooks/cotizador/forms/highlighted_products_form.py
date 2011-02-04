from django import forms

class HighlightedProductsForm(forms.Form):
    highlighted_ordering = forms.ChoiceField(choices = 
        (('1', 'Nuevos'), 
        ('2', 'Populares'),
        ('3', 'Ofertas')))
        
    @staticmethod
    def initialize(args):
        hnf = HighlightedProductsForm(args)
        if not hnf.is_valid():
            hnf.cleaned_data = {'highlighted_ordering': '3'}
            
        return hnf
        
    def apply_filter(self, products):
        ordering = self.cleaned_data['highlighted_ordering']
        if ordering == '1':
            result_products = products.order_by('-date_added')
        elif ordering == '2':
            result_products = products.order_by('-week_visitor_count')
        elif ordering == '3':
            result_products = products.order_by('-week_discount')
            
        return result_products
            
        

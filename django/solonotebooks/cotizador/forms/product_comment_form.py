from django import forms

class ProductCommentForm(forms.Form):
    comments = forms.CharField(widget = forms.Textarea)
    nickname = forms.CharField(max_length = 255, required = False)

from django import forms

class NotebookCommentForm(forms.Form):
    comments = forms.CharField(widget = forms.Textarea)
    nickname = forms.CharField(max_length = 255)

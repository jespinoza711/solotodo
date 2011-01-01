import urllib, hashlib
from django import template
from solonotebooks import settings

register = template.Library()
    
@register.inclusion_tag('templatetags/display_notebook.html')
def display_notebook(notebook, show_options = True):
    return {
        'notebook': notebook, 
        'show_options': show_options
    }
    
@register.inclusion_tag('templatetags/display_notebook_as_table.html')
def display_notebook_as_table(notebook):
    return {
        'notebook': notebook, 
    }

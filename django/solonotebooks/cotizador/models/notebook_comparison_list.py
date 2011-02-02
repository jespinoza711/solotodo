from django.db import models

class NotebookComparisonList(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    notebooks = models.ManyToManyField('Product')
    
    def __unicode__(self):
        return str(self.notebooks.all())
    
    class Meta:
        app_label = 'cotizador'

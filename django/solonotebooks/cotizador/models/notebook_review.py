from django.db import models
from solonotebooks.cotizador.models import Notebook

class NotebookReview(models.Model):
    SCORE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    score_construction = models.IntegerField(choices = SCORE_CHOICES)
    score_speed = models.IntegerField(choices = SCORE_CHOICES)
    score_mobility = models.IntegerField(choices = SCORE_CHOICES)
    score_total = models.IntegerField(choices = SCORE_CHOICES)
    ip_address = models.IPAddressField()
    comments = models.TextField()
    email = models.EmailField()
    date = models.DateField()
    nickname = models.CharField(max_length = 255)
    
    notebook = models.ForeignKey(Notebook)
    
    def __unicode__(self):
        return 'Review de ' + unicode(self.notebook)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook review'

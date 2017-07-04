from django.db import models

class Visit(models.Model):
    user = models.ForeignKey('auth.User', 
                             related_name='visits', 
                             on_delete=models.CASCADE,
                             null=True)
    domain = models.CharField(max_length=200)
    startTime = models.DateTimeField()
    duration = models.FloatField()

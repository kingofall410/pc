from django.db import models

class Visit(models.Model):
    user = models.ForeignKey('auth.User', 
                             related_name='visits', 
                             on_delete=models.CASCADE,
                             null=True)
    domain = models.CharField(max_length=200)
    startTime = models.DateTimeField()
    duration = models.FloatField()
    
    def __str__(self):
        return self.domain+": "+str(self.duration)+" seconds @ "+str(self.startTime);

#A source defining a set of biases (ie: 1-5)
class BiasSetDefinition(models.Model):
    domain = models.CharField(max_length=200)
    nrLevels = models.IntegerField()

#An individual bias (ie: "lean left") from a BiasSetDefinition
class BiasDefinition(models.Model):
    set = models.ForeignKey('BiasSetDefinition', 
                            related_name='biases', 
                            on_delete=models.CASCADE, 
                            null=False)
    levelLabel = models.CharField(max_length=50)
    level = models.IntegerField()
    normalizedLevel = models.FloatField()
    textDesc = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        self.normalizedLevel = self.level
        super(BiasDefinition, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.levelLabel

#A source of information to be given a bias
class Source(models.Model):
    sitename = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True)
    domain = models.CharField(max_length=200)
    bias = models.ManyToManyField(BiasDefinition)

    def __str__(self):
        return self.sitename
      
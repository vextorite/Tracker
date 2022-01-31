from django.db import models

# Create your models here.

class Issue(models.Model):
    title = models.CharField(max_length=250)
    
    description = models.TextField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    priority = 1

    def __str__(self):
        return self.title
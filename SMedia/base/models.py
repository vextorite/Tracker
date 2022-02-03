from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    priority = 1
    state = 'pending fix'
    project = models.ForeignKey(Project, default=None ,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


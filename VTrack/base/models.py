from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
import uuid

# Create your models here.

STATE_CHOICES = [('Open', 'Open'), ('Closed', 'Closed'),('Overdue', 'Overdue'),('Due Now', 'Due Now'),('Due Later', 'Due Later')]
PRIORITY_CHOICES = [('Urgent', 'Urgent'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]

class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def due_date():
    now = timezone.now()
    return now + timezone.timedelta(days=7)

class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    return_date = models.DateField(default=due_date) 
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Open')
    project = models.ForeignKey(Project, default=None ,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


from django.contrib import admin
from .models import Issue, Project

# Register your models here.
admin.site.register(Issue)
admin.site.register(Project)
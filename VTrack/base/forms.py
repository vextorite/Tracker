from django.forms import ModelForm
from .models import Issue, Project

class Issue_Form(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'

class Project_Form(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
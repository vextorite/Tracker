from django.forms import ModelForm
from .models import Issue

class Issue_Form(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'
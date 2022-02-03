from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue
from .forms import Issue_Form

# Create your views here.


def home(request):
    logged_issues = Issue.objects.all()
    return render(request, 'base/home.html', context={'issues':logged_issues})

def issue(request, pk):
    issue = Issue.objects.get(id=pk)
    return render(request, 'base/issue.html', context={'issue':issue})

def create_issue(request):
    form = Issue_Form()
    if request.method == 'POST':
        form = Issue_Form(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'base/issue_form.html', context={'form':form})
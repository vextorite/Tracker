from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Issue, Project
from .forms import Issue_Form, Project_Form

# Create your views here.


def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''        #setup for search by project
    logged_issues = Issue.objects.filter(project__title__icontains=query)       #accounting for wildcard searches
    projects = Project.objects.all()
    return render(request, 'base/home.html', context={'issues':logged_issues, 'projects': projects})

def issue(request, pk):
    issue = Issue.objects.get(id=pk)
    return render(request, 'base/issue.html', context={'issue':issue})

def create_issue(request):
    form = Issue_Form()
    if request.method == 'POST':
        form = Issue_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/issue_form.html', context={'form':form})

def update_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    form = Issue_Form(instance=issue)

    if request.method == 'POST':
        form = Issue_Form(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/issue_form.html', context={'form':form})

def create_project(request):
    form = Project_Form
    if request.method == 'POST':
        form = Project_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/project_form.html', context={'form':form})

def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    form = Project_Form(instance=project)

    if request.method == 'POST':
        form = Project_Form(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/project_form.html', context={'form':form})

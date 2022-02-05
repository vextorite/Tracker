from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Issue, Project
from .forms import Issue_Form, Project_Form
from datetime import date

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or Password')

    return render(request, 'base/reg_login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''        #setup for search by project
    logged_issues = Issue.objects.filter(
        Q(project__title__icontains=query)|
        Q(title__icontains=query))       #accounting for wildcard searches
    projects = Project.objects.all()
    issues = Issue.objects.all()
    for issue in issues:                #There's probably a better way to update this dynamically
        now = date.today()
        if (issue.return_date - now).days<1:
            if(issue.state == 'Closed'):
                continue
            else:
                issue.state = 'Overdue'
                issue.save()
        elif (issue.return_date - now).days==0:
            issue.state = 'Due Now'
            issue.save()
        elif (issue.return_date - now).days>1 and (issue.return_date - now).days<=7:
            issue.state = 'Due Later'
            issue.save()
    counts = [
        logged_issues.filter(state='Open').count()+logged_issues.filter(state='Due Now').count()+logged_issues.filter(state='Due Later').count(), 
        logged_issues.filter(state='Closed').count(),
        logged_issues.filter(state='Overdue').count(),
        logged_issues.filter(state='Due Now').count(),
        logged_issues.filter(state='Due Later').count()]
        
    return render(request, 'base/home.html', context={'issues':logged_issues, 'projects': projects, 'counts': counts})

@login_required(login_url='login')
def issue(request, pk):
    issue = Issue.objects.get(id=pk)
    return render(request, 'base/issue.html', context={'issue':issue})

@login_required(login_url='login')
def create_issue(request):
    form = Issue_Form()
    if request.method == 'POST':
        form = Issue_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/issue_form.html', context={'form':form})

@login_required(login_url='login')
def update_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    form = Issue_Form(instance=issue)

    if request.method == 'POST':
        form = Issue_Form(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/issue_form.html', context={'form':form})

@login_required(login_url='login')
def create_project(request):
    form = Project_Form
    if request.method == 'POST':
        form = Project_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/project_form.html', context={'form':form})

@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    form = Project_Form(instance=project)

    if request.method == 'POST':
        form = Project_Form(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/project_form.html', context={'form':form})

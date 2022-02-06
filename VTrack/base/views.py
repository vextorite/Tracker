from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from scipy.fftpack import idctn
from .models import Issue, Project, Comment
from .forms import Issue_Form, Project_Form
from datetime import date

# Create your views here.

def login_view(request):

    page_val = "login"

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    return render(request, 'base/reg_login.html', context={'page': page_val})

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error creating account. Please contact Administrator!')
    return render(request, 'base/reg_login.html', context={'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''        #setup for search by project
    logged_issues = Issue.objects.filter(
        Q(project__title__icontains=query)|
        Q(title__icontains=query)|
        Q(description__icontains=query))       #accounting for wildcard searches
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
        elif issue.state == 'Closed':
            pass
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

    issue_messages = Comment.objects.filter(
        Q(issue__title__icontains=query)|
        Q(issue__project__title__icontains=query)).order_by('-dateCreated')[:10]
        
    return render(request, 'base/home.html', context={'issues':logged_issues, 'projects': projects, 'counts': counts, 'comments': issue_messages})

@login_required(login_url='login')
def issue(request, pk):
    issue = Issue.objects.get(id=pk)
    comments = issue.comment_set.all().order_by('-dateCreated')
    users = issue.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            issue = issue,
            body = request.POST.get('body')
        )
        issue.participants.add(request.user)
        return redirect('issue', pk=issue.id)
    return render(request, 'base/issue.html', context={'issue':issue, 'comments':comments, 'users': users})

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

@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={'object': comment})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import AuthenticationForm

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'todo/index.html', {'form': form, 'tasks': tasks})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/login/')

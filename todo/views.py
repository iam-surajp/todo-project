from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import todo_task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
    
def signup_view(request):
    if request.method == 'GET':    
        return render(request, 'signup.html',{'form':UserCreationForm})

    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                try:
                    user = form.save()
                    return redirect('login')
                except IntegrityError:
                    return render(request, 'signup.html', {'form': form, 'error': 'Username already exists'})
            else:
                return render(request, 'signup.html', {'form': form, 'error': 'Passwords do not match'})
        else:
            print(form.errors)
            return render(request, 'signup.html', {'form': form, 'error': 'Form is not valid. Please check the inputs.'})


def logout_view(request):
        logout(request)
        return redirect('login')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',{'form':AuthenticationForm,'error':'username or password incorrect'})
        else:
            login(request,user)
            return redirect('home')
            

@login_required
def home(request):
    todos = Tasks.objects.filter(user = request.user,datecompleted__isnull=True)
    return render(request, 'home.html',{'tasks':todos})

@login_required
def completed_tasks(request):
    todos = Tasks.objects.filter(user = request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completed_tasks.html',{'todos':todos})

@login_required
def add_task(request):
    if request.method == 'GET':
        return render(request, 'add_task.html',{'form':todo_task})
    else:
        try:
            form = todo_task(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('home')
        except ValueError:
            return render(request, 'add_task.html',{'form':todo_task,'error':'value exceed'})


@login_required
def view_task(request,todo_pk):
    if request.method == 'GET': 
        todos = get_object_or_404(Tasks,pk=todo_pk,user=request.user)
        return render(request,'view_task.html',{'todos':todos})

@login_required
def update_task(request,todo_pk):
    todos = get_object_or_404(Tasks,pk=todo_pk,user=request.user)
    if request.method =='GET':
        todoform = todo_task(instance=todos)
        return render(request, 'update_task.html',{'todo':todos,'form':todoform})
    else:
        try:
            form = todo_task(request.POST,instance=todos)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'update_task.html',{'todos':todos,'form':todoform,'error':'value error'})

@login_required
def mark_complete(request,todo_pk):
    todos = get_object_or_404(Tasks,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.datecompleted = timezone.now()
        todos.save()
        return redirect('home')


@login_required
def delete_task(request,todo_pk):
    todos = get_object_or_404(Tasks,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('home')
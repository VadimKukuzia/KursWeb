from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import *
# Create your views here.


def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return redirect('index')


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            print('aaaa')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/sign_in.html', {'form': form})


def sign_up(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'tasks/sign_up.html', {'form': form})


def index(request):
    lists = TaskList.objects.filter(user_id=request.user.id).order_by('id')

    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
        return redirect('/')

    form = TaskListForm()
    context = {'lists': lists, 'form': form, 'user': request.user}
    return render(request, 'tasks/lists.html', context)


def delete_list(request, list_id):
    task_list = TaskList.objects.get(id=list_id)

    if request.method == 'POST':
        task_list.delete()
        return redirect('index')

    return redirect('index')


def list_tasks(request, list_id):
    tasks = Task.objects.filter(task_list_id=list_id).order_by('id')
    lists = TaskList.objects.filter(user_id=request.user.id).order_by('id')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.task_list = TaskList.objects.get(id=list_id)
            instance.save()
        else:
            print("Форма не валидна")
        return redirect(f'/{list_id}/tasks')

    form = TaskForm()
    context = {'tasks': tasks, 'form': form, 'lists': lists, 'list': TaskList.objects.get(id=list_id)}
    return render(request, 'tasks/task_list.html', context)


def update_task(request, pk, list_id):
    task = Task.objects.get(id=pk)
    tasks = Task.objects.all().order_by('id')
    lists = TaskList.objects.all().order_by('id')

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(f'/{list_id}/tasks')

    context = {'form': form, 'pk': task.id, 'tasks': tasks, 'lists': lists}

    return render(request, 'tasks/update_task.html', context)


def delete_task(request, pk, list_id):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect(f'/{list_id}/tasks')

    return redirect(f'/{list_id}/tasks')

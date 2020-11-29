from django.conf.global_settings import EMAIL_HOST
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.mail import send_mail
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
            messages.info(request, 'Имя пользователя или пароль не совпадают')
            return render(request, 'tasks/sign_in.html', {'form': form})
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


@login_required(login_url="/sign-in")
def delete_list(request, list_id):
    task_list = TaskList.objects.get(id=list_id)

    if request.method == 'POST':
        task_list.delete()
        return redirect('index')

    return redirect('index')


@login_required(login_url="/sign-in")
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


@login_required(login_url="/sign-in")
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


@login_required(login_url="/sign-in")
def delete_task(request, pk, list_id):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect(f'/{list_id}/tasks')

    return redirect(f'/{list_id}/tasks')


@login_required(login_url="/sign-in")
def send_list_by_email(request, list_id):
    task_list = TaskList.objects.get(id=list_id)
    tasks = Task.objects.filter(task_list_id=list_id).order_by('id')
    email = request.user.email
    text = ''
    for n, el in enumerate(tasks):
        text += f'{n+1}. {el}\n'

    if request.method == 'POST':
        with mail.get_connection() as connection:
            if send_mail(from_email=EMAIL_HOST,
                         subject=f'Список заметок:{task_list}',
                         recipient_list=[email],
                         message=text,
                         fail_silently=False,
                         connection=connection) != 0:
                messages.info(request, 'Письмо было успешно отправлено')
                return redirect('index')

    return redirect('index')

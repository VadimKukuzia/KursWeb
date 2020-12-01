import os
from sys import path

from django.conf.global_settings import EMAIL_HOST
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.core import mail
from django.core.files import File
from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from KursWeb import settings
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
            return redirect('tasks', list_id=instance.id)

    form = TaskListForm()
    context = {'lists': lists, 'form': form, 'user': request.user}
    return render(request, 'tasks/lists.html', context)


def update_email(request):
    lists = TaskList.objects.filter(user_id=request.user.id).order_by('id')
    form = UserEmailEditForm(instance=request.user)

    if request.method == 'POST':
        form = UserEmailEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'tasks/update-email.html', {'form': form, 'lists':lists})


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

    if not any(int(list_id) == el.id for el in lists):
        messages.warning(request, 'У вас нет такого списка')
        return redirect('index')

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
    lists = TaskList.objects.filter(user_id=request.user.id).order_by('id')

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
        if el.complete:
            text += f'{n + 1}. {el} — Х\n'
        else:
            text += f'{n + 1}. {el}\n'

    if request.method == 'POST':
        if tasks.count() > 0:
            with mail.get_connection() as connection:
                if send_mail(from_email=EMAIL_HOST,
                             subject=f'Список заметок:{task_list}',
                             recipient_list=[email],
                             message=text,
                             fail_silently=False,
                             connection=connection) != 0:
                    messages.success(request, f'Письмо со списком "{task_list}" было успешно отправлено на почту {email}')
                    return redirect('tasks', list_id=list_id)
                else:
                    messages.warning(request, 'Не удалость отправить.\nПопробуйте ещё раз')
                    return redirect('tasks', list_id=list_id)
        else:
            messages.warning(request, 'Список пуст')
            return redirect('tasks', list_id=list_id)

    return redirect('tasks', list_id=list_id)


@login_required(login_url="/sign-in")
def download_file(request, list_id):
    task_list = TaskList.objects.get(id=list_id)
    tasks = Task.objects.filter(task_list_id=list_id).order_by('id')
    text = ''
    for n, el in enumerate(tasks):
        if el.complete:
            text += f'{n + 1}. {el} — Х\n'
        else:
            text += f'{n + 1}. {el}\n'

    with open(f'{task_list}.txt', 'w') as file:
        file.write(f'Список - {task_list}:\n{text}')
    if request.method == 'POST':
        if tasks.count() > 0:
            return FileResponse(open(f'{task_list}.txt', 'rb'), as_attachment=True)
        else:
            messages.warning(request, 'Список пуст')
            return redirect('tasks', list_id=list_id)

    os.remove(f'{task_list}.txt')
    return redirect('tasks', list_id=list_id)

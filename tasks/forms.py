from django import forms
from django.forms import ModelForm

from .models import *


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'complete']


class TaskListForm(forms.ModelForm):

    class Meta:
        model = TaskList
        fields = '__all__'

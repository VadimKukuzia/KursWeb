from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['title']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательно к вводу, введите действующую электронную почту',
                             required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if '.ru' or '.com' or '.ua' not in email:
            raise forms.ValidationError('Введите корректный адрес')
        elif user_count > 0:
            raise forms.ValidationError('Такая электронная почта уже есть в базе данных')
        return email

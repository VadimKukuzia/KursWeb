from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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

        if not any(i in email for i in ('.ru', '.com', '.ua', '.net')):
            raise forms.ValidationError('Введите корректный адрес')

        if user_count > 0:
            raise forms.ValidationError('Такая электронная почта уже есть в базе данных')
        return email


class UserEmailEditForm(UserChangeForm):
    email = forms.EmailField(max_length=254, help_text='Обязательно к вводу, введите действующую электронную почту',
                             required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()

        if not any(i in email for i in ('.ru', '.com', '.ua', '.net')):
            raise forms.ValidationError('Введите корректный адрес')

        if user_count > 0:
            raise forms.ValidationError('Такая электронная почта уже есть в базе данных')
        return email

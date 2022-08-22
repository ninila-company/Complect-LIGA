from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    """Форма авторизации."""
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput())

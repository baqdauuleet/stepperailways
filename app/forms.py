from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
        
class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}), label='Имя')
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}), label='Имя пользователя')
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-input"}), label='Адрес электронной почты')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}), label='Подтверждение пароля')
    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такая почта уже существует!')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

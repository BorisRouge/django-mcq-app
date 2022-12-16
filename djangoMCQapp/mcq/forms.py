from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {'class':"form-control"}


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Create your username:', max_length=50)
    password = forms.CharField(label='Create your password:', max_length=256,
                               widget=forms.PasswordInput(render_value=False))


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username:', max_length=50)
    password = forms.CharField(label='Enter your password:', max_length=256,
                               widget=forms.PasswordInput(render_value=True))
from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {'class': "form-control",
                   'id': "form2Example1"}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}))
     # {'class': "form-control",
     #               'id': "form2Example1"}

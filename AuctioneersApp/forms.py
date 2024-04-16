from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Defaulters

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DefaultersForm(forms.ModelForm):
    class Meta:
        model = Defaulters
        fields = '__all__'
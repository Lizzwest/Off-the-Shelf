from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
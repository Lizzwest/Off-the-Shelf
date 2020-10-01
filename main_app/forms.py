from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

class CommentForm(ModelForm):
    helper = FormHelper()
    helper.form_show_label = False
    
    pass
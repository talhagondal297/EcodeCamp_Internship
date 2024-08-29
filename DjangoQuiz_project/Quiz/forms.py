from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',  # Changed label here
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        
class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"
    
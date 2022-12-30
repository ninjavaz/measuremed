from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MeasureForm(ModelForm):
    class Meta:
        model = Measure
        # fields = ['patient', 'topic', 'message', 'sendByEmail', 'plannedOnDate']
        fields = ['patient', 'age', 'height', 'bodyWeight', 'measureDate']

        


class CreateUserForm(UserCreationForm):
    GROUPS_CHOICES =(
    ("patient", "patient"),
    ("doctor", "doctor")
)

    firstName = forms.CharField()
    lastName = forms.CharField()
    userGroup = forms.ChoiceField(choices=GROUPS_CHOICES)

    class Meta:
        model = User
        fields = ['username','firstName', 'lastName', 'email', 'password1', 'password2', 'userGroup']
        
        
        
        

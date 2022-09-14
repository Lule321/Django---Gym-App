from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
"""
class KlijentForm(UserCreationForm):

    class Meta:
        model = Klijent
        fields = ['username', 'password1', 'password2', 'email', 'visina', 'brojClanskeKarte', 'mojTrener']

class TrenerForm(UserCreationForm):
    class Meta:
        model = Trener
        fields = ['username', 'password1', 'password2', 'email']
"""

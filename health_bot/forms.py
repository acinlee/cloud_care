from django import forms
from .models import *
from django.forms import formset_factory

class User_Photo_Model(forms.Form):
    class Meta:
        image = forms.ImageField()
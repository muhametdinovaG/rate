# coding: utf-8

from django import forms
from .models import *


class RatesForm(forms.ModelForm):
    class Meta:
        model = Rates
        fields = "__all__"

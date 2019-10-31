# coding: utf-8

from django.contrib import admin
from modules.core.forms import *
from .models import *


@admin.register(Rates)
class Provider(admin.ModelAdmin):
    form = RatesForm


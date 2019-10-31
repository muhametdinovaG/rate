from django.urls import path
from modules.core.views import *


urlpatterns = [
    path('rate/', PageViewRate.as_view()),
    path('rate2/', rate)
]

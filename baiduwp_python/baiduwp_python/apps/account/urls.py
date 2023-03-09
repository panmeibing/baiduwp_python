from django.contrib import admin
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    re_path(r'bdAccount/$', csrf_exempt(views.BdAccount.as_view()), name='bdAccount'),
]

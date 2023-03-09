from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    re_path(r'login/$', csrf_exempt(views.LoginView.as_view()), name='login'),
    re_path(r'logout/$', csrf_exempt(views.LogoutView.as_view()), name='logout'),
]

from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    re_path(r'resolver/$', csrf_exempt(views.Resolver.as_view()), name='resolver'),
    re_path(r'mSetInfo/$', csrf_exempt(views.MSetInfo.as_view()), name='mSetInfo'),
    re_path(r'fileList/$', csrf_exempt(views.FileList.as_view()), name='fileList'),
    re_path(r'downloadLink/$', csrf_exempt(views.DownloadLink.as_view()), name='downloadLink'),
]

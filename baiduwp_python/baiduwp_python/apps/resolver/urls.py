from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

URL_PATH_WX_FILE_LIST = "wxFileList"
URL_PATH_DOWNLOAD_LINK = "downloadLink"

urlpatterns = [
    re_path(r'resolver/$', csrf_exempt(views.Resolver.as_view()), name='resolver'),
    re_path(r'mSetInfo/$', csrf_exempt(views.MSetInfo.as_view()), name='mSetInfo'),
    re_path(r'fileList/$', csrf_exempt(views.FileList.as_view()), name='fileList'),
    re_path(rf'{URL_PATH_WX_FILE_LIST}/$', csrf_exempt(views.WxFileList.as_view()), name=URL_PATH_WX_FILE_LIST),
    re_path(rf'{URL_PATH_DOWNLOAD_LINK}/$', csrf_exempt(views.DownloadLink.as_view()), name=URL_PATH_DOWNLOAD_LINK),
]

from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from baiduwp_python.settings.config import login_ip_black_list, login_path_white_list, login_path_black_list, admin_path
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.remote_ip_utils import get_client_ip


class LoginRequireMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = request.path
        path = path + "/" if path.startswith("/") and not path.endswith("/") else path
        client_ip = get_client_ip(request)
        if client_ip in login_ip_black_list:
            logger.warning(f"ip ({client_ip}) in ip_black_list want to get server ({path}) but disallow")
            return JsonResponse({"code": 0, "error": "禁止访问"}, status=403)
        if path in ("/", "/index", "/index/"):
            return HttpResponseRedirect(reverse('resolver:resolver'))
        if path.startswith(f"/{admin_path.strip('/')}"):
            return None
        if request.user.is_authenticated or path in login_path_white_list:
            return None
        elif path in login_path_black_list:
            logger.warning(f"{client_ip} in black_list want to get server ({path}) but disallow")
            return JsonResponse({"code": 0, "error": "禁止访问"}, status=403)
        else:
            # return HttpResponseRedirect(reverse('user:login'))
            return HttpResponseForbidden("forbidden")

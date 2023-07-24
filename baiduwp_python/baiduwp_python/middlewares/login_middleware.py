from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from baiduwp_python.middlewares.utils.request_path_utils import normalize_path
from baiduwp_python.settings.config import LOGIN_IP_BLACK_SET, LOGIN_PATH_WHITE_SET, LOGIN_PATH_BLACK_SET, \
    URL_PATH_ADMIN, RESP_CODE_ERROR
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.remote_ip_utils import get_client_ip


class LoginRequireMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = normalize_path(request)
        client_ip = get_client_ip(request)
        if client_ip in LOGIN_IP_BLACK_SET:
            logger.warning(f"ip ({client_ip}) in ip_black_list want to get server ({path}) but disallow")
            return JsonResponse({"code": RESP_CODE_ERROR, "error": "禁止访问"}, status=403)
        elif path in LOGIN_PATH_BLACK_SET:
            logger.warning(f"{client_ip} in black_list want to get server ({path}) but disallow")
            return JsonResponse({"code": RESP_CODE_ERROR, "error": "禁止访问"}, status=403)
        elif path in ("/", "/index", "/index/"):
            return HttpResponseRedirect(reverse('resolver:resolver'))
        elif path.startswith(f"/{URL_PATH_ADMIN.strip('/')}"):
            return None
        elif request.user.is_authenticated or path in LOGIN_PATH_WHITE_SET:
            return None
        else:
            # return HttpResponseRedirect(reverse('user:login'))
            return HttpResponseForbidden("forbidden")

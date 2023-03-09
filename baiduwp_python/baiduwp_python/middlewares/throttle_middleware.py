from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

from baiduwp_python.settings.config import throttle_path_list


class InvitationMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = str(request.path) if request.path else ""
        path = path + "/" if path.startswith("/") and not path.endswith("/") else path
        if path not in throttle_path_list:
            return None
        redis_conn = get_redis_connection("default")
        inv_code_redis = redis_conn.get("bdwp:invitation_code")
        if not inv_code_redis:
            return None
        invitation_code = request.COOKIES.get("invitation_code")
        if not invitation_code:
            return JsonResponse({"code": 2, "error": "缺少邀请码"})
        print(f"inv_code_redis:{inv_code_redis}, invitation_code:{invitation_code}")
        if str(invitation_code) != str(inv_code_redis):
            res = JsonResponse({"code": 2, "error": "邀请码错误"})
            res.delete_cookie("invitation_code")
            return res


class StatisticsMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = str(request.path) if request.path else ""
        path = path + "/" if path.startswith("/") and not path.endswith("/") else path
        redis_conn = get_redis_connection("default")
        redis_conn.incrby("bdwp:totalVisitCount", 1)
        count_key = ""
        if path == "/mSetInfo/":
            count_key = "bdwp:msetCount"
        elif path == "/fileList/":
            count_key = "bdwp:fileListCount"
        elif path == "/downloadLink/":
            count_key = "bdwp:downloadLinkCount"
        if count_key:
            redis_conn.incrby(count_key, 1)

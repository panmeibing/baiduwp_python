from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

from baiduwp_python.middlewares.utils.request_path_utils import normalize_path
from baiduwp_python.settings.config import THROTTLE_PATH_LIST, PARSE_COUNT_LIMIT, PARSE_COUNT_EX_TIME, \
    RESP_CODE_INVITATION, RESP_CODE_PARSE_LIMIT
from baiduwp_python.utils.remote_ip_utils import get_client_ip


class InvitationMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = normalize_path(request)
        if path not in THROTTLE_PATH_LIST:
            return None
        redis_conn = get_redis_connection("default")
        inv_code_redis = redis_conn.get("bdwp:invitation_code")
        if not inv_code_redis:
            return None
        invitation_code = request.COOKIES.get("invitation_code")
        if not invitation_code:
            return JsonResponse({"code": RESP_CODE_INVITATION, "error": "缺少邀请码"})
        # print(f"inv_code_redis:{inv_code_redis}, invitation_code:{invitation_code}")
        if str(invitation_code) != str(inv_code_redis):
            res = JsonResponse({"code": RESP_CODE_INVITATION, "error": "邀请码错误"})
            res.delete_cookie("invitation_code")
            return res


class StatisticsMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = normalize_path(request)
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


class ParseCountLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        path = normalize_path(request)
        if path != "/downloadLink/":
            return None
        client_ip = get_client_ip(request)
        # print(f"ParseCountLimitMiddleware client_ip: {client_ip}")
        if not client_ip:
            return JsonResponse({"code": RESP_CODE_PARSE_LIMIT, "error": "获取远程IP失败"})
        redis_conn = get_redis_connection("parse_count_limit")
        used_count = redis_conn.get(client_ip)
        if not used_count:
            redis_conn.setex(client_ip, PARSE_COUNT_EX_TIME, "1")
            return None
        if int(used_count) >= PARSE_COUNT_LIMIT:
            return JsonResponse({"code": RESP_CODE_PARSE_LIMIT, "error": "已到达最大解析次数，请等释放后再尝试"})
        else:
            redis_conn.incrby(client_ip, 1)
            return None

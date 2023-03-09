import json
import traceback
from urllib.parse import unquote

import requests
from django.http import JsonResponse
from django.views import View

from baiduwp_python.apps.account.utils.account_orm import add_account_cookie, del_account_cookie, get_account_cookie
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.header_utils import get_bd_headers


class BdAccount(View):
    def get(self, request):
        res_data = {"code": 0, "error": "", "result": ""}
        username = request.GET.get("username")
        vip_type = request.GET.get("vip_type")
        is_valid = request.GET.get("is_valid")
        if vip_type and not str(vip_type).isdigit():
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        is_ok, data = get_account_cookie(username, vip_type, is_valid)
        if is_ok:
            res_data.update({"code": 1})
            res_data.update({"data": data})
        else:
            res_data.update({"error": data})
        return JsonResponse(res_data)

    def post(self, request):
        res_data = {"code": 0, "error": "", "result": ""}
        cookie = request.POST.get("cookie")
        if not cookie:
            res_data.update({"error": "缺少参数"})
            return JsonResponse(res_data)
        bdclnd = ""
        for coo in str(cookie).split(";"):
            if "BDCLND=" in coo:
                bdclnd = str(coo).replace("BDCLND=", '').strip()
        if not bdclnd:
            res_data.update({"error": "从cookie提取bdclnd失败"})
            return JsonResponse(res_data)
        bdclnd = unquote(bdclnd)
        try:
            url = "https://pan.baidu.com/rest/2.0/xpan/nas?access_token=&method=uinfo"
            headers = get_bd_headers()
            headers.update({"Cookie": cookie})
            res_json = requests.get(url, headers=headers).json()
        except Exception as e:
            logger.error(f"get account info by cookie meet error: {traceback.format_exc()}")
            res_data.update({"error": f"请求账户信息遇到错误: {e}"})
            return JsonResponse(res_data)
        if res_json["errno"] != 0:
            res_data.update({"error": "获取账户信息失败，请检查cookie是否有效"})
            return JsonResponse(res_data)

        is_ok, data = add_account_cookie(
            res_json.get("baidu_name"), res_json.get("netdisk_name"), res_json.get("uk"),
            res_json.get("vip_type"), bdclnd, cookie
        )
        if not is_ok:
            res_data.update({"error": data})
            return JsonResponse(res_data)
        res_data.update({"code": 1, "result": data})
        return JsonResponse(res_data)

    def delete(self, request):
        res_data = {"code": 0, "error": "", "result": ""}
        try:
            ids = json.loads(request.body.decode()).get("ids")
        except Exception as e:
            res_data.update({"error": "缺少参数或参数错误"})
            return JsonResponse(res_data)
        if not ids or not isinstance(ids, list):
            res_data.update({"error": "缺少参数或参数错误"})
            return JsonResponse(res_data)
        is_ok, data = del_account_cookie(ids)
        if not is_ok:
            res_data.update({"error": data})
            return JsonResponse(res_data)
        res_data.update({"code": 1})
        res_data.update({"result": "成功删除{}条记录".format(data)})
        return JsonResponse(res_data)

import json
import re
from time import time
from urllib.parse import urlencode, unquote, quote, quote_plus, unquote_plus

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from baiduwp_python.apps.account.utils.cookie_orm import get_cookie_from_db
from baiduwp_python.settings.config import RESP_CODE_ERROR, RESP_CODE_SUCCESS, WX_LIST_ERROR_TYPE, DL_INFO_EX_TIME
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.header_utils import get_bd_headers


class Resolver(View):
    def get(self, request):
        return render(request, 'baiduwp_frontend/resolver.html')


class MSetInfo(View):
    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR, "error": ""}
        share_url = request.POST.get("share_url")
        pwd = request.POST.get("pwd")
        share_url = str(share_url).strip() if share_url else ""
        pwd = str(pwd).strip() if pwd else ""
        if not all([share_url, pwd]):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        if not share_url.startswith("https://pan.baidu.com/s/"):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        s_url = share_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        url = share_url.split("?")[0] + f"?pwd={pwd}"
        if not s_url or s_url not in url:
            res_data.update({"error": "提取surl失败"})
            return JsonResponse(res_data)
        is_ok, data = get_cookie_from_db(vip_type=2)
        if not is_ok:
            res_data.update({"error": data})
            return JsonResponse(res_data)
        headers = get_bd_headers()
        headers.update({"Cookie": data.get("cookie")})
        try:
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                res_data.update({"error": f"获取mset响应码为{res.status_code}"})
                return JsonResponse(res_data)
            html = res.text
        except Exception as e:
            logger(f"MSetInfo POST: request url {url} failed: {e}")
            res_data.update({"error": "请求mset失败"})
            return JsonResponse(res_data)

        # html = get_html_by_selenium(url)

        match_res = re.findall('locals.mset\((?P<resJson>\{.*?\})\)', html)
        if not match_res:
            res_data.update({"error": "匹配文件信息失败（locals.mset）"})
            return JsonResponse(res_data)
        try:
            files_info = json.loads(match_res[0])
        except Exception as e:
            logger.error(f"MSetInfo POST: json.loads error: {e}, match_res[0]: {match_res[0]}")
            res_data.update({"error": f"将匹配信息转换成JSON时出错"})
            return JsonResponse(res_data)
        if not files_info.get("file_list"):
            res_data.update({"error": "获取文件列表失败（locals.mset）"})
            return JsonResponse(res_data)
        res_data.update({"code": RESP_CODE_SUCCESS, "result": files_info})
        return JsonResponse(res_data)


class FileList(View):
    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR, "error": ""}
        share_uk = request.POST.get("share_uk")
        shareid = request.POST.get("shareid")
        # bdstoken = request.POST.get("bdstoken")
        dir_ = request.POST.get("dir")
        if not all((share_uk, shareid, dir_)):
            res_data.update({"error": "缺少参数"})
            return JsonResponse(res_data)
        if not all((str(share_uk).isdigit(), str(shareid).isdigit())):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        is_ok, data = get_cookie_from_db(vip_type=2)
        params_dict = {
            "uk": share_uk, "shareid": shareid, "dir": dir_, "bdstoken": data.get("bdstoken"), "order": "other",
            "desc": 1, "web": 1, "page": 1, "num": 100, "channel": "chunlei", "app_id": 250528, "clienttype": 0
        }
        if not is_ok:
            res_data.update({"error": data})
            return JsonResponse(res_data)
        headers = get_bd_headers()
        headers.update({"Cookie": data.get("cookie")})
        url = f"https://pan.baidu.com/share/list?{urlencode(params_dict)}"
        # print("url:", url)
        try:
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                res_data.update({"error": f"获取mset响应码为{res.status_code}"})
                return JsonResponse(res_data)
        except Exception as e:
            logger.error(f"FileList POST: request url({url}) meet error: {e}")
            res_data.update({"error": "请求文件信息出错"})
            return JsonResponse(res_data)
        res_json = res.json()
        if res_json.get("errno") != 0:
            res_data.update({"error": f"请求文件信息失败({res_json.get('errmsg')})"})
            return JsonResponse(res_data)
        res_data.update({"code": RESP_CODE_SUCCESS, "result": res_json.get("list")})
        return JsonResponse(res_data)


class WxFileList(View):
    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR, "error": ""}
        share_url = request.POST.get("share_url")
        pwd = request.POST.get("pwd")
        file_path = request.POST.get("file_path")
        share_url = str(share_url).strip() if share_url else ""
        pwd = str(pwd).strip() if pwd else ""
        file_path = str(file_path).strip() if file_path else ""
        if not all([share_url, pwd]):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        if not share_url.startswith("https://pan.baidu.com/s/"):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        s_url = share_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        url = share_url.split("?")[0] + f"?pwd={pwd}"
        if not s_url or s_url not in url:
            res_data.update({"error": "提取surl失败"})
            return JsonResponse(res_data)
        is_ok, cookie_data = get_cookie_from_db(vip_type=0)
        if not is_ok:
            res_data.update({"error": cookie_data})
            return JsonResponse(res_data)
        is_ok, file_data = get_wx_list(cookie_data.get("cookie"), s_url, pwd, file_path)
        if not is_ok:
            res_data.update({"error": file_data})
            return JsonResponse(res_data)
        res_data.update({"code": RESP_CODE_SUCCESS, "result": file_data})
        return JsonResponse(res_data)


class DownloadLink(View):
    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR, "error": ""}
        share_url = request.POST.get("share_url")
        fs_id = request.POST.get("fs_id")
        share_uk = request.POST.get("share_uk")
        shareid = request.POST.get("shareid")
        seckey = request.POST.get("seckey")
        sign = request.POST.get("sign")
        sign_timestamp = request.POST.get("sign_timestamp")
        if not all([share_url, fs_id, share_uk, shareid, seckey]):
            res_data.update({"error": "缺少参数"})
            return JsonResponse(res_data)
        if not all([str(fs_id).isdigit(), str(share_uk).isdigit(), str(shareid).isdigit()]):
            res_data.update({"error": "参数错误"})
            return JsonResponse(res_data)
        share_url = str(share_url).strip() if share_url else ""
        surl = share_url.split("?")[0].rsplit("/", maxsplit=1)[-1]
        if not surl:
            res_data.update({"error": "缺少参数"})
            return JsonResponse(res_data)
        redis_conn = get_redis_connection("download_link")
        fs_info = redis_conn.get(f"download_link:{fs_id}")
        if fs_info:
            try:
                res_data.update({"code": RESP_CODE_SUCCESS, "result": json.loads(fs_info)})
                return JsonResponse(res_data)
            except Exception as e:
                logger.error(f"DownloadLink post() get fs info from redis failed,  fs_info: {fs_info}, error: {e}")
        is_ok, cookie = get_cookie_from_db(vip_type=2)
        if not is_ok:
            res_data.update({"error": cookie})
            return JsonResponse(res_data)
        if not sign or not sign_timestamp or not str(sign_timestamp).isdigit():
            is_ok, sign_time = get_sign(cookie.get("cookie"), surl)
        elif time() - int(sign_timestamp) > 290:
            is_ok, sign_time = get_sign(cookie.get("cookie"), None, shareid, share_uk)
        else:
            is_ok = True
            sign_time = (sign, int(sign_timestamp))
        if not is_ok:
            res_data.update({"error": sign_time})
            return JsonResponse(res_data)
        seckey = unquote_plus(quote_plus(str(seckey).replace("-", "+").replace("~", "=").replace("_", "/")))
        # seckey = 'Jonb2MEu3UXgKJD5O+TPFVzKcu2/PkCMa2h5aCOHFnA='
        is_ok, d_link_dict = get_d_link(
            cookie.get("cookie"), sign_time[0], sign_time[1], seckey, int(fs_id), share_uk, int(shareid)
        )
        if not is_ok:
            res_data.update({"error": d_link_dict})
            return JsonResponse(res_data)
        is_ok, real_link = get_real_link(cookie.get("cookie"), d_link_dict.get("dlink"))
        if not is_ok:
            res_data.update({"error": real_link})
            return JsonResponse(res_data)
        download_info = {
            "real_link": real_link,
            "user_agent": "LogStatistic",
            "md5": d_link_dict.get("md5"),
            "category": d_link_dict.get("category"),
            "filename": d_link_dict.get("server_filename"),
            "size": d_link_dict.get("size"),
            "sign": sign_time[0],
            "sign_timestamp": sign_time[1],
            "resolve_time": int(time()),
        }
        redis_conn.setex(f"download_link:{fs_id}", DL_INFO_EX_TIME, json.dumps(download_info))
        res_data.update({"code": RESP_CODE_SUCCESS, "result": download_info})
        return JsonResponse(res_data)


def get_sign(cookie, surl=None, share_id=None, uk=None):
    params = ""
    if surl:
        params += f"surl={surl}&"
    if share_id:
        params += f"shareid={share_id}&"
    if uk:
        params += f"uk={uk}&"
    url = f"https://pan.baidu.com/share/tplconfig?{params}fields=sign,timestamp&channel=chunlei&web=1&app_id=250528&clienttype=0"
    headers = {
        "User-Agent": "netdisk;pan.baidu.com",
        "Cookie": cookie,
    }
    try:
        res = requests.get(url, headers=headers).json()
    except Exception as e:
        logger.error(f"DownloadLink POST get_sign() request failed: {e}")
        return False, "获取签名和时间戳错误"
    if res["errno"] != 0:
        logger.warning(f"DownloadLink POST get_sign() is not ok, res.json: {res}")
        return False, "获取签名和时间戳失败"
    sign = res["data"]["sign"]
    timestamp = res["data"]["timestamp"]
    return True, (sign, timestamp)


def get_d_link(cookie, sign, timestamp, randsk, fs_id, uk, shareid):
    url = f'https://pan.baidu.com/api/sharedownload?app_id=250528&channel=chunlei&clienttype=12&sign={sign}&timestamp={timestamp}&web=1'
    headers = get_bd_headers()
    headers.update({"Cookie": unquote(cookie), "Referer": "https://pan.baidu.com/disk/home"})
    sekey_str = quote_plus('{"sekey":"%s"}' % randsk)
    data_str = f"encrypt=0&extra={sekey_str}&fid_list=[{fs_id}]&primaryid={shareid}&uk={uk}&product=share&type=nolimit"
    try:
        res = requests.post(url, data=data_str, headers=headers).json()
    except Exception as e:
        logger.error(f"DownloadLink POST get_d_link() request failed: {e}")
        return False, "请求dlink错误"
    if res["errno"] != 0:
        logger.warning(f"DownloadLink POST get_d_link() is not ok, res.json: {res}")
        return False, "请求dlink链接失败"
    if res.get("errno") != 0 or not res.get("list"):
        logger.warning(f'DownloadLink POST get_d_link() is not ok, errno != 0 or not res.get("list"),res.json: {res}')
        return False, "请求dlink链接失败"
    return True, res["list"][0]


def get_real_link(cookie, d_link):
    headers = {"User-Agent": "LogStatistic", "Cookie": cookie}
    try:
        res = requests.head(d_link, headers=headers, allow_redirects=False)
    except Exception as e:
        logger.error(f"DownloadLink POST get_real_link() request failed: {e}")
        return False, "请求真实下载链接错误"
    if not res.headers.get("Location"):
        return False, "获取真实链接失败（重定向）"
    return True, res.headers["Location"]


def get_wx_list(cookie, surl, pwd, path=""):
    url = "https://pan.baidu.com/share/wxlist?channel=weixin&version=2.2.2&clienttype=25&web=1"
    headers = {"User-Agent": "netdisk", "Cookie": cookie, "Referer": "https://pan.baidu.com/disk/home"}
    data = {
        "shorturl": surl, "dir": path, "root": "0" if path else "1", "pwd": pwd, "page": 1, "num": 1000, "order": "time"
    }
    try:
        res = requests.post(url, headers=headers, data=urlencode(data)).json()
    except Exception as e:
        logger.error(f"WxFileList POST get_wx_list() request failed: {e}")
        return False, "请求文件列表错误"
    if res.get("errtype") != 0:
        logger.warning(f"WxFileList POST get_wx_list() is not ok, res.json: {res}")
        return False, WX_LIST_ERROR_TYPE.get(res.get("errtype"), "遇到未知错误")
    if res["errno"] != 0:
        logger.warning(f"WxFileList POST get_wx_list() is not ok, res.json: {res}")
        return False, "请求文件列表失败"
    if not res.get('data'):
        logger.warning(f"WxFileList POST get_wx_list() returned data is empty, res.json: {res}")
        return False, "文件列表为空"
    return True, res["data"]

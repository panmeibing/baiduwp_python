from django.contrib import auth
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .models import User
from baiduwp_python.settings.config import RESP_CODE_ERROR, RESP_CODE_SUCCESS
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.valid_password_utils import check_pwd


class LoginView(View):
    def get(self, request):
        return render(request, 'baiduwp_frontend/login.html')

    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR}
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if not user:
            res_data.update({"error": "账号或密码错误"})
            return JsonResponse(res_data)
        auth.login(request, user)
        res_data.update({"code": RESP_CODE_SUCCESS, "result": "登录成功"})
        response = JsonResponse(res_data)
        response.set_cookie("is_login", 1, max_age=3600 * 24 * 7)
        return response


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        response = HttpResponseRedirect(reverse('user:login'))
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response

    def post(self, request):
        auth.logout(request)
        response = HttpResponseRedirect(reverse('user:login'))
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response


class RegisterView(View):
    def post(self, request):
        res_data = {"code": RESP_CODE_ERROR, "error": ""}
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_again = request.POST.get("password2")

        if not all([username, password, password_again]):
            res_data.update({"error": "缺少参数"})
            return JsonResponse(res_data)
        try:
            current_user = request.user
            if not current_user or not current_user.is_superuser:
                res_data.update({"error": "无操作权限"})
                return JsonResponse(res_data)
            same_user = User.objects.filter(username=username)
            if same_user:
                res_data.update({"error": "该用户名已被注册"})
                return JsonResponse(res_data)
            if current_user.role_id != 100:
                is_ok, error = check_pwd(password)
                if not is_ok:
                    res_data.update({"error": error})
                    return JsonResponse(res_data)
            user = User.objects.create_user(username=username, password=password)
            res_data.update({"code": RESP_CODE_SUCCESS, "result": "注册成功"})
            return JsonResponse(res_data)
        except Exception as e:
            logger.error("register fail:{}".format(e))
            res_data.update({"error": "注册失败"})
            return JsonResponse(res_data)

"""定时同步任务"""
is_run_sync_job = False  # 是否开启定时同步任务

"""邀请码验证"""
is_need_invitation_code = True  # 是否需要邀请码
invitation_code_fixed = None  # 邀请码，若为None则随机生成
invitation_code_exp_time = 60 * 60 * 24  # 邀请码超时时间（秒）
# 需要验证邀请码的路径
throttle_path_list = [
    "/mSetInfo/", "/fileList/", "/downloadLink/",
]

"""后台登录路由"""
admin_path = "admin/"

"""登录控制"""
# 登录验证白名单
login_path_white_list = [
    "/login/", "/resolver/", "/admin/",
    "/mSetInfo/", "/fileList/", "/downloadLink/"
]
# 登录验证黑名单
login_path_black_list = []
# 登录验证IP地址黑名单
login_ip_black_list = []

"""chrome驱动"""
# chrome驱动路径
selenium_executable_path = r"E:\webdriver\chromedriver.exe"

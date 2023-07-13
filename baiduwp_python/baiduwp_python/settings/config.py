"""定时同步任务"""
IS_RUN_SYNC_JOB = False  # 是否开启定时同步任务

"""邀请码验证"""
IS_NEED_INVITATION_CODE = True  # 是否需要邀请码
INVITATION_CODE_FIXED = None  # 邀请码，若为None则随机生成
INVITATION_CODE_EXP_TIME = 86400  # 邀请码超时时间（秒）
# 需要验证邀请码的路径
THROTTLE_PATH_LIST = [
    "/mSetInfo/", "/fileList/", "/downloadLink/",
]

"""后台登录路由"""
URL_PATH_ADMIN = "admin/"

"""登录控制"""
# 登录验证白名单
LOGIN_PATH_WHITE_LIST = [
    "/login/", "/resolver/", "/admin/",
    "/mSetInfo/", "/fileList/", "/downloadLink/", "/wxFileList/"
]
# 登录验证黑名单
LOGIN_PATH_BLACK_LIST = []
# 登录验证IP地址黑名单
LOGIN_IP_BLACK_LIST = []

"""chrome驱动"""
# chrome驱动路径
SELENIUM_EXECUTABLE_PATH = r"E:\webdriver\chromedriver.exe"

"""限制解析次数"""
PARSE_COUNT_LIMIT = 10  # 限制每个IP的解析次数
PARSE_COUNT_EX_TIME = 86400  # 解除限制时间（秒）

"""下载链接缓存"""
DL_INFO_EX_TIME = 25200  # 下载链接信息过期时间（秒）

"""响应码"""
RESP_CODE_ERROR = 0
RESP_CODE_SUCCESS = 1
RESP_CODE_INVITATION = 2
RESP_CODE_PARSE_LIMIT = 3

"""wxList常见错误信息"""
WX_LIST_ERROR_TYPE = {
    "mispw_9": "提取码错误",
    "mispwd-9": "提取码错误",
    "mis_105": "所解析的链接不存在",
    "mis_2": "文件目录不存在",
    "mis_4": "文件目录不存在",
}

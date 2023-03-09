from account.models import AccountCookie
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.date_utils import get_datetime_now_str


def get_account_cookie(username, vip_type, is_valid, order_by='-update_time'):
    match_dict = {"is_active": True}
    if username:
        match_dict.update({"username__contains": username})
    if vip_type:
        match_dict.update({"vip_type": vip_type})
    if is_valid:
        match_dict.update({"is_valid": is_valid})
    try:
        account_cookie_list = list(AccountCookie.objects.filter(**match_dict).order_by(order_by).values().all())
        return True, account_cookie_list
    except Exception as e:
        logger.error(f"get_account_cookie() meet error: {e}")
        return False, "操作数据库出错"


def add_account_cookie(baidu_name, net_disk_name, uk, vip_type, bdclnd, cookie):
    try:
        count = AccountCookie.objects.filter(uk=uk, is_active=True).count()
        if count:
            return False, "请勿重复添加"
        date_time_now = get_datetime_now_str()
        AccountCookie.objects.create(
            baidu_name=baidu_name, net_disk_name=net_disk_name, uk=uk, vip_type=vip_type, is_valid=True, bdclnd=bdclnd,
            cookie=cookie, create_time=date_time_now, update_time=date_time_now,
            is_active=True
        )
        return True, "新增成功"
    except Exception as e:
        logger.error(f"add_account_cookie() meet error: {e}")
        return False, "操作数据库出错"


def del_account_cookie(ids: list):
    try:
        count = AccountCookie.objects.filter(is_active=True, id__in=ids).update(is_active=False)
        return True, count
    except Exception as e:
        logger.error(f"del_account_cookie() meet error: {e}")
        return False, "操作数据库出错"

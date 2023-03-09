from random import choice

from account.models import AccountCookie

from baiduwp_python.settings.settings import logger


def get_cookie_from_db(vip_type=None):
    match_dict = {"is_active": True, "is_valid": True}
    if vip_type is not None and str(vip_type).isdigit():
        match_dict.update({"vip_type": vip_type})
    try:
        cookie_ids = AccountCookie.objects.filter(**match_dict).values_list("id")
        cookie_id_list = [c[0] for c in cookie_ids if c]
        if not cookie_id_list:
            return False, "未查询到可用cookie"
        cookie_list = list(AccountCookie.objects.filter(id=choice(cookie_id_list)).values("bdstoken", "cookie"))
        # print("cookie_list:", cookie_list)
        cookie_dict = cookie_list[0]
        return True, cookie_dict
    except Exception as e:
        logger.error(f"get_cookie_from_db() meet error: {e}")
        return False, "查询cookie失败"

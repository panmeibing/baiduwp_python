import time
from random import randint
from threading import Thread

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from account.models import AccountCookie
from baiduwp_python.settings.settings import logger
from baiduwp_python.utils.header_utils import get_bd_headers


def valid_account_info(data_dict: dict):
    time.sleep(randint(1, 60))
    try:
        url = "https://pan.baidu.com/rest/2.0/xpan/nas?access_token=&method=uinfo"
        headers = get_bd_headers()
        headers.update({"Cookie": data_dict["cookie"]})
        res_json = requests.get(url, headers=headers).json()
        update_filed_dict = dict()
        if res_json["errno"] == 0:
            if res_json.get("baidu_name") != data_dict["baidu_name"]:
                update_filed_dict["baidu_name"] = res_json.get("baidu_name")
            if res_json.get("netdisk_name") != data_dict["net_disk_name"]:
                update_filed_dict["net_disk_name"] = res_json.get("netdisk_name")
            if res_json.get("uk") != data_dict["uk"]:
                update_filed_dict["uk"] = res_json.get("uk")
            if res_json.get("vip_type") != data_dict["vip_type"]:
                update_filed_dict["vip_type"] = res_json.get("vip_type")
        else:
            update_filed_dict["is_valid"] = False
        if update_filed_dict:
            AccountCookie.objects.filter(id=data_dict["id"]).update(**update_filed_dict)
            logger.info(f"valid_account_info() update AccountCookie({data_dict['id']}) success: {update_filed_dict}")
    except Exception as e:
        logger.error(f"get account info by cookie meet error: {e}")


def valid_cookie():
    ac_list = list(AccountCookie.objects.filter(is_active=True).values(
        "id", "baidu_name", "net_disk_name", "uk", "vip_type", "is_valid", "cookie",
    ))
    if not ac_list:
        return
    thread_list = list()
    for ac in ac_list:
        if not all((ac.get("id"), ac.get("uk"), ac.get("cookie"))):
            logger.warning(f"valid_cookie() miss params: id:{ac.get('id')},uk({ac.get('uk')})")
            return
        thread = Thread(target=valid_account_info, args=(ac,))
        thread_list.append(thread)
        thread.start()
    for t in thread_list:
        t.join()


def run_job_valid_cookie():
    logger.info("start to apscheduler job valid_cookie()")
    scheduler = BackgroundScheduler()
    try:
        scheduler.add_job(
            valid_cookie, trigger=CronTrigger(minute="*/10"), misfire_grace_time=300,
            id="run_job_valid_cookie", replace_existing=True,
        )
        scheduler.start()
    except Exception as e:
        logger.error(f"run apscheduler job valid_cookie() failed: {e}")
        scheduler.shutdown()

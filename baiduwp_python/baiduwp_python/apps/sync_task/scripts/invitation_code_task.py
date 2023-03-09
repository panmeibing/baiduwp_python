from random import randint

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_redis import get_redis_connection

from baiduwp_python.settings.config import invitation_code_exp_time, is_need_invitation_code, invitation_code_fixed
from baiduwp_python.settings.settings import logger


def monitor_invitation_code():
    try:
        logger.info("start to run monitor_invitation_code()")
        if not is_need_invitation_code:
            return
        redis_conn = get_redis_connection("default")
        invitation_code = redis_conn.get("bdwp:invitation_code")
        if not invitation_code:
            invitation_code = randint(10, 99999) if invitation_code_fixed is None else invitation_code_fixed
            redis_conn.setex("bdwp:invitation_code", invitation_code_exp_time, invitation_code)
            logger.info(f"set redis success, invitation_code: {invitation_code}")
        # print(f"monitor_invitation_code() invitation_code: {invitation_code}")
    except Exception as e:
        logger.error(f"run monitor_invitation_code() meet error: {e}")


def run_job_invitation_code():
    logger.info("start to apscheduler job monitor_invitation_code()")
    monitor_invitation_code()
    scheduler = BackgroundScheduler()
    try:
        scheduler.add_job(
            monitor_invitation_code, trigger=CronTrigger(second="*/15"), misfire_grace_time=300,
            id="monitor_invitation_code", replace_existing=True,
        )
        scheduler.start()
    except Exception as e:
        logger.error(f"run apscheduler job monitor_invitation_code() failed: {e}")
        scheduler.shutdown()

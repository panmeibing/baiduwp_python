from random import randint

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_redis import get_redis_connection

from baiduwp_python.settings.config import INVITATION_CODE_EXP_TIME, IS_NEED_INVITATION_CODE, INVITATION_CODE_FIXED
from baiduwp_python.settings.settings import logger


def monitor_invitation_code():
    try:
        logger.info("start to run monitor_invitation_code()")
        if not IS_NEED_INVITATION_CODE:
            return
        redis_conn = get_redis_connection("default")
        invitation_code = redis_conn.get("bdwp:invitation_code")
        if not invitation_code:
            invitation_code = randint(10, 99999) if INVITATION_CODE_FIXED is None else INVITATION_CODE_FIXED
            redis_conn.setex("bdwp:invitation_code", INVITATION_CODE_EXP_TIME, invitation_code)
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

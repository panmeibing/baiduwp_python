from baiduwp_python.settings.config import IS_RUN_SYNC_JOB
from .scripts.invitation_code_task import run_job_invitation_code
from .scripts.valid_cookie_task import run_job_valid_cookie

urlpatterns = []

if IS_RUN_SYNC_JOB:
    run_job_invitation_code(),
    run_job_valid_cookie(),

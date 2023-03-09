from baiduwp_python.settings.config import is_run_sync_job
from .scripts.invitation_code_task import run_job_invitation_code
from .scripts.valid_cookie_task import run_job_valid_cookie

urlpatterns = []

if is_run_sync_job:
    run_job_invitation_code(),
    run_job_valid_cookie(),

from celery import shared_task
from .services.profiles import profile_count_update


@shared_task
def profile_count_update():
    profile_count_update()

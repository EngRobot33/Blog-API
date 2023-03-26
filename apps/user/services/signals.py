from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import User
import os
import shutil


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        os.mkdir(f"static/user/{instance.username}")
        print(f"{instance.username} directory has been made successfully!")


@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    shutil.rmtree(f"static/user/{instance.username}")
    print(f"{instance.username} directory has been deleted successfully!")

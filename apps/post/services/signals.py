from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Post
import os
import shutil


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        os.mkdir(f"static/post/{instance.title}")
        print(f"{instance.title} directory made by {instance.author.username}")


@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    shutil.rmtree(f"static/post/{instance.title}")
    print(f"{instance.title} directory has been deleted successfully!")

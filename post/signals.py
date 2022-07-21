from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Post
import os
import shutil


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        os.mkdir(f"static/user/{instance.username}")
        print(f"{instance.username} folder has been created successfully!")

@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    shutil.rmtree(f"static/user/{instance.username}")
    print(f"{instance.username} folder has been deleted successfully!")

@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        os.mkdir(f"static/post/{instance.title}")
        print(f"{instance.title} created by {instance.author}")

@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    shutil.rmtree(f"static/post/{instance.title}")
    print(f"{instance.title} folder has been deleted successfully!")

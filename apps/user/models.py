from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, is_active=True, is_admin=False, password=None):
        if not username:
            raise ValueError("You must set a username for yourself!")

        user = self.model(username=username, is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, is_active=True, is_admin=True, password=password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        indexes = [models.Index(fields=['username', 'is_active', 'is_admin', 'created_at', 'updated_at', ])]

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    followings_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profiles'
        indexes = [models.Index(fields=['user', 'posts_count', 'followers_count', 'followings_count', ])]

    def __str__(self):
        return f"{self.user}"

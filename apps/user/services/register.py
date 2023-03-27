from django.db import transaction

from ..models import User, Profile


def create_profile(*, user: User) -> Profile:
    return Profile.objects.create(user=user)


def create_user(*, username: str, password: str) -> User:
    return User.objects.create_user(username=username, password=password)


@transaction.atomic
def register(*, username: str, password: str) -> User:
    user = create_user(username=username, password=password)
    create_profile(user=user)
    return user

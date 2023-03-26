from ..models import Relation
from apps.user.models import User


def follow(*, user: User, username: str) -> Relation:
    following = User.objects.get(username=username)
    follower = Relation(follower=user, following=following)
    follower.full_clean()
    follower.save()
    return follower


def unfollow(*, user: User, username: str) -> None:
    following = User.objects.get(username=username)
    Relation.objects.get(follower=user, following=following).delete()


def count_follower(*, user: User) -> int:
    return Relation.objects.filter(follwing=user).count()


def count_following(*, user: User) -> int:
    return Relation.objects.filter(follwer=user).count()

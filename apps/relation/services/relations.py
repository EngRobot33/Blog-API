from ..models import Relation
from apps.user.models import User
from apps.user.services.profiles import cache_profile


def follow(*, user: User, username: str) -> Relation:
    following = User.objects.get(username=username)
    follower = Relation(follower=user, following=following)
    follower.full_clean()
    follower.save()
    cache_profile(user=user)

    return follower


def unfollow(*, user: User, username: str) -> None:
    following = User.objects.get(username=username)
    Relation.objects.get(follower=user, following=following).delete()
    cache_profile(user=user)


def count_follower(*, user: User) -> int:
    return Relation.objects.filter(follwing=user).count()


def count_following(*, user: User) -> int:
    return Relation.objects.filter(follwer=user).count()

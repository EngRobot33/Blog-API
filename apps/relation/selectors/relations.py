from django.db.models import QuerySet

from ..models import Relation
from apps.user.models import User


def get_followers(*, user: User) -> QuerySet[Relation]:
    return Relation.objects.filter(follower=user)

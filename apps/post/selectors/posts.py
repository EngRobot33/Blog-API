from django.db.models import QuerySet

from ..filters import PostFilter
from ..models import Post
from apps.relation.models import Relation
from apps.user.models import User


def post_list(*, filters=None, user: User, self_include: bool = True) -> QuerySet[Post]:
    filters = filters or {}
    relations = list(Relation.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        relations.append(user.id)
    if relations:
        queryset = Post.objects.filter(author__in=relations)
        return PostFilter(filters, queryset).qs
    return Post.objects.none()


def post_detail(*, slug: str, user: User, self_include: bool = True) -> QuerySet[Post]:
    relations = list(Relation.objects.filter(follower=user).values_list("following", flat=True))
    if self_include:
        relations.append(user.id)

    return Post.objects.get(slug=slug, author__in=relations)

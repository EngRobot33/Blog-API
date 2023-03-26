from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify

from ..models import Post
from apps.user.models import User


@transaction.atomic()
def create_post(*, user: User, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
    return post


def count_posts(*, user: User) -> int:
    return Post.objects.filter(author=user).count()

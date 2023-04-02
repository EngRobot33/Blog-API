from django.core.cache import cache

from ..models import User


def cache_profile(*, user: User) -> None:

    from apps.relation.services.relations import count_follower, count_following
    from apps.post.services.posts import count_posts

    profile = {
        'posts_count': count_posts(user=user),
        'followers_count': count_follower(user=user),
        'followings_count': count_following(user=user),
    }
    cache.set(f'profile_{user}', profile, timeout=None)

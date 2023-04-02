from django.core.cache import cache

from ..models import User, Profile


def cache_profile(*, user: User) -> None:

    from apps.relation.services.relations import count_follower, count_following
    from apps.post.services.posts import count_posts

    profile = {
        'posts_count': count_posts(user=user),
        'followers_count': count_follower(user=user),
        'followings_count': count_following(user=user),
    }
    cache.set(f'profile_{user}', profile, timeout=None)


def profile_count_update():
    profiles = cache.keys("profile_*")

    for profile_key in profiles:
        username = profile_key.replace("profile_", "")
        data = cache.get(profile_key)

        try:
            profile = Profile.objects.get(user__username=username)
            profile.posts_count = data.get("posts_count")
            profile.followers_count = data.get("followers_count")
            profile.followings_count = data.get("followings_count")
            profile.save()

        except Exception as ex:
            print(ex)

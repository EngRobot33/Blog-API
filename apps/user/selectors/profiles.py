from ..models import Profile, User


def get_profile(user: User) -> Profile:
    return Profile.objects.get(user=user)

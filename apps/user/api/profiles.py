from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from ..models import Profile
from ..selectors.profiles import get_profile
from apps.api.mixins import ApiAuthMixin


class ProfileApi(ApiAuthMixin, APIView):
    class ProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('posts_count', 'followers_count', 'followings_count')

    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request):
        profile = get_profile(user=request.user)
        return Response(self.ProfileOutputSerializer(profile).data, status=status.HTTP_200_OK)

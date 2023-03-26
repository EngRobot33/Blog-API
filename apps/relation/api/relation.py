from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from ..models import Relation
from ..selectors.relations import get_followers
from ..services.relations import follow, unfollow
from apps.api.paginations import get_paginated_response, LimitOffsetPagination
from apps.api.mixins import ApiAuthMixin


class FollowApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FollowInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=127)

    class FollowOutputSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField("get_username")

        class Meta:
            model = Relation
            fields = ("username", )

        def get_username(self, relation):
            return relation.following.username

    @extend_schema(request=FollowInputSerializer, responses=FollowOutputSerializer)
    def post(self, request):
        serializer = self.FollowInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            relation = follow(user=request.user, username=serializer.validated_data.get("username"))
        except Exception as ex:
            return Response(f'Database Error: {ex}', status=status.HTTP_400_BAD_REQUEST)

        return Response(self.FollowOutputSerializer(relation).data)

    @extend_schema(responses=FollowOutputSerializer)
    def get(self, request):
        user = request.user
        followers = get_followers(user=user)
        return get_paginated_response(
                request=request,
                pagination_class=self.Pagination,
                queryset=followers,
                serializer_class=self.FollowOutputSerializer,
                view=self,
                )


class FollowDetailApi(ApiAuthMixin, APIView):
    def delete(self, request, username):
        try:
            unfollow(user=request.user, username=username)
        except Exception as ex:
            return Response(f'Database Error: {ex}', status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

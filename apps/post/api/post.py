from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Post
from ..services.posts import create_post
from ..selectors.posts import post_list, post_detail
from apps.api.mixins import ApiAuthMixin
from apps.api.paginations import LimitOffsetPagination, get_paginated_response_context


class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        author__in = serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)
        content = serializers.CharField(required=False, max_length=1000)

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=127)
        content = serializers.CharField(max_length=1000)

    class PostOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField('get_author')

        class Meta:
            model = Post
            fields = ('author', 'slug', 'title', 'content')

        def get_author(self, post):
            return post.author.username

    @extend_schema(request=PostInputSerializer, responses=PostOutputSerializer)
    def post(self, request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            post = create_post(
                user=request.user,
                title=serializer.validated_data.get('title'),
                content=serializer.validated_data.get('content')
            )
        except Exception as ex:
            return Response(f'Database Error: {ex}', status=status.HTTP_400_BAD_REQUEST)

        return Response(self.PostOutputSerializer(data=post).data, status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[FilterSerializer], responses=PostOutputSerializer,)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            post = post_list(filters=filters_serializer.validated_data, user=request.user)
        except Exception as ex:
            return Response(f'Filter Error: {ex}',  status=status.HTTP_400_BAD_REQUEST)

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.PostOutputSerializer,
            queryset=post,
            request=request,
            view=self,
        )


class PostDetailApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class PostDetailOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.email

    @extend_schema(responses=PostDetailOutputSerializer,)
    def get(self, request, slug):
        try:
            post = post_detail(slug=slug, user=request.user)
        except Exception as ex:
            return Response(f'Filter Error: {ex}',  status=status.HTTP_400_BAD_REQUEST)

        return Response(self.PostDetailOutputSerializer(data=post).data)

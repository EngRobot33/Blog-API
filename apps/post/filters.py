from django_filters import CharFilter, FilterSet
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from .models import Post
from rest_framework.exceptions import APIException


class PostFilter(FilterSet):
    search = CharFilter(method="filter_search")
    author__in = CharFilter(method="filter_author__in")
    created_at__range = CharFilter(method="filter_created_at__range")

    def filter_author__in(self, queryset, name, value):
        limit = 10
        authors = value.split(",")
        if len(authors) > limit:
            raise APIException(f"You cannot add more than {len(authors)} authors!")
        return queryset.filter(author__username__in=authors)

    def filter_created_at__range(self, queryset, name, value):
        limit = 2
        created_at__in = value.split(",")
        if len(created_at__in) > limit:
            raise APIException("Please just add two created_at with , in the middle.")

        first_created_at, second_created_at = created_at__in

        if not second_created_at:
            second_created_at = timezone.now()

        if not first_created_at:
            return queryset.filter(created_at__date__lt=second_created_at)

        return queryset.filter(created_at__date__range=(first_created_at, second_created_at))

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("title")).filter(search=value)

    class Meta:
        model = Post
        fields = ('slug', 'title', )

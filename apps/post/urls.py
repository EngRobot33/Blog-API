from django.urls import path

from .api.post import PostApi, PostDetailApi

app_name = 'post'
urlpatterns = [
    path('post/', PostApi.as_view(), name='post-list'),
    path('post/<slug:slug>/', PostDetailApi.as_view(), name='post-detail'),
]

from django.urls import path

from .api.relation import FollowApi, FollowDetailApi

app_name = 'relation'
urlpatterns = [
    path('follow/', FollowApi.as_view(), name='follow-list'),
    path('follow/<slug:slug>/', FollowDetailApi.as_view(), name='follow-detail'),
]
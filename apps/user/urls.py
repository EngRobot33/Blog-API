from django.urls import path

from .api.register import RegisterApi
from .api.profiles import ProfileApi


app_name = 'user'
urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('profile/', ProfileApi.as_view(), name="profile"),
]

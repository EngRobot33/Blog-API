from django.urls import path

from .api.register import RegisterApi


app_name = 'user'
urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
]

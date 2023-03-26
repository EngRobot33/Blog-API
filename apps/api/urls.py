from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('post/', include('apps.post.urls')),
    path('relation/', include('apps.relation.urls')),
    path('user/', include('apps.user.urls')),
]

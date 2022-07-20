from rest_framework import routers
from .views import *


router = routers.SimpleRouter()

router.register('post', PostViewSet, basename='post')
router.register('user', UserViewSet, basename='user')

urlpatterns = router.urls

from django.conf.urls import include
from django.urls import path
from finalcapstoneapi.views import Resolutions, Categories, Tags, Comments
from rest_framework import routers



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'resolutions', Resolutions, 'resolution')
router.register(r'categories', Categories, 'category')
router.register(r'tags', Tags, 'tag')
router.register(r'comments', Comments, 'comment')

urlpatterns = [
    path('', include(router.urls)),
]

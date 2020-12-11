from django.conf.urls import include
from django.urls import path
from finalcapstoneapi.views import Resolutions
from rest_framework import routers



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'resolutions', Resolutions, 'resolution')


urlpatterns = [
    path('', include(router.urls)),
]

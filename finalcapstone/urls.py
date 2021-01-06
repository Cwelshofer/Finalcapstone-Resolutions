from django.conf.urls import include
from django.urls import path
from finalcapstoneapi.views import Resolutions, Categories, Tags, Comments, CurrentUser, ResolutionUsers, ResolutionTags, Subscriptions
from rest_framework import routers
from finalcapstoneapi.views import register_user, login_user


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'resolutions', Resolutions, 'resolution')
router.register(r'categories', Categories, 'category')
router.register(r'tags', Tags, 'tag')
router.register(r'comments', Comments, 'comment')
router.register(r'currentuser', CurrentUser, 'resolutionuser')
router.register(r'users', ResolutionUsers, 'resolutionuser')
router.register(r'resolutiontags', ResolutionTags, 'resolutiontag')
router.register(r'subscriptions', Subscriptions, 'subscription')
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

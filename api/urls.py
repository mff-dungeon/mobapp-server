from django.conf.urls import url, include
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bundles', BundleViewSet)
router.register(r'contacts', ContactViewSet, base_name='contact')
router.register(r'groups', GroupViewSet, base_name='group')
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
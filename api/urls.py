from django.conf.urls import url, include
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register(r'bundles', BundleViewSet)
router.register(r'contacts', ContactViewSet, base_name='contact')
router.register(r'groups', GroupViewSet, base_name='group')
router.register(r'tickets', TicketViewSet)
router.register(r'clone', TicketCloneHandler, base_name='clone')

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', TokenView.as_view()),
    url(r'^', include(router.urls)),
]
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, mixins

from api import serializers
from contacts.models import Bundle, Ticket


class FilterOwnedTickets(object):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if not request.user.is_authenticated:
            return Ticket.objects.none()
        return queryset.filter(owner=request.user)


class FilterKnownBundles(object):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if not request.user.is_authenticated:
            return Bundle.objects.none()
        return queryset.filter(Q(tickets__owner=request.user) | Q(owner=request.user))


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer


class BundleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bundle.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.BundleSerializer
    filter_backends = (FilterKnownBundles,)


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bundle.objects.filter(is_contact=True)
    lookup_field = 'id'
    serializer_class = serializers.ContactSerializer
    filter_backends = (FilterKnownBundles,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bundle.objects.filter(is_contact=False)
    lookup_field = 'id'
    serializer_class = serializers.GroupSerializer
    filter_backends = (FilterKnownBundles,)


class TicketViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.TicketSerializer
    filter_backends = (FilterOwnedTickets,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

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
        return queryset.filter(Q(in_bundles__tickets__owner=request.user) | Q(tickets__owner=request.user) | Q(owner=request.user)).distinct()


class FilterKnownContactInfos(object):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if not request.user.is_authenticated:
            return ContactInfoViewSet.objects.none()
        return queryset.filter(Q(bundle__tickets__owner=request.user) | Q(bundle__owner=request.user)).distinct()


class BundleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bundle.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.BundleSerializer
    filter_backends = (FilterKnownBundles,)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.filter(is_contact=True)
    lookup_field = 'id'
    serializer_class = serializers.ContactSerializer
    filter_backends = (FilterKnownBundles,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_contact=True)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.filter(is_contact=False)
    lookup_field = 'id'
    serializer_class = serializers.GroupSerializer
    filter_backends = (FilterKnownBundles,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_contact=True)


class TicketCloneHandler(viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.TicketSerializer

    """
    Clone a ticket.
    """
    def update(self, request, *args, **kwargs):
        ticket_id = kwargs['id']
        instance = Ticket.objects.get(id=ticket_id)

        if instance.owner == self.request.user:
            # pretend that user-owned tickets do not exist for this endpoint
            raise NotFound()

        if not instance.can_share:
            # it is forbidden to share this ticket
            raise PermissionDenied()

        cloned_tickets = Ticket.objects.filter(owner=self.request.user, cloned_from=instance)
        if cloned_tickets.count() == 0:
            # create clone of the ticket
            clone = Ticket()
            clone.clone_other(instance)
            clone.owner = self.request.user
            clone.save()
        else:
            # here we assume that the count is 0 or 1
            clone = cloned_tickets.get()

        serializer = serializers.TicketSerializer(clone)
        return Response(serializer.data)


class TicketViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.TicketSerializer
    filter_backends = (FilterOwnedTickets,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactInfoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.ContactInfoSerializer
    filter_backends = (FilterKnownContactInfos,)

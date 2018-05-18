from django.contrib.auth.models import User
from rest_framework.serializers import *

from contacts import models


class UserSerializer(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = ('username', 'detail')


class UserDetailSerializer(ModelSerializer):
    tickets = HyperlinkedRelatedField(many=True, read_only=True, source='contactuser.tickets', view_name='ticket-detail')
    root_group = HyperlinkedRelatedField(read_only=True, source='contactuser.root_group', view_name='group-detail')

    class Meta:
        model = User
        fields = ('username', 'email', 'tickets', 'root_group')


class ContactInfoSerializer(ModelSerializer):
    contact = PrimaryKeyRelatedField(write_only=True, queryset=models.Bundle.objects.filter(is_contact=True))
    class Meta:
        model = models.ContactInfo
        fields = ('id', 'type', 'version', 'data', 'contact')


class BundleSerializer(ModelSerializer):
    class Meta:
        model = models.Bundle
        fields = ('id', 'last_modified', 'is_contact')


class ContactSerializer(BundleSerializer):
    is_contact = HiddenField(default=True)
    information = ContactInfoSerializer(many=True, read_only=True, source='infos')

    class Meta(BundleSerializer.Meta):
        fields = BundleSerializer.Meta.fields + ('label', 'information',)


class GroupSerializer(BundleSerializer):
    inner_bundles = BundleSerializer(many=True, read_only=True)
    is_contact = HiddenField(default=False)

    class Meta(BundleSerializer.Meta):
        fields = BundleSerializer.Meta.fields + ('label', 'inner_bundles')


class TicketSerializer(ModelSerializer):
    last_modified = DateTimeField(source='bundle.last_modified')

    class Meta:
        model = models.Ticket
        fields = ('id', 'bundle', 'last_modified', 'label', 'can_share', 'can_edit')

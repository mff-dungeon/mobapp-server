import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models import *


class Bundle(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = CharField(max_length=256)
    owner = ForeignKey(User, related_name='owned_contacts', on_delete=SET_NULL, null=True)
    last_modified = DateTimeField(auto_now=True)

    # TODO: limit groups -> contacts, otherwise loops might be created
    inner_bundles = ManyToManyField('Bundle', related_name='in_bundles', blank=True)

    is_contact = BooleanField()
    information = JSONField(blank=True, default=list)

    @property
    def kind(self):
        if self.is_contact:
            return "Contact"
        else:
            return "Group"

    def __str__(self):
        return "%s \"%s\" by %s" % (self.kind, self.label, self.owner)

    def __repr__(self):
        return "%s <%s> \"%s\" by %s" % (self.kind, self.id, self.label, self.owner)


class Ticket(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = CharField(max_length=256)
    bundle = ForeignKey(Bundle, related_name='tickets', on_delete=PROTECT)
    owner = ForeignKey(User, related_name='tickets', on_delete=CASCADE)

    cloned_from = ForeignKey('Ticket', blank=True, null=True, related_name='children',
                             on_delete=PROTECT)  # Direct clone of, e.g. predecessor in the tree
    cloned_root = ForeignKey('Ticket', blank=True, null=True, related_name='all_clones',
                             on_delete=PROTECT)  # The root of the tree

    clones_shareable = BooleanField()
    clones_editable = BooleanField()

    can_share = BooleanField()
    can_edit = BooleanField()

    def __str__(self):
        b = self.bundle
        return "Ticket \"%s\" for %s" % (self.label, self.bundle)

    def __repr__(self):
        b = self.bundle
        return "Ticket <%s> \"%s\" for %s" % (self.id, self.label, self.bundle)

    def clone_other(self, other):
        self.label = 'Clone of %s' % other.label
        self.bundle = other.bundle

        self.cloned_from = other
        self.cloned_root = other.cloned_root

        self.clones_shareable = other.clones_shareable
        self.clones_editable = other.clones_editable

        self.can_share = other.clones_shareable
        self.can_edit = other.clones_editable


class ContactUser(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    root_contact = ForeignKey(Bundle, related_name='+', on_delete=PROTECT)

from polymorphic.models import PolymorphicModel

from netbox.models import NetBoxModel, PrimaryModel, ChangeLoggingMixin
from netbox_routing.querysets import NetBoxPolyMorphicQuerySet


class NetBoxPolymorphicModel(ChangeLoggingMixin, PolymorphicModel):

    objects = NetBoxPolyMorphicQuerySet.as_manager()

    class Meta:
        abstract = True


class PrimaryPolymorphicModel(PolymorphicModel, PrimaryModel):

    objects = NetBoxPolyMorphicQuerySet.as_manager()

    class Meta:
        abstract = True
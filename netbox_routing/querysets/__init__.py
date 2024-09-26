from polymorphic.query import PolymorphicQuerySet

from utilities.querysets import RestrictedQuerySet


class NetBoxPolyMorphicQuerySet(PolymorphicQuerySet, RestrictedQuerySet):
    pass
from django.contrib.contenttypes.fields import GenericRelation, GenericRel


class NetBoxGenericRel(GenericRel):
    def value_from_object(self, obj):
        """Return the value of this field in the given model instance."""
        # Get the accessor name; returns None if related_name='+'
        accessor_name = self.get_accessor_name()
        if not accessor_name:
            return None

        # Safely access the related manager
        manager = getattr(obj, accessor_name, None)
        if manager is None:
            return None

        # Get the first related object's pk
        if value := manager.first():
            return value.pk
        return None


class NetBoxGenericRelation(GenericRelation):
    rel_class = NetBoxGenericRel

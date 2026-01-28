from django.contrib.contenttypes.fields import GenericRelation, GenericRel


class NetBoxGenericRel(GenericRel):
    def value_from_object(self, obj):
        """Return the value of this field in the given model instance."""
        if value := getattr(obj, self.related_name).first():
            return value.pk
        return None


class NetBoxGenericRelation(GenericRelation):
    rel_class = NetBoxGenericRel

from netbox.ui.attrs import TextAttr
from utilities.data import resolve_attr_path
from utilities.object_types import object_type_name

__all__ = ('ContentTypeAttribute',)


class ContentTypeAttribute(TextAttr):
    """
    An ObjectAttribute for displaying a ContentType. The value is the ContentType's model name, but the label is the
    verbose name of the model.
    """

    def get_value(self, obj):
        value = resolve_attr_path(obj, self.accessor)
        if value is None:
            return None
        return object_type_name(value, include_app=False)

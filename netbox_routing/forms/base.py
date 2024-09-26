from polymorphic.formsets import PolymorphicFormSetChild

from netbox.forms import NetBoxModelForm


class NetboxPolymorphicFormSetChild(NetBoxModelForm, PolymorphicFormSetChild):
    pass
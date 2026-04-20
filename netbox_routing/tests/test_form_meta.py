"""
Introspection tests that verify every form for a PrimaryModel-based model
includes the standard PrimaryModel fields in Meta.fields.

This guards against the class of bug where fields like description, comments,
tags, or owner exist on the model but are silently dropped on UI save because
they were omitted from the form's Meta.fields list.
"""

from django.test import SimpleTestCase

from netbox.models import PrimaryModel
from netbox_routing.forms import model_objects

STANDARD_PRIMARYMODEL_FIELDS = ('description', 'comments', 'tags', 'owner')


def _iter_model_forms():
    """Yield every ModelForm class declared in netbox_routing.forms.model_objects."""
    from django.forms import ModelForm

    seen = set()
    for submodule_name in ('bgp', 'community', 'eigrp', 'objects', 'ospf', 'static'):
        submodule = getattr(model_objects, submodule_name, None)
        if submodule is None:
            continue
        for attr_name in dir(submodule):
            attr = getattr(submodule, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, ModelForm)
                and attr is not ModelForm
                and attr.__module__.startswith('netbox_routing.')
                and attr not in seen
            ):
                seen.add(attr)
                yield attr


class PrimaryModelFormFieldsTestCase(SimpleTestCase):
    """Every form whose model inherits from PrimaryModel must expose the
    standard fields in Meta.fields."""

    def test_all_primarymodel_forms_include_standard_fields(self):
        missing = {}
        for form_cls in _iter_model_forms():
            model = getattr(getattr(form_cls, 'Meta', None), 'model', None)
            if model is None or not issubclass(model, PrimaryModel):
                continue
            declared = set(form_cls.Meta.fields)
            gaps = [f for f in STANDARD_PRIMARYMODEL_FIELDS if f not in declared]
            if gaps:
                missing[form_cls.__name__] = gaps
        self.assertFalse(
            missing,
            msg=(
                'Forms missing standard PrimaryModel fields in Meta.fields. '
                'These fields will be silently dropped on UI save:\n'
                + '\n'.join(
                    f'  {name}: {fields}' for name, fields in sorted(missing.items())
                )
            ),
        )

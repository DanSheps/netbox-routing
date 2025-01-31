from django import forms
from django.apps import apps
from django.forms import fields
from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelForm
from netbox_routing.choices.objects import RouteMapOptions
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from utilities.forms.fields import DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups


__all__ = (
    'PrefixListForm',
    'PrefixListEntryForm',

    'RouteMapForm',
    'RouteMapEntryForm'
)


class PrefixListForm(NetBoxModelForm):

    class Meta:
        model = PrefixList
        fields = ('name', 'description', 'comments', )


class PrefixListEntryForm(NetBoxModelForm):

    class Meta:
        model = PrefixListEntry
        fields = ('prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge', 'description', 'comments', )


class RouteMapForm(NetBoxModelForm):

    class Meta:
        model = RouteMap
        fields = ('name', 'description', 'comments', )


class RouteMapEntryForm(NetBoxModelForm):

    class Meta:
        model = RouteMapEntry
        fields = ['route_map', 'sequence', 'type', 'description', 'comments', ]

    def _init_fields(self):
        choices = RouteMapOptions.CHOICES
        fieldtypes = RouteMapOptions.FIELD_TYPES
        for key, label in choices:
            initial = None
            if hasattr(self, 'instance'):
                if key[0:5] == 'match' and self.instance.match is not None:
                    initial = self.instance.match.get(key[6:], None)
                if key[0:3] == 'set' and self.instance.set is not None:
                    initial = self.instance.set.get(key[4:], None)

            if self.fields and key in self.fields:
                continue
            elif fieldtypes[key] == 'char':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=255
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif fieldtypes[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif fieldtypes[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif fieldtypes[key] == 'boolean':
                choices = (
                    (None, '---------'),
                    (True, _('True')),
                    (False, _('False')),
                )
                self.fields[key] = fields.NullBooleanField(
                    label=label,
                    required=False,
                    initial=initial,
                    widget=forms.Select(choices=choices)
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif type(fieldtypes[key]) is dict and fieldtypes[key].get('multiple') is True:
                app, model = fieldtypes[key].get('model').split('.', 1)
                queryset = apps.get_model(app, model).objects.all()
                self.fields[key] = DynamicModelMultipleChoiceField(
                    queryset=queryset,
                    label=label,
                    required=False,
                    selector=True,
                    initial=initial,
                )

    def __append_fieldsets(self):
        match = []
        set = []

        for key in RouteMapOptions.FIELD_TYPES.keys():
            if key[0:5] == 'match':
                match.append(key)
            else:
                set.append(key)

        fieldset = FieldSet(
            TabbedGroups(
                FieldSet(*match, name=_('Match Fields')),
                FieldSet(*set, name=_('Set Fields')),
            ),
            name=_('Criteria'),
        )
        return fieldset

    @property
    def fieldsets(self):
        fieldsets = list(self.get_fieldsets())

        settings_fieldset = self.__append_fieldsets()
        if settings_fieldset:
            fieldsets.append(settings_fieldset)

        return fieldsets

    def get_fieldsets(self):
        return (
            FieldSet('route_map', 'sequence', 'type', 'description', name=_('Route Map Entry')),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_fields()

    def save(self, *args, **kwargs):
        self.cleaned_data['match'] = {}
        self.cleaned_data['set'] = {}
        if self.instance.pk is not None:
            self.cleaned_data['match'] = self.instance.match if self.instance.match else {}
            self.cleaned_data['set'] = self.instance.set if self.instance.set else {}

        choices = RouteMapOptions.CHOICES
        fieldtypes = RouteMapOptions.FIELD_TYPES
        for key, label in choices:
            if key[0:5] == 'match':
                field = 'match'
                name = key[6:]
            else:
                field = 'set'
                name = key[4:]

            if key in self.cleaned_data.keys():
                value = self.cleaned_data.pop(key)
                if type(fieldtypes[key]) == dict and fieldtypes[key].get('multiple') is True:
                    value = [pk for pk in value.all().values_list('pk', flat=True)]
                self.cleaned_data[field][name] = value
            elif key not in self.cleaned_data.keys() and name in self.cleaned_data[field].keys():
                del self.cleaned_data[field][name]

        if not self.cleaned_data['set']:
            self.cleaned_data['set'] = None
        else:
            self.instance.set = self.cleaned_data['set']

        if not self.cleaned_data['match']:
            self.instance.match = None
        else:
            self.instance.match = self.cleaned_data['match']

        return super().save(*args, **kwargs)

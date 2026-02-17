from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.utils.translation import gettext as _

from ipam.models import Prefix
from netbox.forms import PrimaryModelForm
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)

from netbox_routing.models.community import Community, CommunityList
from netbox_routing.models.objects import *

__all__ = (
    'PrefixListForm',
    'PrefixListEntryForm',
    'RouteMapForm',
    'RouteMapEntryForm',
    'ASPathForm',
    'ASPathEntryForm',
    'CustomPrefixForm',
)

from utilities.forms.rendering import TabbedGroups, FieldSet

from utilities.querysets import RestrictedQuerySet


class ASPathForm(PrimaryModelForm):

    class Meta:
        model = ASPath
        fields = (
            'name',
            'description',
            'comments',
            'tags',
            'owner',
        )


class ASPathEntryForm(PrimaryModelForm):

    class Meta:
        model = ASPathEntry
        fields = (
            'aspath',
            'sequence',
            'action',
            'pattern',
            'description',
            'comments',
            'tags',
            'owner',
        )


class PrefixListForm(PrimaryModelForm):

    class Meta:
        model = PrefixList
        fields = (
            'name',
            'family',
            'description',
            'comments',
            'tags',
            'owner',
        )

    def clean_family(self):
        family = self.cleaned_data.get('family')
        if not family:
            raise forms.ValidationError(_('Family must be specified'))
        try:
            self.cleaned_data['family'] = int(family)
        except ValueError:
            raise forms.ValidationError(_('Family must be an integer'))
        return self.cleaned_data['family']


class PrefixListEntryForm(PrimaryModelForm):
    ipam_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix'),
    )
    custom_prefix = DynamicModelChoiceField(
        queryset=CustomPrefix.objects.all(),
        required=False,
        selector=True,
        quick_add=True,
        label=_('Custom Prefix'),
    )

    fieldsets = (
        FieldSet(
            'prefix_list',
            'sequence',
            'action',
        ),
        FieldSet(
            TabbedGroups(
                FieldSet('ipam_prefix', name=_('Prefix')),
                FieldSet('custom_prefix', name=_('Custom Prefix')),
            ),
            name=_('Prefix'),
        ),
        FieldSet(
            'le',
            'ge',
            name=_('Filtering'),
        ),
        FieldSet(
            'description',
        ),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = PrefixListEntry
        fields = (
            'prefix_list',
            'sequence',
            'action',
            'ipam_prefix',
            'custom_prefix',
            'le',
            'ge',
            'description',
            'comments',
            'tags',
            'owner',
        )

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_prefix) is Prefix:
                initial['ipam_prefix'] = instance.assigned_prefix
            elif type(instance.assigned_prefix) is CustomPrefix:
                initial['custom_prefix'] = instance.assigned_prefix
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        # Handle object assignment
        selected_objects = [
            field
            for field in ('ipam_prefix', 'custom_prefix')
            if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[1]: _(
                        "You can only assign a prefix or a custom prefix."
                    )
                }
            )
        elif selected_objects:
            self.instance.assigned_prefix = self.cleaned_data[selected_objects[0]]
        else:
            raise ValidationError(_('A Prefix or Custom Prefix must be specified'))


class CustomPrefixForm(PrimaryModelForm):

    fieldsets = (
        FieldSet(
            'prefix',
            'description',
        ),
    )

    class Meta:
        model = CustomPrefix
        fields = (
            'prefix',
            'description',
            'comments',
            'tags',
            'owner',
        )


class RouteMapForm(PrimaryModelForm):

    class Meta:
        model = RouteMap
        fields = (
            'name',
            'description',
            'comments',
            'tags',
            'owner',
        )


class RouteMapEntryForm(PrimaryModelForm):
    continue_entry = forms.IntegerField(
        required=False,
        label=_("Continue"),
        help_text=_("0 = Next Entry; >0 = Sequence Number"),
    )
    match_community = DynamicModelChoiceField(
        queryset=Community.objects.all(),
        required=False,
        selector=True,
        label=_('Match Community'),
    )
    match_community_list = DynamicModelChoiceField(
        queryset=CommunityList.objects.all(),
        required=False,
        selector=True,
        label=_('Match Community List'),
    )
    match_ipv4 = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Match IPv4'),
        query_params={'family': '4'},
    )
    match_ipv6 = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Match IPv6'),
        query_params={'family': '6'},
    )
    match_aspath = DynamicModelMultipleChoiceField(
        queryset=ASPath.objects.all(),
        required=False,
        selector=True,
        label=_('Match AS-Path'),
    )

    class Meta:
        model = RouteMapEntry
        fields = (
            'route_map',
            'sequence',
            'action',
            'match',
            'set',
            'description',
            'comments',
            'tags',
            'owner',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            matches = [
                field.replace('match_', '')
                for field in self.fields.keys()
                if 'match_' in field
            ]
            sets = [
                field.replace('sets_', '')
                for field in self.fields.keys()
                if 'set_' in field
            ]
            for field in matches:
                if field in self.instance.match.keys():
                    self.fields[f'match_{field}'].initial = self.instance.match.pop(
                        field
                    )
            for field in sets:
                if field in self.instance.set.keys():
                    self.fields[f'set_{field}'].initial = self.instance.match.pop(field)

    def clean(self, *args, **kwargs):
        super().clean()
        temp = self.cleaned_data.get('match', {})
        if temp is None:
            temp = {}
        matches = [field for field in self.fields.keys() if 'match_' in field]
        for field in matches:
            if data := self.cleaned_data.pop(field):
                name = field.replace('match_', '')
                if type(data) is RestrictedQuerySet:
                    temp.update({f'{name}': [d.pk for d in data]})
                elif type(data) is Model:
                    temp.update({f'{name}': data.pk})
                else:
                    temp.update({f'{name}': data.pk})
        self.cleaned_data['match'] = temp

        temp = self.cleaned_data.get('set', {})
        if temp is None:
            temp = {}
        sets = [field for field in self.fields.keys() if 'sets_' in field]
        for field in sets:
            if data := self.cleaned_data.pop(field):
                name = field.replace('set_', '')
                if type(data) is RestrictedQuerySet:
                    temp.update({f'{name}': [d.pk for d in data]})
                elif type(data) is Model:
                    temp.update({f'{name}': data.pk})
                else:
                    temp.update({f'{name}': data.pk})
        self.cleaned_data['set'] = temp

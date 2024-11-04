from django import forms
from django.forms import fields
from django.utils.translation import gettext as _

from ipam.models import VRF
from netbox.forms import NetBoxModelForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelMultipleChoiceField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups


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
    match_v4_prefixlist = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        label=_('V4 Prefix List'),
        required=False
    )
    match_v6_prefixlist = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        label=_('V4 Prefix List'),
        required=False
    )
    match_v4_acl = fields.CharField(
        label=_('V4 ACL'),
        required=False
    )
    match_v6_acl = fields.CharField(
        label=_('V6 ACL'),
        required=False
    )
    match_interface = fields.CharField(
        label=_('Interface'),
        required=False
    )
    set_v4_vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        label=_('V4 VRF'),
        required=False,
    )
    set_v6_vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        label=_('V6 VRF'),
        required=False,
    )
    set_v4_global = fields.NullBooleanField(
        label=_('V4 Set Global VRF'),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    set_v6_global = fields.NullBooleanField(
        label=_('V4 Set Global VRF'),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    set_interface = fields.CharField(
        label=_('Interface'),
        required=False
    )
    set_local_preference = fields.IntegerField(
        label=_('Local Preference'),
        required=False
    )
    set_local_preference = fields.IntegerField(
        label=_('Local Preference'),
        required=False
    )
    set_weight = fields.IntegerField(
        label=_('Weight'),
        required=False
    )
    set_metric = fields.IntegerField(
        label=_('Metric'),
        required=False
    )

    fieldsets = (
        FieldSet('route_map', 'sequence', 'type', 'description', name=_('Settings')),
        FieldSet(
            TabbedGroups(
                FieldSet(
                    # IPv4
                    'match_v4_prefixlist', 'match_v4_acl', #'match_v4_flowspec_src_prefixlist',
                    # 'match_v4_flowspec_dst_prefix_list', 'match_v4_flowspec_src_acl', 'match_v4_flowspec_dst_acl',
                    # 'match_v4_nh_prefixlist', 'match_v4_nh_acl', 'match_v4_rds_prefixlist', 'match_v4_rds_acl',
                    # 'match_v4_rs_prefixlist', 'match_v4_rs_acl', 'match_v4_rs_rds_prefixlist', 'match_v4_rs_rds_acl',
                    # IPv6
                    'match_v6_prefixlist', 'match_v6_acl', #'match_v6_flowspec_src_prefixlist',
                    # 'match_v6_flowspec_dst_prefix_list', 'match_v6_flowspec_src_acl', 'match_v6_flowspec_dst_acl',
                    # 'match_v6_nh_prefixlist', 'match_v6_nh_acl', 'match_v6_rs_prefixlist', 'match_v6_rs_acl',
                    # Interface
                    'match_interface',
                    name=_('Match')
                ),
                FieldSet(
                    # IPv4
                    'set_v4_vrf', 'set_v4_global',
                    # IPv6
                    'set_v6_vrf', 'set_v6_global',
                    # Interface
                    'set_interface',
                    # Properties
                    'set_local_preference', 'set_weight', 'set_metric',
                    name=_('Set')
                )
            ),
        ),
    )
    class Meta:
        model = RouteMapEntry
        fields = ('route_map', 'sequence', 'type', 'description', 'comments', )

    def save(self, *args, **kwargs):
        from pprint import pprint
        pprint(self.cleaned_data)

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from ipam.models import Role

from utilities.filtersets import register_filterset

from netbox_routing.models.community import *

__all__ = (
    'CommunityFilterSet',
    'CommunityListFilterSet',
    'CommunityListEntryFilterSet',
)


@register_filterset
class CommunityFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    role_id = django_filters.ModelMultipleChoiceFilter(
        field_name='role',
        queryset=Role.objects.all(),
        label=_('Role (ID)'),
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='role__name',
        queryset=Role.objects.all(),
        to_field_name='name',
        label=_('Role (Name)'),
    )

    class Meta:
        model = Community
        fields = (
            'community',
            'status',
            'role_id',
            'role',
            'tenant_id',
            'tenant',
            'tenant_group_id',
            'tenant_group',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(community__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class CommunityListFilterSet(TenancyFilterSet, NetBoxModelFilterSet):

    class Meta:
        model = CommunityList
        fields = ('name', 'tenant_id', 'tenant', 'tenant_group_id', 'tenant_group')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class CommunityListEntryFilterSet(NetBoxModelFilterSet):
    community_list_id = django_filters.ModelMultipleChoiceFilter(
        field_name='community_list',
        queryset=CommunityList.objects.all(),
        label=_('Community List (ID)'),
    )
    community_list = django_filters.ModelMultipleChoiceFilter(
        field_name='community_list__name',
        queryset=CommunityList.objects.all(),
        to_field_name='name',
        label=_('Community List (Name)'),
    )
    community_id = django_filters.ModelMultipleChoiceFilter(
        field_name='community',
        queryset=Community.objects.all(),
        label=_('Community (ID)'),
    )
    community = django_filters.ModelMultipleChoiceFilter(
        field_name='community__community',
        queryset=Community.objects.all(),
        to_field_name='community',
        label=_('Community (Community)'),
    )

    class Meta:
        model = CommunityListEntry
        fields = (
            'community_list_id',
            'community_list',
            'community_id',
            'community',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(community_list__name__icontains=value)
        qs_filter |= Q(community__community__icontains=value)
        return queryset.filter(qs_filter).distinct()

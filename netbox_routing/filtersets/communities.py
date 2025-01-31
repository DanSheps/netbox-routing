import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Tenant

from netbox_routing.models.communities import *


__all__ = (
    'CommunityListFilterSet',
    'CommunityFilterSet',
)


class CommunityListFilterSet(NetBoxModelFilterSet):
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )
    community_id = django_filters.ModelMultipleChoiceFilter(
        field_name='communities',
        queryset=Tenant.objects.all(),
        label=_('Community (ID)'),
    )
    community = django_filters.ModelMultipleChoiceFilter(
        field_name='communities__community',
        queryset=Tenant.objects.all(),
        to_field_name='community',
        label=_('Community'),
    )

    class Meta:
        model = CommunityList
        fields = ('tenant_id', 'tenant', 'community_id',  'community', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value) |
            Q(communities__community__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class CommunityFilterSet(NetBoxModelFilterSet):
    community_list_id = django_filters.ModelMultipleChoiceFilter(
        field_name='community_lists',
        queryset=Tenant.objects.all(),
        label=_('Community List (ID)'),
    )
    community_list = django_filters.ModelMultipleChoiceFilter(
        field_name='community_lists__name',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Community List'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = Community
        fields = ('community_list_id', 'community_list', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(community_lists__name__icontains=value) |
            Q(community__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

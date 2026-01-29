from netbox.search import SearchIndex, register_search
from netbox_routing.models.eigrp import EIGRPRouter, EIGRPAddressFamily

__all__ = (
    'EIGRPRouterIndex',
    'EIGRPAddressFamilyIndex',
)


@register_search
class EIGRPRouterIndex(SearchIndex):
    model = EIGRPRouter
    fields = (
        ('rid', 100),
        ('pid', 200),
        ('name', 210),
        ('comments', 5000),
    )
    display_attrs = ('device', 'mode')


@register_search
class EIGRPAddressFamilyIndex(SearchIndex):
    model = EIGRPAddressFamily
    fields = (
        ('rid', 100),
        ('comments', 5000),
    )

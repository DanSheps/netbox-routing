from netbox.search import SearchIndex, register_search
from netbox_routing.models.static import StaticRoute

@register_search
class StaticRouteIndex(SearchIndex):
    model = StaticRoute
    fields = (
        ('name', 100),
        ('prefix', 200),
        ('next_hop', 300),
        ('comments', 5000),
    )
    display_attrs = ('prefix', 'next_hop', 'vrf')

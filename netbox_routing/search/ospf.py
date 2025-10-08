from netbox.search import SearchIndex, register_search
from netbox_routing.models.ospf import OSPFInstance, OSPFArea

@register_search
class OSPFInstanceIndex(SearchIndex):
    model = OSPFInstance
    fields = (
        ('name', 100),
        ('router_id', 200),
        ('process_id', 300),
        ('comments', 5000),
    )
    display_attrs = ('process_id', 'device', 'vrf')

@register_search
class OSPFAreaIndex(SearchIndex):
    model = OSPFArea
    fields = (
        ('area_id', 100),
        ('comments', 5000),
    )

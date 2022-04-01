from django.db.models import Q

BGPSETTING_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope')
)

BGPAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope') |
    Q(app_label='netbox_routing', model='bgpneighbor') |
    Q(app_label='ipam', model='VRF')
)

BGPNEIGHBOR_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope') |
    Q(app_label='netbox_routing', model='bgpaddressfamily')
)
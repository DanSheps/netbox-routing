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

BGPPEER_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope') |
    Q(app_label='netbox_routing', model='bgpaddressfamily')
)

BGPPEERAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgppeer') |
    Q(app_label='netbox_routing', model='bgppeergroup') |
    Q(app_label='netbox_routing', model='bgptemplatepeer') |
    Q(app_label='netbox_routing', model='bgptemplatepeerpolicy')
)
from django.db.models import Q

BGPSETTING_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter')
    | Q(app_label='netbox_routing', model='bgpscope')
    | Q(app_label='netbox_routing', model='bgpaddressfamily')
    | Q(app_label='netbox_routing', model='bgppeer')
    | Q(app_label='netbox_routing', model='bgppeeraddressfamily')
)

BGPAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter')
    | Q(app_label='netbox_routing', model='bgpscope')
)

BGPPEER_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter')
    | Q(app_label='netbox_routing', model='bgpscope')
)

BGPPEERAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgppeer')
    | Q(app_label='netbox_routing', model='bgppeertemplate')
)

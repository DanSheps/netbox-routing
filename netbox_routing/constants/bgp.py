from django.db.models import Q

BGPSETTING_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope')
)

BGPAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope')
)

BGPPEER_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgprouter') |
    Q(app_label='netbox_routing', model='bgpscope')
)

BGPPEERAF_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='bgppeer') |
    Q(app_label='netbox_routing', model='bgppeergroup') |
    Q(app_label='netbox_routing', model='bgptemplatepeer') |
    Q(app_label='netbox_routing', model='bgptemplatepeerpolicy')
)
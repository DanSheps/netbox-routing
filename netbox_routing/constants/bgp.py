from django.db.models import Q


__all__ = (
    'BGPROUTER_ASSIGNMENT_MODEL',
    'BGPSETTING_ASSIGNMENT_MODELS',
    'BGPAF_ASSIGNMENT_MODELS',
    'BGPPEER_ASSIGNMENT_MODELS',
    'BGPPEERAF_ASSIGNMENT_MODELS',
)


BGPROUTER_ASSIGNMENT_MODEL = Q(
    Q(app_label='dcim', model='region')
    | Q(app_label='dcim', model='site')
    | Q(app_label='dcim', model='site_group')
    | Q(app_label='dcim', model='location')
    | Q(app_label='dcim', model='device')
    | Q(app_label='virtualization', model='cluster')
    | Q(app_label='virtualization', model='virtual_machine')
)

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

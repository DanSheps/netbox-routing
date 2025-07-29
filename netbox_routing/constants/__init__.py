from .bgp import *
from .eigrp import *


__all__ = (
    # BGP
    'BGPAF_ASSIGNMENT_MODELS',
    'BGPPEER_ASSIGNMENT_MODELS',
    'BGPPEERAF_ASSIGNMENT_MODELS',
    'BGPSETTING_ASSIGNMENT_MODELS',
    # EIGRP
    'EIGRP_ROUTER_MODELS',
    'EIGRP_ASSIGNABLE_MODELS',
    # Objects
    'ROUTEMAPMATCH_ASSIGNMENT_MODELS',
)


ROUTEMAPMATCH_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='prefix')
    | Q(app_label='netbox_routing', model='prefixlist')
    | Q(app_label='netbox_routing', model='community')
    | Q(app_label='netbox_routing', model='communitylist')
    | Q(app_label='netbox_routing', model='aspathlist')
    | Q(app_label='netbox_routing', model='bgppeergroup')
    | Q(app_label='netbox_routing', model='bgptemplatepeer')
    | Q(app_label='netbox_routing', model='bgptemplatepeerpolicy')
)

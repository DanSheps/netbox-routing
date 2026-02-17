from django.db.models import Q

__all__ = ('PREFIX_ASSIGNMENT_MODELS',)

PREFIX_ASSIGNMENT_MODELS = Q(
    Q(app_label='ipam', model='prefix')
    | Q(app_label='netbox_routing', model='customprefix')
)

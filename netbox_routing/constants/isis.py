# SPDX-License-Identifier: Apache-2.0

from django.db.models import Q

__all__ = (
    'ISISSETTING_ASSIGNMENT_MODELS',
)


ISISSETTING_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_routing', model='isisinstance')
    | Q(app_label='netbox_routing', model='isisinterface')
)

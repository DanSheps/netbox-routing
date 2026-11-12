# SPDX-License-Identifier: Apache-2.0

from functools import reduce
from operator import or_

from django.db.models import Q

__all__ = (
    'ISISSETTING_ASSIGNMENT_MODEL_NAMES',
    'ISISSETTING_ASSIGNMENT_MODELS',
)


# Single source of truth for the object types an ISISSetting may attach to. Both the
# limit_choices_to Q below and ISISSetting.clean()'s allow-list derive from this, so a
# new assignable type can't be added to one and silently missed by the other.
ISISSETTING_ASSIGNMENT_MODEL_NAMES = ('isisinstance', 'isisinterface')

# NB: wrap the OR-reduction in an outer Q so this deconstructs identically to the
# original literal Q(Q(a) | Q(b)) — keeping migration 0033's limit_choices_to in sync
# (makemigrations would otherwise see a changed field).
ISISSETTING_ASSIGNMENT_MODELS = Q(
    reduce(
        or_,
        (Q(app_label='netbox_routing', model=name) for name in ISISSETTING_ASSIGNMENT_MODEL_NAMES),
    )
)

# SPDX-License-Identifier: Apache-2.0

import re

from django.utils.translation import gettext_lazy as _

__all__ = (
    'NET_RE',
    'auth_pair_errors',
)


# A NET (Network Entity Title) is hex bytes written as dot-separated groups: a
# 1-byte AFI, the area + 6-byte system-id as 2-byte (4-hex) groups, and a 1-byte
# N-selector — e.g. 49.0001.1921.6800.1001.00.
NET_RE = re.compile(r'^[0-9A-Fa-f]{2}(?:\.[0-9A-Fa-f]{4}){3,}\.[0-9A-Fa-f]{2}$')


def auth_pair_errors(type_value, key_value, type_field, key_field):
    """An IS-IS auth (type, key) pair is only meaningful together; return the
    field-keyed error(s) for a half-configured pair (shared by every IS-IS clean())."""
    if type_value and not key_value:
        return {
            key_field: _(
                'An authentication key is required when an authentication type is set.'
            )
        }
    if key_value and not type_value:
        return {
            type_field: _(
                'An authentication type is required when an authentication key is set.'
            )
        }
    return {}

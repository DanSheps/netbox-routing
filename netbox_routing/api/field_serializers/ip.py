import netaddr
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

__all__ = (
    'IPAddressField',
)


class IPAddressField(serializers.CharField):
    """
    An IPv4 or IPv6 address with optional mask
    """
    default_error_messages = {
        'invalid': _('Enter a valid IPv4 or IPv6 address with optional mask.'),
    }

    def to_internal_value(self, data):
        try:
            return netaddr.IPAddress(data)
        except netaddr.AddrFormatError:
            raise serializers.ValidationError(_("Invalid IP address format: {data}").format(data))
        except (TypeError, ValueError) as e:
            raise serializers.ValidationError(e)

    def to_representation(self, value):
        return str(value)

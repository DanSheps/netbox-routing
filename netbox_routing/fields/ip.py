from django.core.exceptions import ValidationError
from django.db import models
from netaddr import AddrFormatError, IPAddress

from ipam.formfields import IPAddressFormField


class IPAddressField(models.Field):

    def python_type(self):
        return IPAddress

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            return value
        try:
            # Always return a netaddr.IPNetwork object. (netaddr.IPAddress does not provide a mask.)
            return IPAddress(value)
        except AddrFormatError:
            raise ValidationError("Invalid IP address format: {}".format(value))
        except (TypeError, ValueError) as e:
            raise ValidationError(e)

    def get_prep_value(self, value):
        if not value:
            return None
        if isinstance(value, list):
            return [str(self.to_python(v)) for v in value]
        return str(self.to_python(value))

    def form_class(self):
        return IPAddressFormField

    def formfield(self, **kwargs):
        defaults = {'form_class': self.form_class()}
        defaults.update(kwargs)
        return super().formfield(**defaults)
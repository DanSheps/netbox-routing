from django.core.exceptions import ValidationError
from django.test import TestCase

from utilities.testing import create_test_device

from netbox_routing.models import *

__all__ = (
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
)


class OSPFInstanceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Device 1')

    def test_distance_out_of_range(self):
        instance = OSPFInstance(
            name='Instance 1',
            device=self.device,
            router_id='1.1.1.1',
            process_id=1,
            distance=256,
        )
        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_default_information_metric_requires_originate(self):
        instance = OSPFInstance(
            name='Instance 1',
            device=self.device,
            router_id='1.1.1.1',
            process_id=1,
            default_information_metric=10,
            default_information_metric_type='type-1',
        )
        with self.assertRaises(ValidationError) as cm:
            instance.full_clean()
        self.assertIn('default_information_metric', cm.exception.error_dict)
        self.assertIn('default_information_metric_type', cm.exception.error_dict)

        instance.default_information_originate = 'always'
        instance.full_clean()

    def test_max_metric_on_startup_out_of_range(self):
        instance = OSPFInstance(
            name='Instance 1',
            device=self.device,
            router_id='1.1.1.1',
            process_id=1,
            max_metric_on_startup=4,
        )
        with self.assertRaises(ValidationError):
            instance.full_clean()


class OSPFAreaTestCase(TestCase):
    pass


class OSPFInterfaceTestCase(TestCase):
    pass

from django.test import TestCase

from dcim.models import Device, Interface
from ipam.models import VRF
from utilities.testing import create_test_device

from netbox_routing.forms import *
from netbox_routing.models import *

__all__ = (
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
)


class OSPFInstanceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        vrf = VRF.objects.create(name='Test VRF')
        device = create_test_device(name='Device 1')

    def test_instance(self):
        form = OSPFInstanceForm(data={
            'name': 'Instance 1',
            'process_id': '0',
            'router_id': '10.10.10.1',
            'device': Device.objects.first().pk,
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_instance_with_vrf(self):
        form = OSPFInstanceForm(data={
            'name': 'Instance 2',
            'process_id': '1',
            'router_id': '20.20.20.1',
            'device': Device.objects.first().pk,
            'vrf': VRF.objects.first().pk,
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class OSPFAreaTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_valid_area_id_with_ip(self):
        form = OSPFAreaForm(data={
            'area_id': '0.0.0.0',
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_valid_area_id_with_integer(self):
        form = OSPFAreaForm(data={
            'area_id': '0',
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_invalid_area(self):
        form = OSPFAreaForm(data={
            'area_id': 'a.a.a.a',
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class OSPFInterfaceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        interface = Interface.objects.create(name='Interface 1', device=device, type='virtual')
        instance = OSPFInstance.objects.create(
            name='Instance 1',
            router_id='10.10.10.1',
            process_id=0,
            device_id=device.pk
        )
        area = OSPFArea.objects.create(area_id='0.0.0.0')

    def test_interface_with_correct_device(self):
        form = OSPFInterfaceForm(data={
            'device': Device.objects.first().pk,
            'interface': Interface.objects.first().pk,
            'instance': OSPFInstance.objects.first().pk,
            'area': OSPFArea.objects.first().pk,
            'passive': True,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_interface_with_incorrect_device(self):
        device = create_test_device(name='Device 2')
        interface = Interface.objects.create(name='Interface 1', device=device, type='virtual')

        form = OSPFInterfaceForm(data={
            'device': device.pk,
            'interface': interface.pk,
            'instance': OSPFInstance.objects.first().pk,
            'area': OSPFArea.objects.first().pk,
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

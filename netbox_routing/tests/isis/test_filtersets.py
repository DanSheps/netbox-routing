# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from dcim.models import Device, Interface
from ipam.models import VRF
from utilities.testing import create_test_device

from netbox_routing.filtersets import ISISInstanceFilterSet, ISISInterfaceFilterSet
from netbox_routing.models import ISISInstance, ISISInterface

__all__ = (
    'ISISInstanceFilterSetTestCase',
    'ISISInterfaceFilterSetTestCase',
)


class ISISInstanceFilterSetTestCase(TestCase):
    queryset = ISISInstance.objects.all()
    filterset = ISISInstanceFilterSet

    @classmethod
    def setUpTestData(cls):
        vrfs = (
            VRF(name='VRF 1'),
            VRF(name='VRF 2'),
            VRF(name='VRF 3'),
        )
        VRF.objects.bulk_create(vrfs)

        devices = [
            create_test_device(name='Device 1'),
            create_test_device(name='Device 2'),
            create_test_device(name='Device 3'),
            create_test_device(name='Device 4'),
        ]

        data = (
            ISISInstance(
                device=devices[0],
                vrf=vrfs[0],
                process_tag='CORE',
                net='49.0001.0000.0000.0001.00',
                is_type='level-1-2',
            ),
            ISISInstance(
                device=devices[1],
                vrf=vrfs[1],
                process_tag='EDGE',
                net='49.0001.0000.0000.0002.00',
                is_type='level-2-only',
            ),
            ISISInstance(
                device=devices[2],
                vrf=None,
                process_tag='',
                net='49.0001.0000.0000.0003.00',
                is_type='level-1',
            ),
            ISISInstance(
                device=devices[3],
                vrf=vrfs[2],
                process_tag='FABRIC',
                net='49.0001.0000.0000.0004.00',
                is_type='level-1-2',
            ),
        )
        ISISInstance.objects.bulk_create(data)

    def test_q(self):
        params = {'q': 'CORE'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search_strips_whitespace(self):
        # search() must trim before the icontains match, otherwise '  CORE  '
        # would never match the 'CORE' process tag. Call search() directly: the
        # `q` form field already strips, which would otherwise mask an untrimmed
        # search() and make this a false pass.
        qs = self.filterset().search(self.queryset, 'q', '  CORE  ')
        self.assertEqual(qs.count(), 1)

    def test_process_tag(self):
        params = {'process_tag': ['CORE', 'EDGE']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_vrf(self):
        data = VRF.objects.order_by('pk')[:2]

        params = {'vrf_id': [data[0].pk, data[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'vrf': [data[0].name, data[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        data = Device.objects.order_by('pk')[:2]

        params = {'device_id': [data[0].pk, data[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'device': [data[0].name, data[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ISISInterfaceFilterSetTestCase(TestCase):
    queryset = ISISInterface.objects.all()
    filterset = ISISInterfaceFilterSet

    @classmethod
    def setUpTestData(cls):
        vrfs = (
            VRF(name='VRF 1'),
            VRF(name='VRF 2'),
            VRF(name='VRF 3'),
        )
        VRF.objects.bulk_create(vrfs)

        devices = (
            create_test_device(name='Device 1'),
            create_test_device(name='Device 2'),
            create_test_device(name='Device 3'),
            create_test_device(name='Device 4'),
        )
        interfaces = (
            Interface(device=devices[0], name='Interface 1', type='virtual'),
            Interface(device=devices[1], name='Interface 2', type='virtual'),
            Interface(device=devices[2], name='Interface 3', type='virtual'),
            Interface(device=devices[3], name='Interface 4', type='virtual'),
        )
        Interface.objects.bulk_create(interfaces)

        instances = (
            ISISInstance(
                device=devices[0],
                vrf=vrfs[0],
                process_tag='CORE',
                net='49.0001.0000.0000.0001.00',
                is_type='level-1-2',
            ),
            ISISInstance(
                device=devices[1],
                vrf=vrfs[1],
                process_tag='EDGE',
                net='49.0001.0000.0000.0002.00',
                is_type='level-2-only',
            ),
            ISISInstance(
                device=devices[2],
                vrf=None,
                process_tag='',
                net='49.0001.0000.0000.0003.00',
                is_type='level-1',
            ),
            ISISInstance(
                device=devices[3],
                vrf=vrfs[2],
                process_tag='FABRIC',
                net='49.0001.0000.0000.0004.00',
                is_type='level-1-2',
            ),
        )
        ISISInstance.objects.bulk_create(instances)

        data = (
            ISISInterface(
                interface=interfaces[0],
                instance=ISISInstance.objects.get(process_tag='CORE'),
                address_family='ipv4',
                circuit_type='level-1-2',
                network_type='point-to-point',
                passive=True,
                hello_auth_type='md5',
                hello_auth_key='s3cret',
            ),
            ISISInterface(
                interface=interfaces[1],
                instance=ISISInstance.objects.get(process_tag='EDGE'),
                address_family='ipv6',
                circuit_type='level-2-only',
                passive=False,
            ),
            ISISInterface(
                interface=interfaces[2],
                instance=ISISInstance.objects.get(net='49.0001.0000.0000.0003.00'),
                address_family='ipv4',
                circuit_type='level-1',
                passive=True,
            ),
            ISISInterface(
                interface=interfaces[3],
                instance=ISISInstance.objects.get(process_tag='FABRIC'),
                address_family='ipv6',
                circuit_type='level-1-2',
                passive=False,
            ),
        )
        ISISInterface.objects.bulk_create(data)

    def test_q(self):
        params = {'q': 'Interface 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        params = {'q': 'CORE'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search_strips_whitespace(self):
        # See ISISInstanceFilterSetTestCase.test_search_strips_whitespace: the
        # `q` field strips upstream, so exercise search() directly.
        qs = self.filterset().search(self.queryset, 'q', '  CORE  ')
        self.assertEqual(qs.count(), 1)

    def test_instances(self):
        data = ISISInstance.objects.order_by('pk')[:2]

        params = {'instance_id': [data[0].pk, data[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_address_family(self):
        params = {'address_family': ['ipv4']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_devices(self):
        data = Device.objects.order_by('pk')[:2]

        params = {'device_id': [data[0].pk, data[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'device': [data[0].name, data[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_interfaces(self):
        data = Interface.objects.order_by('pk')[:2]

        params = {'interface_id': [data[0].pk, data[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {'interface': [data[0].name, data[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_passive(self):
        params = {'passive': True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_hello_auth_type(self):
        params = {'hello_auth_type': ['md5']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

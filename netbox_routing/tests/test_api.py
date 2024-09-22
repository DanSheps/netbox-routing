from django.urls import reverse
from netaddr.ip import IPAddress
from rest_framework import status

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import APIViewTestCases, APITestCase, create_test_device

from netbox_routing.models import StaticRoute, OSPFInstance, OSPFArea, OSPFInterface
from netbox_routing.tests.base import IPAddressFieldMixin


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_routing-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StaticRouteTest(IPAddressFieldMixin , APIViewTestCases.APIViewTestCase):
    model = StaticRoute
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = ['description', 'display', 'id', 'name', 'next_hop', 'prefix', 'url', ]


    bulk_update_data = {
        'metric': 5
    }

    @classmethod
    def setUpTestData(cls):

        device = create_test_device(name='Test Device')
        vrf = VRF.objects.create(name='Test VRF')

        nh = IPAddress('10.10.10.1')

        routes = (
            StaticRoute(name='Test Route 1', vrf=vrf, prefix='0.0.0.0/0', next_hop=nh),
            StaticRoute(name='Test Route 2', vrf=None, prefix='1.1.1.1/32', next_hop=nh),
            StaticRoute(name='Test Route 3', vrf=vrf, prefix='2.2.2.2/32', next_hop=nh),
        )
        StaticRoute.objects.bulk_create(routes)

        routes[0].devices.set([device])
        routes[1].devices.set([device])
        routes[2].devices.set([device])

        cls.create_data = [
            {
                'name': 'Default Route',
                'devices': [device.pk],
                'vrf': vrf.pk,
                'prefix': '0.0.0.0/0',
                'next_hop': '10.10.10.2',
                'metric': 1,
                'permanent': True
            },
            {
                'name': 'Google DNS',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '4.4.4.4/32',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True
            },
            {
                'name': 'One dot one dot one dot one',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '1.1.1.0/24',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True
            },
        ]


class OSPFInstanceTest(IPAddressFieldMixin , APIViewTestCases.APIViewTestCase):
    model = OSPFInstance
    view_namespace = 'plugins-api:netbox_routing'
    brief_fields = ['device', 'display', 'id', 'name', 'process_id', 'router_id', 'url', ]


    bulk_update_data = {
        'description': "A test description"
    }

    @classmethod
    def setUpTestData(cls):

        device = create_test_device(name='Test Device')

        data = (
            cls.model(name='Instance 1', device=device, router_id='1.1.1.1', process_id=1),
            cls.model(name='Instance 2', device=device, router_id='2.2.2.2', process_id=2),
            cls.model(name='Instance 3', device=device, router_id='3.3.3.3', process_id=3),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'name': 'Instance X',
                'device': device.pk,
                'router_id': '4.4.4.4',
                'process_id': 4
            },
        ]


class OSPFAreaTest(IPAddressFieldMixin , APIViewTestCases.APIViewTestCase):
    model = OSPFArea
    view_namespace = 'plugins-api:netbox_routing'
    brief_fields = ['area_id', 'display', 'id', 'url', ]


    bulk_update_data = {
        'description': "A test description"
    }

    @classmethod
    def setUpTestData(cls):

        data = (
            cls.model(area_id='1'),
            cls.model(area_id='2'),
            cls.model(area_id='3'),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'area_id': '4',
            },
        ]


class OSPFInterfaceTest(IPAddressFieldMixin, APIViewTestCases.APIViewTestCase):
    model = OSPFInterface
    view_namespace = 'plugins-api:netbox_routing'
    brief_fields = ['device', 'display', 'id', 'name', 'process_id', 'router_id', 'url', ]


    bulk_update_data = {
        'description': "A test description"
    }

    @classmethod
    def setUpTestData(cls):

        device = create_test_device(name='Test Device')
        instance = OSPFInstance.objects.create(name='Instance 1', device=device, router_id='1.1.1.1', process_id=1)
        area = OSPFArea.objects.create(area_id='0')

        interfaces = (
            Interface(device=device, name='Interface 1', type='virtual'),
            Interface(device=device, name='Interface 2', type='virtual'),
            Interface(device=device, name='Interface 3', type='virtual'),
            Interface(device=device, name='Interface 4', type='virtual'),
        )
        Interface.objects.bulk_create(interfaces)

        data = (
            cls.model(device=device, instance=instance, area=area, interface=interfaces[0], ),
            cls.model(device=device, instance=instance, area=area, interface=interfaces[1], ),
            cls.model(device=device, instance=instance, area=area, interface=interfaces[2], ),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'device': device.pk,
                'instance': instance.pk,
                'area': area.pk,
                'interface': interfaces[3].pk,
                'priority': 2,
                'authentication': 'passphrase',
                'passphrase': 'test-password',
                'bfd': True,
            },
        ]

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import APIViewTestCases, create_test_device

from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface
from netbox_routing.tests.base import IPAddressFieldMixin

__all__ = (
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
)


class OSPFInstanceTestCase(IPAddressFieldMixin, APIViewTestCases.APIViewTestCase):
    model = OSPFInstance
    view_namespace = 'plugins-api:netbox_routing'
    brief_fields = ['device', 'display', 'id', 'name', 'process_id', 'router_id', 'url', 'vrf', ]

    user_permissions = ('dcim.view_device', )

    bulk_update_data = {
        'description': "A test description"
    }

    @classmethod
    def setUpTestData(cls):
        vrf = VRF.objects.create(name='Test VRF')
        device = create_test_device(name='Test Device')

        data = (
            cls.model(name='Instance 1', device=device, router_id='1.1.1.1', process_id=1, vrf=None),
            cls.model(name='Instance 2', device=device, router_id='2.2.2.2', process_id=2, vrf=vrf),
            cls.model(name='Instance 3', device=device, router_id='3.3.3.3', process_id=3, vrf=None),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'name': 'Instance X',
                'device': device.pk,
                'router_id': '4.4.4.4',
                'process_id': 4,
                'vrf': vrf.pk,
            },
        ]


class OSPFAreaTestCase(IPAddressFieldMixin , APIViewTestCases.APIViewTestCase):
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


class OSPFInterfaceTestCase(IPAddressFieldMixin, APIViewTestCases.APIViewTestCase):
    model = OSPFInterface
    view_namespace = 'plugins-api:netbox_routing'
    brief_fields = ['area', 'display', 'id', 'instance', 'interface', 'passive', 'url', ]

    user_permissions = (
        'netbox_routing.view_ospfinstance', 'netbox_routing.view_ospfarea', 'dcim.view_device', 'dcim.view_interface',
    )

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
            cls.model(instance=instance, area=area, interface=interfaces[0], passive=True),
            cls.model(instance=instance, area=area, interface=interfaces[1], passive=False),
            cls.model(instance=instance, area=area, interface=interfaces[2], ),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'instance': instance.pk,
                'area': area.pk,
                'interface': interfaces[3].pk,
                'passive': True,
                'priority': 2,
                'authentication': 'message-digest',
                'passphrase': 'test-password',
                'bfd': True,
            },
        ]

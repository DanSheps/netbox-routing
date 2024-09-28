import netaddr

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import ViewTestCases, create_test_device

from netbox_routing.models import StaticRoute, OSPFInstance, OSPFArea, OSPFInterface
from netbox_routing.tests.base import IPAddressFieldMixin

__all__ = (
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
)


class OSPFInstanceTestCase(
        IPAddressFieldMixin,
        ViewTestCases.GetObjectViewTestCase,
        ViewTestCases.GetObjectChangelogViewTestCase,
        ViewTestCases.CreateObjectViewTestCase,
        ViewTestCases.EditObjectViewTestCase,
        ViewTestCases.DeleteObjectViewTestCase,
        ViewTestCases.ListObjectsViewTestCase,
        ViewTestCases.BulkEditObjectsViewTestCase,
        ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = OSPFInstance

    @classmethod
    def setUpTestData(cls):
        vrf = VRF.objects.create(name='Test')
        devices = [create_test_device(name='Device 1'), create_test_device(name='Device 2')]

        instances = (
            cls.model(name="Instance 0", device=devices[0], router_id='0.0.0.0', process_id='0', vrf=None),
            cls.model(name="Instance 1", device=devices[0], router_id='1.1.1.1', process_id='1', vrf=None),
            cls.model(name="Instance 2", device=devices[0], router_id='2.2.2.2', process_id='2', vrf=vrf),
        )
        cls.model.objects.bulk_create(instances)

        cls.form_data = {
            'name': 'Instance X',
            'device': devices[1].pk,
            'router_id': '4.4.4.4',
            'process_id': 4,
            'vrf': vrf.pk,
        }

        cls.bulk_edit_data = {
            'description': 'A test Instance description',
            'vrf': vrf.pk
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:ospfinstance_{}'


class OSPFAreaTestCase(
        IPAddressFieldMixin,
        ViewTestCases.GetObjectViewTestCase,
        ViewTestCases.GetObjectChangelogViewTestCase,
        ViewTestCases.CreateObjectViewTestCase,
        ViewTestCases.EditObjectViewTestCase,
        ViewTestCases.DeleteObjectViewTestCase,
        ViewTestCases.ListObjectsViewTestCase,
        ViewTestCases.BulkEditObjectsViewTestCase,
        ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = OSPFArea

    @classmethod
    def setUpTestData(cls):
        areas = (
            cls.model(area_id='0.0.0.0'),
            cls.model(area_id='1.1.1.1'),
            cls.model(area_id='2.2.2.2'),
        )
        cls.model.objects.bulk_create(areas)

        cls.form_data = {
            'area_id': '4.4.4.4',
        }

        cls.bulk_edit_data = {
            'description': 'A test Area description'
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:ospfarea_{}'


class OSPFInterfaceTestCase(
        IPAddressFieldMixin,
        ViewTestCases.GetObjectViewTestCase,
        ViewTestCases.GetObjectChangelogViewTestCase,
        ViewTestCases.CreateObjectViewTestCase,
        ViewTestCases.EditObjectViewTestCase,
        ViewTestCases.DeleteObjectViewTestCase,
        ViewTestCases.ListObjectsViewTestCase,
        ViewTestCases.BulkEditObjectsViewTestCase,
        ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = OSPFInterface

    @classmethod
    def setUpTestData(cls):
        devices = [create_test_device(name='Device 1'), create_test_device(name='Device 2')]
        interfaces = (
            Interface(name='Interface 1', device=devices[0], type='virtual'),
            Interface(name='Interface 2', device=devices[0], type='virtual'),
            Interface(name='Interface 3', device=devices[1], type='virtual'),
            Interface(name='Interface 4', device=devices[1], type='virtual'),
        )
        Interface.objects.bulk_create(interfaces)

        instances = (
            OSPFInstance(name="Instance 0", device=devices[0], router_id='0.0.0.0', process_id='0'),
            OSPFInstance(name="Instance 1", device=devices[0], router_id='1.1.1.1', process_id='1'),
            OSPFInstance(name="Instance 2", device=devices[1], router_id='2.2.2.2', process_id='2'),
            OSPFInstance(name="Instance 3", device=devices[1], router_id='3.3.3.3', process_id='3'),
        )
        OSPFInstance.objects.bulk_create(instances)

        areas = (
            OSPFArea(area_id='0.0.0.0'),
            OSPFArea(area_id='1.1.1.1'),
            OSPFArea(area_id='2.2.2.2'),
            OSPFArea(area_id='3.3.3.3'),
        )
        OSPFArea.objects.bulk_create(areas)

        ospfinterfaces = (
            cls.model(interface=interfaces[0], instance=instances[0], area=areas[0], passive=False),
            cls.model(interface=interfaces[1], instance=instances[1], area=areas[1]),
            cls.model(interface=interfaces[2], instance=instances[2], area=areas[2], passive=False),
        )
        cls.model.objects.bulk_create(ospfinterfaces)

        cls.form_data = {
            'interface': interfaces[3].pk,
            'area': areas[3].pk,
            'instance': instances[3].pk,
            'passive': True,
        }

        cls.bulk_edit_data = {
            'description': 'A test Interface description',
            'passive': False,
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:ospfinterface_{}'

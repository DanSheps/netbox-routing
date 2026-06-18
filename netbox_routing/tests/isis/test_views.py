# SPDX-License-Identifier: Apache-2.0

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import ViewTestCases, create_test_device

from netbox_routing.models import ISISInstance, ISISInterface

__all__ = (
    'ISISInstanceViewTestCase',
    'ISISInterfaceViewTestCase',
)


class ISISInstanceViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = ISISInstance

    @classmethod
    def setUpTestData(cls):
        vrf = VRF.objects.create(name='Test')
        devices = [
            create_test_device(name='Device 1'),
            create_test_device(name='Device 2'),
        ]

        instances = (
            cls.model(
                device=devices[0],
                process_tag='CORE',
                net='49.0001.0000.0000.0001.00',
                is_type='level-1-2',
                vrf=None,
            ),
            cls.model(
                device=devices[0],
                process_tag='EDGE',
                net='49.0001.0000.0000.0002.00',
                is_type='level-2-only',
                vrf=None,
            ),
            cls.model(
                device=devices[0],
                process_tag='FABRIC',
                net='49.0001.0000.0000.0003.00',
                is_type='level-1',
                vrf=vrf,
            ),
        )
        cls.model.objects.bulk_create(instances)

        cls.form_data = {
            'device': devices[1].pk,
            'process_tag': 'ACCESS',
            'net': '49.0001.0000.0000.0004.00',
            'is_type': 'level-1-2',
            'vrf': vrf.pk,
        }

        cls.bulk_edit_data = {
            'description': 'A test instance description',
            'vrf': vrf.pk,
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:isisinstance_{}'


class ISISInterfaceViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = ISISInterface

    @classmethod
    def setUpTestData(cls):
        devices = [
            create_test_device(name='Device 1'),
            create_test_device(name='Device 2'),
        ]
        interfaces = (
            Interface(name='Interface 1', device=devices[0], type='virtual'),
            Interface(name='Interface 2', device=devices[0], type='virtual'),
            Interface(name='Interface 3', device=devices[1], type='virtual'),
            Interface(name='Interface 4', device=devices[1], type='virtual'),
        )
        Interface.objects.bulk_create(interfaces)

        instances = (
            ISISInstance(
                device=devices[0],
                process_tag='CORE',
                net='49.0001.0000.0000.0001.00',
                is_type='level-1-2',
            ),
            ISISInstance(
                device=devices[0],
                process_tag='EDGE',
                net='49.0001.0000.0000.0002.00',
                is_type='level-2-only',
            ),
            ISISInstance(
                device=devices[1],
                process_tag='FABRIC',
                net='49.0001.0000.0000.0003.00',
                is_type='level-1',
            ),
            ISISInstance(
                device=devices[1],
                process_tag='ACCESS',
                net='49.0001.0000.0000.0004.00',
                is_type='level-1-2',
            ),
        )
        ISISInstance.objects.bulk_create(instances)

        isis_interfaces = (
            cls.model(
                interface=interfaces[0],
                instance=ISISInstance.objects.get(process_tag='CORE'),
                address_family='ipv4',
                passive=False,
            ),
            cls.model(
                interface=interfaces[1],
                instance=ISISInstance.objects.get(process_tag='EDGE'),
                address_family='ipv6',
            ),
            cls.model(
                interface=interfaces[2],
                instance=ISISInstance.objects.get(process_tag='FABRIC'),
                address_family='ipv4',
                passive=False,
            ),
        )
        cls.model.objects.bulk_create(isis_interfaces)

        cls.form_data = {
            'interface': interfaces[3].pk,
            'instance': ISISInstance.objects.get(process_tag='ACCESS').pk,
            'address_family': 'ipv6',
            'circuit_type': 'level-1-2',
            'network_type': 'point-to-point',
            'metric': 10,
            'passive': True,
        }

        cls.bulk_edit_data = {
            'description': 'A test interface description',
            'passive': False,
            # hello auth type + key must be settable together in one bulk edit:
            # ISISInterface.clean() requires the pair, and the view runs
            # full_clean() per object, so exposing the type without the key would
            # make any auth bulk-edit fail validation.
            'hello_auth_type': 'md5',
            'hello_auth_key': 's3cret',
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:isisinterface_{}'

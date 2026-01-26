from django.db.models import ForeignKey

from utilities.testing import ViewTestCases

from netbox_routing.models.objects import *

__all__ = (
    'ASPathTestCase',
    'ASPathEntryTestCase',
)


class NBRObjectMixin:

    @classmethod
    def setUpTestData(cls):
        name = cls.model._meta.verbose_name
        items = []

        for seq in range(1, 4):
            items.append(
                cls.model(
                    name=f'{name} {seq}',
                ),
            )
        cls.model.objects.bulk_create(items)

        cls.form_data = {
            'name': f'{name} 4',
        }

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }


class NBRObjectEntryMixin:

    @classmethod
    def setUpTestData(cls):
        parent_field = None
        parent = None
        for parent_field in cls.model._meta.fields:
            if isinstance(parent_field, ForeignKey) and parent_field.name != 'owner':
                print(parent_field)
                parent = parent_field.related_model(
                    name=parent_field.related_model._meta.verbose_name
                )
                parent.full_clean()
                parent.save()
                break

        items = []
        for seq in range(1, 4):
            args = {
                parent_field.name: parent,
                'action': 'permit',
                'sequence': seq,
                cls.key_field: cls.key_value,
            }
            items.append(
                cls.model(**args),
            )
        cls.model.objects.bulk_create(items)

        cls.form_data = {
            parent_field.name: parent.pk,
            'action': 'permit',
            'sequence': 9999,
            cls.key_field: cls.key_value,
        }

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }


class ASPathTestCase(
    NBRObjectMixin,
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
    model = ASPath

    def _get_base_url(self):
        return 'plugins:netbox_routing:aspath_{}'


class ASPathEntryTestCase(
    NBRObjectEntryMixin,
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
    model = ASPathEntry
    key_field = 'pattern'
    key_value = '^.*$'

    def _get_base_url(self):
        return 'plugins:netbox_routing:aspathentry_{}'


class PrefixListTestCase(
    NBRObjectMixin,
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
    model = PrefixList

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data.update({'family': 4})
        data = PrefixList.objects.all()
        for instance in data:
            instance.family = 4
            instance.full_clean()
            instance.save()

    def _get_base_url(self):
        return 'plugins:netbox_routing:prefixlist_{}'


class PrefixListEntryTestCase(
    NBRObjectEntryMixin,
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
    model = PrefixListEntry
    key_field = 'prefix'
    key_value = '10.0.0.0/24'

    def _get_base_url(self):
        return 'plugins:netbox_routing:prefixlistentry_{}'


class RouteMapTestCase(
    NBRObjectMixin,
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
    model = RouteMap

    def _get_base_url(self):
        return 'plugins:netbox_routing:routemap_{}'


class RouteMapEntryTestCase(
    NBRObjectEntryMixin,
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
    model = RouteMapEntry
    key_field = 'match'
    key_value = {
        'tags': 1234,
    }

    def _get_base_url(self):
        return 'plugins:netbox_routing:routemapentry_{}'

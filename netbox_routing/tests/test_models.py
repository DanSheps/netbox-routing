from django.apps import apps
from django.db.models import UniqueConstraint
from django.test import SimpleTestCase

from netbox_routing.tests.community.test_models import *
from netbox_routing.tests.eigrp.test_models import *
from netbox_routing.tests.isis.test_models import *
from netbox_routing.tests.ospf.test_models import *
from netbox_routing.tests.static.test_models import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'ISISSettingModelTestCase',
    'ISISFlexAlgoModelTestCase',
    'ISISPrefixSIDModelTestCase',
    'ISISSegmentRoutingCleanTestCase',
    'ISISSRv6LocatorModelTestCase',
    'ISISMigrationStateTestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
    'ModelOrderingTestCase',
    'AggregateModelTestExportsTestCase',
)


class ModelOrderingTestCase(SimpleTestCase):
    def test_concrete_models_have_total_ordering(self):
        invalid_ordering = {}

        for model in apps.get_app_config('netbox_routing').get_models():
            if model._meta.abstract:
                continue

            ordering = model._meta.ordering
            if not ordering:
                invalid_ordering[model._meta.label] = ordering
                continue

            ordering_fields = {field.lstrip('-') for field in ordering}
            unique_field_sets = [
                {field.name}
                for field in model._meta.fields
                if field.unique and not field.null
            ]
            unique_field_sets.extend(
                set(fields)
                for fields in model._meta.unique_together
                if all(not model._meta.get_field(field).null for field in fields)
            )
            unique_field_sets.extend(
                set(constraint.fields)
                for constraint in model._meta.constraints
                if isinstance(constraint, UniqueConstraint)
                and constraint.fields
                and constraint.condition is None
                and (
                    constraint.nulls_distinct is False
                    or all(
                        not model._meta.get_field(field).null
                        for field in constraint.fields
                    )
                )
            )

            last_field = ordering[-1].lstrip('-')
            if last_field not in ('pk', 'id') and not any(
                fields <= ordering_fields for fields in unique_field_sets
            ):
                invalid_ordering[model._meta.label] = ordering

        self.assertEqual(
            invalid_ordering,
            {},
            f'models without total ordering: {invalid_ordering}',
        )


class AggregateModelTestExportsTestCase(SimpleTestCase):
    """Guard that this aggregate re-exports every model TestCase from the submodules
    it wildcard-imports, so ``from netbox_routing.tests.test_models import *`` (used for
    test discovery) cannot silently drop one — e.g. ISISSettingModelTestCase."""

    SUBMODULES = ('community', 'eigrp', 'isis', 'ospf', 'static')

    def test_all_submodule_testcases_reexported(self):
        import importlib

        # Check that each submodule TestCase is both listed in this aggregate's
        # ``__all__`` *and* actually bound on the module. ``__all__`` membership
        # alone is not enough: if a ``from ... import *`` line is dropped but the
        # name is left in ``__all__``, ``from netbox_routing.tests.test_models
        # import *`` raises AttributeError at discovery time — the very
        # regression this guard exists to catch — while a tuple-only check stays
        # green.
        aggregate = importlib.import_module('netbox_routing.tests.test_models')
        missing = {}
        for name in self.SUBMODULES:
            sub = importlib.import_module(f'netbox_routing.tests.{name}.test_models')
            for cls_name in getattr(sub, '__all__', ()):
                if cls_name not in __all__ or not hasattr(aggregate, cls_name):
                    missing.setdefault(name, []).append(cls_name)
        self.assertEqual(
            missing, {}, f'aggregate fails to re-export submodule exports: {missing}'
        )

    def test_isis_testcases_reexported_in_all_aggregates(self):
        import importlib

        # The models/api/forms aggregates each ``from ...isis.<mod> import *`` and must
        # list every IS-IS submodule TestCase in their own ``__all__`` and bind it —
        # the same contract the models guard above enforces, applied to the api and
        # forms aggregates too (test_api listed only 2 of the IS-IS API cases, and
        # test_forms dropped ISISBulkEditFieldsetTestCase).
        checks = (
            (
                'netbox_routing.tests.test_models',
                'netbox_routing.tests.isis.test_models',
            ),
            ('netbox_routing.tests.test_api', 'netbox_routing.tests.isis.test_api'),
            ('netbox_routing.tests.test_forms', 'netbox_routing.tests.isis.test_forms'),
            ('netbox_routing.tests.test_views', 'netbox_routing.tests.isis.test_views'),
            (
                'netbox_routing.tests.test_filtersets',
                'netbox_routing.tests.isis.test_filtersets',
            ),
        )
        missing = {}
        for aggregate_name, submodule_name in checks:
            aggregate = importlib.import_module(aggregate_name)
            aggregate_all = getattr(aggregate, '__all__', ())
            sub = importlib.import_module(submodule_name)
            for cls_name in getattr(sub, '__all__', ()):
                if cls_name not in aggregate_all or not hasattr(aggregate, cls_name):
                    missing.setdefault(aggregate_name, []).append(cls_name)
        self.assertEqual(
            missing, {}, f'aggregates fail to re-export IS-IS test cases: {missing}'
        )

    def test_search_indexes_reexported_in_package(self):
        # search/__init__.py must re-export every SearchIndex that search/isis.py
        # exports so `from netbox_routing.search import <Index>` stays in sync with
        # the @register_search-decorated classes.
        import importlib

        search = importlib.import_module('netbox_routing.search')
        isis_search = importlib.import_module('netbox_routing.search.isis')
        missing = [
            name
            for name in getattr(isis_search, '__all__', ())
            if name not in getattr(search, '__all__', ()) or not hasattr(search, name)
        ]
        self.assertEqual(
            missing, [], f'search package fails to re-export IS-IS indexes: {missing}'
        )

    def test_isis_serializers_expose_tags(self):
        # Every IS-IS serializer models a PrimaryModel (tags-capable); tags must be
        # in Meta.fields or the API can neither return nor accept them.
        import importlib

        serializers = importlib.import_module('netbox_routing.api.serializers')
        names = (
            'ISISFlexAlgoSerializer',
            'ISISLevelSerializer',
            'ISISInterfaceLevelSerializer',
            'ISISSegmentRoutingSerializer',
            'ISISSettingSerializer',
            'ISISInstanceSerializer',
            'ISISInterfaceSerializer',
            'ISISPrefixSIDSerializer',
            'ISISSRv6LocatorSerializer',
        )
        missing = [
            name
            for name in names
            if 'tags' not in getattr(serializers, name).Meta.fields
        ]
        self.assertEqual(
            missing, [], f'IS-IS serializers missing tags in Meta.fields: {missing}'
        )
